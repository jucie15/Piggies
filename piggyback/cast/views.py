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

def contents_detail(request, contents_pk):
    # 컨텐츠 세부 페이지

    contents = get_object_or_404(Contents, pk=contents_pk)

    context = {}
    context['contents'] = contents

    return render(request, 'cast/contents_detail.html', context)

def congressman_detail(request, cm_pk):
    # 국회의원 세부 페이지

    congressman = get_object_or_404(CongressMan, pk=cm_pk)

    pledge_status = {}

    try:
        pledge_status['not_enforcement'] = congressman.pledge_set.filter(status='0').count() / congressman.pledge_set.all().count() * 100
        pledge_status['progress'] = congressman.pledge_set.filter(status='1').count() / congressman.pledge_set.all().count() * 100
        pledge_status['complete'] = congressman.pledge_set.filter(status='2').count() / congressman.pledge_set.all().count() * 100
        pledge_status['falied'] = congressman.pledge_set.filter(status='3').count() / congressman.pledge_set.all().count() * 100
    except ZeroDivisionError:
        pledge_status['not_enforcement'] = 100
        pledge_status['progress'] = 0
        pledge_status['complete'] =0
        pledge_status['falied'] = 0

    context = {}
    context['congressman'] = congressman
    context['pledge_status'] = pledge_status

    return render(request, 'cast/congressman_detail.html', context)

def pledge_detail(request, pledge_pk):
    # 공약 세부 페이지
    pledge = get_object_or_404(Pledge, pk=pledge_pk)
    # comment_form = CommentForm()

    context = {}
    context['pledge'] = pledge
    # context['comment_form'] = comment_form

    return render(request, 'cast/pledge_detail.html', context)
