import requests
import re
from bs4 import BeautifulSoup
import os

member_url = 'http://www.assembly.go.kr/assm/memact/congressman/memCond/memCondListAjax.do?&rowPerPage=400' # 요청을 보낼 Url

response = requests.get(member_url) # member_url로 보낸 요청에 대한 응답

if response.encoding is None:
    # 인코딩이 없을 경우 urf-8로 설정
    response.encoding = 'utf-8'

member_html = response.text
member_soup = BeautifulSoup(member_html, 'html.parser') # html_parser 생성

for img_tag in member_soup.select('.img a img'):
    # img 태그를 찾아 순회
    img_url = 'http://www.assembly.go.kr' + img_tag['src'] # src 속성에서 파일 이름을 따온다.

    member_name = img_tag.get('alt').split(' ')[0] # 이름은 img 태그에 alt 속성에서 가져온다.

    member_id = img_tag['src'].split('/')[2].split('.')[0] # 멤버 아이디

    filename = img_tag['src'].split('/')[2] # src속성에서 이미지 파일 이름만을 따와 파일이름으로 결정한다.

    img_filepath = os.path.join('cast', 'static', 'cast', 'img', filename)

    name_filepath = os.path.join('cast', 'static', 'cast', 'txt', 'congressman_list.txt')

    dirpath = os.path.dirname(img_filepath)

    if not os.path.exists(dirpath):
        # 디렉토리가 없을 경우 디렉토리 생성
        os.makedirs(dirpath)

    if not os.path.exists(img_filepath):
        # 해당 이미지 파일이 없을 경우
        img_data = requests.get(img_url).content # 이미지를 불러온다.

        with open(img_filepath, 'wb') as f:
            # 이미지 파일 저장
            f.write(img_data)

        with open(name_filepath, 'at') as f:
            # 국회의원의 이름만 따로 파일에 저장
            f.write(member_name + ',' + member_id + '\n')




