import re
from django.db import models
from django.conf import settings
from django.forms import ValidationError
from cast.models import Favorite
from tagging.registry import register

def birth_validator(value):
    if not re.match(r'^\d{8}$', value):
        raise ValidationError("19910101")

class Profile(models.Model):
    # 사용자 추가 정보 모델
    SEX_CHOICES = (
        ('1','MALE'),
        ('2','FEMALE'),
    ) # 성별 종류 명시

    user = models.OneToOneField(settings.AUTH_USER_MODEL) # AUTH_USER 모델과 1:1 관계 설장
    nickname = models.CharField(max_length=16, null=True, verbose_name='닉네임') # 닉네임
    sex = models.CharField(max_length=2, choices=SEX_CHOICES, verbose_name='성별') # 성별
    birth = models.CharField(max_length=16, null=True, verbose_name='생년월일', validators=[birth_validator]) # 생년월일
    city = models.CharField(max_length=16, null=True, verbose_name='시/도') # 시/도
    district = models.CharField(max_length=8, null=True, verbose_name='구') # 구

    def __str__(self):
        return '{}-{}'.format(self.user.username, self.nickname)

register(Profile)
