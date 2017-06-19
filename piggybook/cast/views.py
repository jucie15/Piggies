from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from cast.models import Contents, Pledge, CongressMan

def index(request):
    # 메인 페이지
    contents_list = Contents.objects.all()

    context = {}
    context['contents_list'] = contents_list
    return render(request, 'cast/index.html', context)

def tagged_list(request):
    # 해당 태그가 포함 되어있는 전체 리스트

    tag = request.GET.get('tag','')

    pledge_list = Pledge.objects.filter(tag__contains=tag) # 공약 리스트
    contents_list = Contents.objects.filter(tag__contains=tag) # 콘텐츠 리스트
    congressman_list = CongressMan.objects.filter(tag__contains=tag) # 국회의원 리스트

    context = {}
    context['contents_list'] = contents_list
    context['pledge_list'] = pledge_list
    context['congressman_list'] = congressman_list

    return render(request, 'cast/tagged_list.html', context)

