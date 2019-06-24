import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "piggyback.settings")
import re
import requests
from bs4 import BeautifulSoup

import django
django.setup()

from django.conf import settings

def get_fuckers_info():
    url = 'http://www.assembly.go.kr/assm/memact/congressman/memCond/memCondListAjax.do'
    data = {'currentPage' : 1, 'rowPerPage': 300}
    req = requests.post(url, data=data)
    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    for fucker in soup.select('.memberna_list dl dt a'):
        fucker_name = fucker.text
        fucker_id = re.search(r'\d+', fucker['href']).group(0)
        with open(settings.ROOT_FROM_CAST_APP('fucker-list.txt'), 'a', encoding='utf8') as f:
            a_fucker = fucker_name + ',' + fucker_id + '\n'
            f.write(a_fucker)

if __name__ == '__main__':
    get_fuckers_info()