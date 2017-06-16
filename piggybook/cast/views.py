from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from cast.models import Content

def index(request):
    content_list = Content.objects.all()

    context = {}
    context['content_list'] = content_list
    return render(request, 'cast/index.html', context)
