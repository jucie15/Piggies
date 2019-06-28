import requests
import re
from bs4 import BeautifulSoup
import os

'''
http://www.assembly.go.kr/assm/memPop/memPopup.do?dept_cd=9770276
멤버의 아이디를 이용해 페이지를 바꿔가며 크롤링 한다.
'''

with open('cast/static/cast/txt/congressman_list.txt','rt') as f:
    mem_list = f.read().split('\n')

mem_id_list = [];
for mem_id in mem_list:
    # 멤버의 아이디만을 리스트에 담는다.
    if mem_id != '':
        mem_id_list.append(mem_id.split(',')[1])

for mem_id in mem_id_list:
    # 국회의원의 아이디를 통해 세부페이지를 순회하며 크롤링한다.
    req_url = 'http://www.assembly.go.kr/assm/memPop/memPopup.do?dept_cd=' + mem_id # 요청을 보낼 URL

    response = requests.get(req_url)

    if response.encoding is None:
        # 인코딩이 없을 경우 utf-8로 설정
        response.encoding = 'utf-8'

    html = response.text
    soup = BeautifulSoup(html, 'html.parser') # html_parser 생성

    mem_dic = {} # 각 데이터를 사전형으로 만들어 관리
    mem_name = soup.select('.left .profile h4')[0].text # 국회의원 이름
    save_data = '이름:' + mem_name + '\n' # 저장할 데이터 내용에 이름 추가
    save_data += 'id:' + mem_id + '\n' # 저장할 데이터 내용에 id 추가

    for dt_tag , dd_tag in zip(soup.select('.cont_in dt') , soup.select('.cont_in dd')):
        # dt 태그를 찾아 순회

        mem_index = dt_tag.text # 각 dt들을 인덱스로 사용
        mem_value = dd_tag.text # 각 dd들을 값으로 사용

        if mem_index=='약력' or mem_index=='정당' or mem_index=='선거구' or mem_index=='이메일':
            # 원하는 정보만 사용
            mem_dic[mem_index] = mem_value
            save_data += mem_index + ':' + ' '.join(mem_dic[mem_index].split()) + '\n' # 저장할 데이터 내용에 필요한 정보 추가

            #mem_dic[mem_index].replace('\n','').replace('\t','').replace('\r','')

            filename = 'congressman_detail.txt' # 파일 이름
            filepath = os.path.join('cast', 'static', 'cast', 'txt', filename) # 파일 경로
            dirpath = os.path.dirname(filepath) # 파일이 있는 디렉토리 경로

            if not os.path.exists(dirpath):
                # 파일 경로가 없을 경우 생성
                os.makedirs(dirpath)

    save_data += '\n' # 일단 구분이 용이하게 각 국회의원별로 한칸 씩 개행

    with open(filepath, 'at') as f:
        f.write(save_data)

