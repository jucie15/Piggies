import urllib.request
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.conf import settings
from django.shortcuts import reverse
from django.utils.functional import cached_property
from tagging.registry import register
from collections import Counter

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
    comment_number = models.IntegerField(default=0) # 댓글의 개수
    like_number = models.IntegerField(default=0) # 좋아요 개수
    dislike_number = models.IntegerField(default=0) # 싫어요 개수
    surprise_number = models.IntegerField(default=0) # 놀라워요 개수
    angry_number = models.IntegerField(default=0) # 화나요 개수
    laugh_number = models.IntegerField(default=0) # 웃겨요 개수
    sad_number = models.IntegerField(default=0) # 슬퍼요 개수

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

    def get_count_emotion(self, emotion):
        # 해당 컨텐츠의 각 감정들의 개수 카운트
        emotion_count = ContentsEmotion.objects.filter(contents_id=self.id, name=emotion).count()
        return emotion_count

    @classmethod
    def delete_empty_contents(cls, queryset):
        for content in queryset:
            if(content.contents_type == '1'): #동영상 컨텐츠만 삭제한다.
                url_path = content.url_path
                image_path = "https://img.youtube.com/vi/" + url_path[30:] + "/0.jpg"
                try:
                    urllib.request.urlopen(image_path)
                except:
                    print(image_path+"는 없는 동영상 주소. 삭제합니다.")
                    Contents.objects.filter(url_path=url_path).delete()

    def update_comment_number(self):
        # 댓글 개수 업데이트
        self.comment_number = self.comment_set.all().count()
        self.save(update_fields=['comment_number'])

    def update_emotion_number(self):
        # 감정 개수 업데이트
        emotion_list = ContentsEmotion.objects.filter(contents_id=self.id).values_list('name', flat=True) #
        emotion_number_list = Counter(emotion_list)
        self.like_number = emotion_number_list['1']
        self.dislike_number = emotion_number_list['2']
        self.surprise_number = emotion_number_list['3']
        self.angry_number = emotion_number_list['4']
        self.laugh_number = emotion_number_list['5']
        self.sad_number = emotion_number_list['6']
        self.save()

register(Contents)

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
    like_number = models.IntegerField(default=0) # 좋아요 개수
    dislike_number = models.IntegerField(default=0) # 싫어요 개수
    comment_number = models.IntegerField(default=0) # 댓글의 개수

    class Meta():
        ordering =['id']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cast:congressman_detail', args=[self.pk])

    def get_count_emotion(self, emotion):
        # 해당 국회의원의 각 감정들의 개수 카운트
        emotion_count = CongrssmanEmotion.objects.filter(congressman_id=self.id, name=emotion).count()
        return emotion_count

    def update_comment_number(self):
        # 댓글 개수 업데이트 함수
        self.comment_number = self.comment_set.all().count()
        self.save(update_fields=['comment_number'])

    def update_emotion_number(self):
        # 감정 개수 업데이트
        emotion_list = CongressmanEmotion.objects.filter(congressman_id=self.id).values_list('name', flat=True) #
        emotion_number_list = Counter(emotion_list)
        self.like_number = emotion_number_list['1']
        self.dislike_number = emotion_number_list['2']
        self.save()


register(Congressman)

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
    like_number = models.IntegerField(default=0) # 좋아요 개수
    dislike_number = models.IntegerField(default=0) # 싫어요 개수
    comment_number = models.IntegerField(default=0) # 댓글의 개수

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cast:pledge_detail', args = [self.pk])

    def get_count_emotion(self, emotion):
        # 해당 공약의 각 감정들의 개수 카운트
        emotion_count = PledgeEmotion.objects.filter(pledge_id=self.id, name=emotion).count()
        return emotion_count

    def max_emotion_count(self):
        # 감정 표현 중 가장 큰 값 리턴 함수
        if self.like_number >= self.dislike_number:
            return self.like_number
        else:
            return self.dislike_number

    def update_comment_number(self):
        # 댓글 개수 업데이트 함수
        self.comment_number = self.comment_set.all().count()
        self.save(update_fields=['comment_number'])

    def update_emotion_number(self):
        # 감정 개수 업데이트
        emotion_list = PledgeEmotion.objects.filter(pledge_id=self.id).values_list('name', flat=True) #
        emotion_number_list = Counter(emotion_list)
        self.like_number = emotion_number_list['1']
        self.dislike_number = emotion_number_list['2']
        self.save()

register(Pledge)

class ContentsEmotion(models.Model):
    # 컨텐츠내 감정 표현 관계 모델

    CONTENTS_EMOTION_CHOICE = (
        ('0', '선택안함'),
        ('1', '좋아요'),
        ('2', '싫어요'),
        ('3', '놀라워요'),
        ('4', '화나요'),
        ('5', '웃겨요'),
        ('6', '슬퍼요'),
    ) # 감정 표현 종류

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='contents_emotion_set') # 유저와 1:N 관계 설정
    contents = models.ForeignKey(Contents) # 컨텐츠와 1:N 관계 설정
    name = models.CharField(max_length=2, default='0', choices=CONTENTS_EMOTION_CHOICE) # 감정의 이름

    def __str__(self):
        return self.get_name_display() # name 필드의 Choice Value 값을 보여 준다.

    @staticmethod
    def on_post_update(sender, **kwargs):
        # 컨텐츠 감정표현 클릭 시(생성, 삭제, 변경)
        contents_emotion = kwargs['instance'] # 생성된 인스턴스를 받아온다.
        contents_emotion.contents.update_emotion_number()

post_delete.connect(ContentsEmotion.on_post_update, sender=ContentsEmotion)
post_save.connect(ContentsEmotion.on_post_update, sender=ContentsEmotion)

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

    @staticmethod
    def on_post_update(sender, **kwargs):
        # 컨텐츠 감정표현 클릭 시(생성, 삭제, 변경)
        pledge_emotion = kwargs['instance'] # 생성된 인스턴스를 받아온다.
        pledge_emotion.pledge.update_emotion_number()

post_delete.connect(PledgeEmotion.on_post_update, sender=PledgeEmotion)
post_save.connect(PledgeEmotion.on_post_update, sender=PledgeEmotion)

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
    @staticmethod
    def on_post_update(sender, **kwargs):
        # 컨텐츠 감정표현 클릭 시(생성, 삭제, 변경)
        congressman_emotion = kwargs['instance'] # 생성된 인스턴스를 받아온다.
        congressman_emotion.congressman.update_emotion_number()

post_delete.connect(CongressmanEmotion.on_post_update, sender=CongressmanEmotion)
post_save.connect(CongressmanEmotion.on_post_update, sender=CongressmanEmotion)

class Comment(models.Model):
    # 댓글 모델

    user = models.ForeignKey(settings.AUTH_USER_MODEL) # 해당 댓글을 쓴 유저와 1:N 관계 설졍
    contents = models.ForeignKey(Contents, default=None, null=True) # 컨텐츠에 댓글이 달릴 경우 관계 설정
    congressman = models.ForeignKey(Congressman, default=None, null=True) # 국회의원에 댓글이 달릴 경우 관계 설정
    pledge = models.ForeignKey(Pledge, default=None, null=True) # 공약에 댓글이 달릴 경우 관계 설정
    message = models.TextField() # 댓글 내용
    created_at = models.DateTimeField(auto_now_add=True) # 댓글 작성 시간
    like_number = models.IntegerField(default=0) # 좋아요 개수
    dislike_number = models.IntegerField(default=0) # 싫어요 개수
    recomment_number = models.IntegerField(default=0) # 대댓글 개수

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return "{}의 댓글 {}".format(self.user, self.message)

    @cached_property
    def user_avatar_url(self):
        socialaccount = self.user.socialaccount_set.all().first()
        if socialaccount:
            return socialaccount.get_avatar_url()
        return None

    def update_emotion_number(self, emotions):
        # 감정 개수 업데이트
        for emotion in emotions:
            if emotion == '1':
                # 좋아요일 경우
                self.like_number = self.commentemotion_set.filter(name=emotion).count()
            elif emotion == '2':
                # 싫어요일 경우
                self.dislike_number = self.commentemotion_set.filter(name=emotion).count()
        self.save(update_fields=['dislike_number', 'like_number']) # 두개의 필드만 업데이트하여 저장

    def update_recomment_number(self):
        self.recomment_number = self.recomment_set.all().count()
        self.save(update_fields=['recomment_number'])

    @staticmethod
    def on_post_save(sender, **kwargs):
        # 댓글 생성시 실행되는 함수
        comment = kwargs['instance'] # 생성된 인스턴스를 받아온다.
        if kwargs['created']:
            # 지금 생성된게 맞다면
            if comment.contents != None:
                comment.contents.update_comment_number()
            elif comment.pledge != None:
                comment.pledge.update_comment_number()
            elif comment.congressman != None:
                comment.congressman.update_comment_number()

    @staticmethod
    def on_post_delete(sender, **kwargs):
        # 댓글 삭제시 실행되는 함수
        comment = kwargs['instance'] # 실제로는 삭제된 데이터로 사용에 주의해야함.
        if comment.contents != None:
            comment.contents.update_comment_number()
        elif comment.pledge != None:
            comment.pledge.update_comment_number()
        elif comment.congressman != None:
            comment.congressman.update_comment_number()

post_save.connect(Comment.on_post_save, sender=Comment)
post_delete.connect(Comment.on_post_delete, sender=Comment)

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

    def on_post_save(sender, **kwargs):
        # 대댓글 생성시 실행되는 함수
        recomment = kwargs['instance'] # 생성된 인스턴스를 받아온다,
        if kwargs['created']:
            # 지금 생성된게 맞다면
            recomment.comment.update_recomment_number()

    def on_post_delete(sender, **kwargs):
        # 대댓글 삭제시 실행되는 함수
        recomment = kwargs['instance'] # 실제로는 삭제된 데이터로 사용에 주의해야함.
        recomment.comment.update_recomment_number()

post_save.connect(ReComment.on_post_save, sender=ReComment)
post_delete.connect(ReComment.on_post_delete, sender=ReComment)

class Favorite(models.Model):
    # 즐겨찾기

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='favorite_set') # 유저와 1:N 관계 생성
    contents = models.ForeignKey(Contents, default=None, null=True) # 컨텐츠와 1:N 관계 생성
    pledge = models.ForeignKey(Pledge, default=None, null=True) # 공약과 1:N 관계 생성
    congressman = models.ForeignKey(Congressman, default=None, null=True) # 국회의원 1:N 관계 생성

    def __str__(self):
        if self.contents != None:
            return self.contents.title
        elif self.pledge != None:
            return self.pledge.title
        elif self.congressman != None:
            return self.congressman.name


    def get_absolute_url(self):
        if self.contents != None:
            return reverse('cast:contents_detail', args=[self.contents.pk])
        elif self.pledge != None:
            return reverse('cast:pledge_detail', args=[self.pledge.pk])
        elif self.congressman != None:
            return reverse('cast:congressman_detail', args=[self.congressman.pk])

