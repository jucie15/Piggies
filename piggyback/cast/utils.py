import requests
import re
import os
import time
from selenium import webdriver
from bs4 import BeautifulSoup
from cast.models import *


ROOT = lambda *args: os.path.join(settings.BASE_DIR, 'cast', 'static', 'cast', 'txt', *args)

def contents_db_create():
    # youtube 영상을 크롤링함과 동시에 디비에 저장

    driver = webdriver.Firefox() # 파이어폭스를 불러온다.

    with open(ROOT('crawling_list.txt'), 'rt') as f:
        keyword_list = f.read().split('\n')[:-1] # 파일에서 키워드 리스트를 받아온다

    for keyword in keyword_list:
        list_url = 'https://www.youtube.com/results?sp=CAM%253D&q=' + keyword # 각 키워드를 통해 url을 만든다.

        driver.get(list_url) # 파이어폭스를 통해 url에 접속

        list_html = driver.page_source # 접속한 페이지의 소스를 받아온다,
        list_soup = BeautifulSoup(list_html, 'html.parser') # html_parser 생성

        for a_tag in list_soup.select('.yt-lockup-thumbnail a[href*=watch]'):
            # 영상리스트 페이지에서 각 영상들의 url을 받아오기 위해 a태그를 받아온다 검색결과에 영상뿐아니라 다른 결과물도 있어 href속성에 watch가 들어가있는 태그만 불러온다..

            watch_url = 'https://www.youtube.com' +a_tag['href'] # a태그의 href를 통해 url 파싱

            driver.get(watch_url) # 영상 url로 접속

            watch_html = driver.page_source
            watch_soup = BeautifulSoup(watch_html, 'html.parser') # 각 영상 페이지의 html_parser 생성

            contents_title = watch_soup.select('.watch-title-container span')[0]['title'] # 해당 페이지에서 제목을 받아온다.
            contents_desc = watch_soup.select('#watch-description-text p')[0].text # 해당 페이지에서 설명글을 받아온다.
            contents_embed_url = 'https://www.youtube.com/embed/' + a_tag['href'].split('=')[-1] # 해당 페이지의 url을 통해 embed url을 만들어낸다.

            if not Contents.objects.filter(title=contents_title).exists():
                # DB에 해당 글이 없을 경우 저장
                contents = Contents()
                contents.contents_type = 1
                contents.title = contents_title
                contents.description = contents_desc
                contents.url_path = contents_embed_url
                contents.save()
