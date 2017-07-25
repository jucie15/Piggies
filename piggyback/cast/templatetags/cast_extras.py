from django import template
from cast.models import Contents


register = template.Library()

@register.filter(name='emotion_count')
def emotion_count(objects, emotion):
    return objects.get_count_emotion(emotion)
