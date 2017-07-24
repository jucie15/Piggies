from django import template
from cast.models import Contents


register = template.Library()

@register.filter(name='emotion_count')
def emotion_count(contents, emotion):
    return contents.get_count_emotion(emotion)
