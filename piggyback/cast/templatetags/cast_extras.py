from django import template
from cast.models import Contents


register = template.Library()

@register.filter(name='emotion_count')
def emotion_count(objects, emotion):
    # 템플릿의 감정 표현 개수 카운트 태그
    return objects.get_count_emotion(emotion) # 모델 인스턴스의 카운트 해주는 함수 호출

