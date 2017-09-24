from cast.utils import contents_db_create
import kronos
import random

@kronos.register('* * * * *')
def cron_contents_crawling():
    contents_db_create()
