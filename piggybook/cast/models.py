from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from tagging.fields import TagField



class Content(models.Model):
    # 컨텐츠(뉴스/영상) 모델
    CONTENT_CHOICES = (
        ('0','뉴스'),
        ('1','영상')
    ) # 컨텐츠 타입 명시

    content_type = models.CharField(max_length=2, null=True, verbose_name='타입', choices=CONTENT_CHOICES) # 컨텐츠 종류
    url_path = models.CharField(max_length=128, null=True, verbose_name='컨텐츠URL') # 컨텐츠 원본 URL
    title = models.CharField(max_length=64, null=True, verbose_name='제목') # 컨텐츠 제목
    description = models.TextField(max_length=1024) # 컨텐츠 내용
    tag = TagField() # 컨텐츠 태그

    def __str__(self):
        return self.title

class CongressMan(models.Model):
    # 국회의원 모델
    name = models.CharField(max_length=32) #국회의원 이름
    profile_image_path = models.CharField(max_length=512, null=True, blank=True) # 프로필 사진 저장 경로
    description = models.TextField(max_length=512, null=True, blank=True) # 추가 정보
    party = models.CharField(max_length=32, null=True, blank=True) # 정당
    constituency = models.CharField(max_length=32, null=True, blank=True) # 선거구
    email = models.CharField(max_length=64, null=True, blank=True) # 이메일 주소
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True) # 업데이트 날짜
    tag = TagField() # 국회의원 태그

    class Meta():
        ordering =['id']

    def __str__(self):
        return self.name

class Pledge(models.Model):
    # 공약 모델
    PLEDGE_STATUS_CHOICE = (
        ('0', '미시행'),
        ('1', '진행중'),
        ('2', '시행완료'),
        ('3', '시행실패'),
    ) # 공약 상태 ENUM 변수처럼 사용하기 위한 임시 변수

    congressman = models.ForeignKey(CongressMan) # 국회의원 모델과 1toN 관계 설정
    title = models.CharField(max_length=32) # 공약 이름
    status = models.CharField(max_length=2, choices=PLEDGE_STATUS_CHOICE) # 공약 상태
    description = models.TextField(max_length=1024) # 공약에 대한 추가 설명
    created_at = models.DateTimeField(auto_now_add=True) # 공약 날짜
    tag = TagField() # 공약 태그



    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cast:pledge_detail', args = [self.pk])

