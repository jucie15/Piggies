from django import template
from cast.models import Contents


register = template.Library()

@register.filter(name='emotion_count')
def emotion_count(objects, emotion):
    # 템플릿의 감정 표현 개수 카운트 태그
    return objects.get_count_emotion(emotion) # 모델 인스턴스의 카운트 해주는 함수 호출

@register.filter(name='max_count')
def max_emotion_count(objects):
    # 감정표현 개수 중 가장 큰 값을 알려주는 태그
    return objects.max_emotion_count() # 모델 인스턴스의 가장 큰 값 찾아주는 함수 호출

