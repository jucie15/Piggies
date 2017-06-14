from django.db import models
from django.conf import settings

class Profile(models.Model):
    # 사용자 추가 정보 모델
    SEX_CHOICES = (
        ('1','MALE'),
        ('2','FEMALE'),
    ) # 성별 종류 명시

    user = models.OneToOneField(settings.AUTH_USER_MODEL) # AUTH_USER 모델과 1:1 관계 설장
    sex = models.CharField(max_length=2, choices=SEX_CHOICES, verbose_name='성별') # 성별
    birth = models.CharField(max_length=16, null=True, verbose_name='생년월일') # 생년월일
    city = models.CharField(max_length=16, null=True, verbose_name='시/도') # 시/구
    district = models.CharField(max_length=8, null=True, verbose_name='구') # 구


