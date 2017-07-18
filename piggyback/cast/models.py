import urllib
from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from tagging.fields import TagField

class Contents(models.Model):
    # 컨텐츠(뉴스/영상) 모델

    CONTENTS_CHOICES = (
        ('0','뉴스'),
        ('1','영상')
    ) # 컨텐츠 타입 명시

    contents_type = models.CharField(max_length=2, null=True, verbose_name='타입', choices=CONTENTS_CHOICES) # 컨텐츠 종류
    url_path = models.CharField(max_length=128, null=True, verbose_name='컨텐츠URL') # 컨텐츠 원본 URL
    title = models.CharField(max_length=64, null=True, verbose_name='제목') # 컨텐츠 제목
    description = models.TextField(max_length=1024) # 컨텐츠 내용
    emotion = models.ManyToManyField(settings.AUTH_USER_MODEL, through='ContentsEmotion') # 감정 표현 모델을 통해 유저와 M:N 관계 설정
    tag = TagField() # 컨텐츠 태그

    class Meta:
        verbose_name_plural = 'contents' # 모델 복수개 명칭(admin표시)
        ordering = ['id']

    def get_absolute_url(self):
        return reverse('cast:contents_detail',
            args=[self.pk])

    def get_image_url(self):
        image = self.url_path
        image = "https://img.youtube.com/vi/" + image[30:] + "/0.jpg"
        return image

    def __str__(self):
        return '{}번 {}'.format(self.id, self.title)

    @property
    def get_count_emotion(self):
        # 해당 컨텐츠의 각 감정들의 개수 카운트 @property 장식자를 통해 템플릿에서 쉽게 접근하게 한다.
        total_number = {} # 각 감정들의 개수를 담을 dic 변수
        for idx in range(1,7):
            # 각 감정들 별로 개수 카운트
            total_number[idx] = ContentsEmotion.objects.filter(contents_id=self.id, name=idx).count()
        return total_number




class Congressman(models.Model):
    # 국회의원 모델
    name = models.CharField(max_length=32) #국회의원 이름
    profile_image_path = models.CharField(max_length=512, null=True, blank=True) # 프로필 사진 저장 경로
    description = models.TextField(max_length=512, null=True, blank=True) # 추가 정보
    party = models.CharField(max_length=32, null=True, blank=True) # 정당
    constituency = models.CharField(max_length=32, null=True, blank=True) # 선거구
    email = models.CharField(max_length=64, null=True, blank=True) # 이메일 주소
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True) # 업데이트 날짜
    emotion = models.ManyToManyField(settings.AUTH_USER_MODEL, through='CongressmanEmotion') # 감정 표현 모델을 통해 유저와 M:N 관계 설정
    tag = TagField() # 국회의원 태그

    class Meta():
        ordering =['id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cast:congressman_detail', args=[self.pk])


    @property
    def get_count_emotion(self):
        # 해당 국회의원의 좋아요/싫어요 개수 카운트 @property 장식자를 통해 템플릿에서 쉽게 접근하게 한다.
        total_number = {} # 각 감정들의 개수를 담을 dic 변수
        for idx in range(1,3):
            # 각 감정들 별로 개수 카운트
            total_number[idx] = CongressmanEmotion.objects.filter(congressman_id=self.id, name=idx).count()
        return total_number

class Pledge(models.Model):
    # 공약 모델
    PLEDGE_STATUS_CHOICE = (
        ('0', '미시행'),
        ('1', '진행중'),
        ('2', '시행완료'),
        ('3', '시행실패'),
    ) # 공약 상태 ENUM 변수처럼 사용하기 위한 임시 변수

    congressman = models.ForeignKey(Congressman) # 국회의원 모델과 1toN 관계 설정
    title = models.CharField(max_length=32) # 공약 이름
    status = models.CharField(max_length=2, choices=PLEDGE_STATUS_CHOICE) # 공약 상태
    description = models.TextField(max_length=1024) # 공약에 대한 추가 설명
    created_at = models.DateTimeField(auto_now_add=True) # 공약 날짜
    emotion = models.ManyToManyField(settings.AUTH_USER_MODEL, through='PledgeEmotion') # 감정 표현 모델을 통해 유저와 M:N 관계 설정
    tag = TagField() # 공약 태그

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cast:pledge_detail', args = [self.pk])

    @property
    def get_count_emotion(self):
        # 해당 공약의 좋아요/싫어요 개수 카운트 @property 장식자를 통해 템플릿에서 쉽게 접근하게 한다.
        total_number = {} # 각 감정들의 개수를 담을 dic 변수
        for idx in range(1,3):
            # 각 감정들 별로 개수 카운트
            total_number[idx] = PledgeEmotion.objects.filter(pledge_id=self.id, name=idx).count()
        return total_number

class ContentsEmotion(models.Model):
    # 컨텐츠내 감정 표현 관계 모델

    CONTENTS_EMOTION_CHOICE = (
        ('0', '선택안함'),
        ('1', '역겨워요'),
        ('2', '놀라워요'),
        ('3', '기뻐요'),
        ('4', '슬퍼요'),
        ('5', '화나요'),
        ('6', '멋져요'),
    ) # 감정 표현 종류

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='contents_emotion_set') # 유저와 1:N 관계 설정
    contents = models.ForeignKey(Contents) # 컨텐츠와 1:N 관계 설정
    name = models.CharField(max_length=2, default='0', choices=CONTENTS_EMOTION_CHOICE) # 감정의 이름

    def __str__(self):
        return self.get_name_display() # name 필드의 Choice Value 값을 보여 준다.

class PledgeEmotion(models.Model):
    # 공약내 감정 표현 관계 모델

    PLEDGE_EMOTION_CHOICE = (
        ('0', '선택안함'),
        ('1', '좋아요'),
        ('2', '싫어요'),
    ) # 감정 표현 종류

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='pledge_emotion_set') # 유저와 1:N 관계 설정
    pledge = models.ForeignKey(Pledge) # 공약모델과 1:N 관계 설정
    name = models.CharField(max_length=2, default='0', choices=PLEDGE_EMOTION_CHOICE) # 감정의 이름

    def __str__(self):
        return self.get_name_display() # name 필드의 Choice Value 값을 보여 준다.

class CongressmanEmotion(models.Model):
    # 국회의원내 감정 표현 관계 모델

    CONGRESSMAN_EMOTION_CHOICE = (
        ('0', '선택안함'),
        ('1', '좋아요'),
        ('2', '싫어요'),
    ) # 감정 표현 종류

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='congressman_emotion_set') # 유저와 1:N 관계 설정
    congressman = models.ForeignKey(Congressman) #  국회의원모델과 1:N 관계 설정
    name = models.CharField(max_length=2, default='0', choices=CONGRESSMAN_EMOTION_CHOICE) # 감정의 이름

    def __str__(self):
        return self.get_name_display() # name 필드의 Choice Value 값을 보여 준다.

class Comment(models.Model):
    # 댓글 모델

    user = models.ForeignKey(settings.AUTH_USER_MODEL) # 해당 댓글을 쓴 유저와 1:N 관계 설졍
    contents = models.ForeignKey(Contents, default=None, null=True) # 컨텐츠에 댓글이 달릴 경우 관계 설정
    congressman = models.ForeignKey(Congressman, default=None, null=True) # 국회의원에 댓글이 달릴 경우 관계 설정
    pledge = models.ForeignKey(Pledge, default=None, null=True) # 공약에 댓글이 달릴 경우 관계 설정
    message = models.TextField() # 댓글 내용
    created_at = models.DateTimeField(auto_now_add=True) # 댓글 작성 시간

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return "{}의 댓글 {}".format(self.user, self.message)

    @property
    def get_count_emotion(self):
        # 해당 댓글의 각 감정들의 개수 카운트 @property 장식자를 통해 템플릿에서 쉽게 접근하게 한다.
        total_number = {} # 각 감정들의 개수를 담을 dic 변수
        for idx in range(1,3):
            # 각 감정들 별로 개수 카운트
            total_number[idx] = CommentEmotion.objects.filter(comment_id=self.id, name=idx).count()
        return total_number

class CommentEmotion(models.Model):
    # 댓글의 좋아요/싫어요

    LIKE_DISLIKE_CHOICE = (
        ('0', '선택안함'),
        ('1', '좋아요'),
        ('2', '싫어요'),
    ) # 감정 표현 종류

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='comment_emotion_set') # 유저와 1:N 관계 설졍
    comment = models.ForeignKey(Comment) # 해당 댓글과 1:N 관계 설정
    name = models.CharField(max_length=2, default='0', choices=LIKE_DISLIKE_CHOICE) # 감정의 이름

    def __str__(self):
        return self.get_name_display() # name 필드의 Choice Value 값을 보여 준다.

class ReComment(models.Model):
    # 대댓글

    user = models.ForeignKey(settings.AUTH_USER_MODEL) # 유저와 1:N 관계 설정
    comment = models.ForeignKey(Comment) # 해당 댓글과 1:N 관계 설정
    message = models.TextField() # 대댓글의 내용

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return "{}의 댓글 {}".format(self.user, self.message)

class Favorite(models.Model):
    # 즐겨찾기

    user = models.ForeignKey(settings.AUTH_USER_MODEL) # 유저와 1:N 관계 생성
    contents = models.ForeignKey(Contents, default=None, null=True) # 컨텐츠와 1:N 관계 생성
    pledge = models.ForeignKey(Pledge, default=None, null=True) # 공약과 1:N 관계 생성
    congressman = models.ForeignKey(Congressman, default=None, null=True) # 국회의원 1:N 관계 생성

    def __str__(self):
        if self.contents != None:
            return self.contents.title
        elif self.pledge != None:
            return self.pledge.title
        else:
            return self.congressman.name


