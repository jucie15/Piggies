import os
import time
from django.shortcuts import get_object_or_404
from selenium import webdriver
from bs4 import BeautifulSoup
from cast.models import *
from tagging.models import Tag


ROOT = lambda *args: os.path.join(settings.BASE_DIR, 'cast', 'static', 'cast', 'txt', *args)


def contents_db_create():
    # youtube 영상을 크롤링함과 동시에 디비에 저장

    driver = webdriver.Chrome('/Users/gustos/Downloads/chromedriver')  # 크롬 드라이버 사용

    with open(ROOT('crawling_list.txt'), 'rt') as f:
        keyword_list = f.read().split('\n')  # 파일에서 키워드 리스트를 받아온다

    for keyword in keyword_list:
        list_url = 'https://www.youtube.com/results?sp=CAMSAggD&search_query=' + keyword  # 각 키워드를 통해 url을 만든다.

        driver.get(list_url)  # 파이어폭스를 통해 url에 접속

        list_html = driver.page_source  # 접속한 페이지의 소스를 받아온다,
        list_soup = BeautifulSoup(list_html, 'html.parser')  # html_parser 생성

        for a_tag in list_soup.select('ytd-thumbnail a[href^=/watch]')[:5]:
            # 영상리스트 페이지에서 각 영상들의 url을 받아오기 위해 a태그를 받아온다 검색결과에 영상뿐아니라 다른 결과물도 있어 href속성에 watch가 들어가있는 태그만 불러온다..

            watch_url = 'https://www.youtube.com' + a_tag['href']  # a태그의 href를 통해 url 파싱

            driver.get(watch_url)  # 영상 URL로 접속
            condition = True
            while condition:
                try:
                    contents_title = driver.find_element_by_css_selector('h1.title').text
                    contents_desc = driver.find_element_by_css_selector('#description').text
                    condition = False
                except Exception as e:
                    print(e)
                    time.sleep(3)

            contents_embed_url = 'https://www.youtube.com/embed/' + a_tag['href'].split('=')[-1]

            if not Contents.objects.filter(title=contents_title).exists():
                # DB에 해당 글이 없을 경우 저장
                contents = Contents()
                contents.contents_type = '1'
                contents.title = contents_title
                contents.description = contents_desc
                contents.url_path = contents_embed_url
                contents.save()


def congressman_db_create():
    # 크롤링 해놓은 데이터를 불러와 디비에 저장
    with open(ROOT("congressman_detail.txt"), "rt") as f:
        mem_detail_list = f.read().split('\n')

    img_path = os.path.join('cast', 'img', 'congressman') # 프로필 사진 경로 설정
    mem_dic = {} # 각 정보를 저장할 사전형 선언

    for mem_detail in mem_detail_list:
        '''
            각 의원별로 개행시켜 놓았기에 개행을 기준하여 디비에 저장한다.
        '''
        if mem_detail != '':
            mem_index = mem_detail.split(':')[0]
            mem_value = mem_detail.split(':')[1]
            mem_dic[mem_index] = mem_value
        else:
            if mem_dic:
                # 의원 데이터가 있을 경우
                congressman = Congressman() # 모델 인스턴스 생성
                congressman.name = mem_dic['이름']
                congressman.profile_image_path = img_path + '/' + mem_dic['id'] + '.png'
                congressman.description = mem_dic['약력']
                congressman.party = mem_dic['정당']
                congressman.constituency = mem_dic['선거구']
                congressman.email = mem_dic['이메일']
                mem_dic = {} # 다음 의원을 위해 변수 초기화
                congressman.save() # 디비에 저장


def congressman_db_update():
    # 크롤링 해놓은 데이터를 불러와 디비에 저장
    with open(ROOT("congressman_detail.txt"), "rt") as f:
        mem_detail_list = f.read().split('\n')

    img_path = os.path.join('cast', 'img', 'congressman') # 프로필 사진 경로 설정
    mem_dic = {} # 각 정보를 저장할 사전형 선언

    for mem_detail in mem_detail_list:
        '''
            각 의원별로 개행시켜 놓았기에 개행을 기준하여 디비에 저장한다.
        '''
        if mem_detail != '':
            mem_index = mem_detail.split(':')[0]
            mem_value = mem_detail.split(':')[1]
            mem_dic[mem_index] = mem_value
        else:
            if mem_dic:
                # 의원 데이터가 있을 경우
                congressman = get_object_or_404(Congressman, name=mem_dic['이름'], description=mem_dic['약력']) # 모델 인스턴스 생성
                congressman.profile_image_path = img_path + '/' + mem_dic['id'] + '.png'
                congressman.description = mem_dic['약력']
                congressman.party = mem_dic['정당']
                congressman.constituency = mem_dic['선거구']
                congressman.email = mem_dic['이메일']
                Tag.objects.add_tag(congressman, mem_dic['정당']) # 해당 인스턴스에 태그 추가
                Tag.objects.add_tag(congressman, '20대') # 해당 인스턴스에 태그 추가
                mem_dic = {} # 다음 의원을 위해 변수 초기화
                congressman.save() # 디비에 저장

def pledge_db_create():
    # 크롤링 해놓은 공약 리스트로 공약 DB 생성
    with open(ROOT("pledge_list.txt"), "rt") as f:
        mem_detail_list = f.read().split('\n')

    mem_dic = {}

    for member in mem_detail_list:
        index = member.split(':')[0]
        value = member.split(':')[1]
        mem_dic[index] = value

        if mem_dic['이름'] != '김종태':
            # 김종대 그는 누구인기!?!?
            if index == '선거구':
                congressman = get_object_or_404(Congressman, name=mem_dic['이름'], constituency__icontains=mem_dic['선거구'])

            if index == '상태':
                if not Pledge.objects.filter(congressman=congressman, title=mem_dic['공약']).exists():
                    # 해당 공약이 존재하지 않으면
                    pledge = Pledge()
                    pledge.congressman = congressman
                    pledge.title = mem_dic['공약']
                    pledge.description = mem_dic['공약']
                    pledge.status = '0'
                    pledge.save()
