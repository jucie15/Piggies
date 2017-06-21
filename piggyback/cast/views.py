import json
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from cast.models import *

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
    congressman_list = Congressman.objects.filter(tag__contains=tag) # 국회의원 리스트

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

    congressman = get_object_or_404(Congressman, pk=cm_pk)

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

def contents_emotion(request, contents_pk):
    # 컨텐츠의 감정표현 처리
    if request.is_ajax():
        # ajax 요청일 경우
        user = request.user # 현재 유저의 정보를 받아온다.
        contents = get_object_or_404(Contents, pk=contents_pk) # 현재 콘텐츠 인스턴스 생성
        emotion_name = request.GET.get('emotion_name','') # url GET 정보에 담겨있는 감정정보를 받아온다.
        if user.contents_emotion_set.filter(contents=contents).exists():
            # 해당 컨텐츠에 감정 표현을 이미 해놓은 경우
            contents_emotion = user.contents_emotion_set.get(contents=contents) # 해당유저가 컨텐츠에 해놓은 감정표현을 정보를 받아와
            contents_emotion.name = emotion_name # 감정을 바꿔준 후 저장
            contents_emotion.save()
        else:
            # 감정표현을 처음 하는 경우 새롭게 생성
            ContentsEmotion.objects.create(
                user=user,
                contents=contents,
                name=emotion_name,
            )
        context = {}
        context['status'] = 'success'

    else:
        context = {}
        context['message'] = '잘못된 접근입니다.'
        context['status'] = 'fail'

    # dic 형식을 json 형식으로 바꾸어 전달한다.
    return HttpResponse(json.dumps(context), content_type='application/json')

def pledge_emotion(request, pledge_pk):
    # 컨텐츠의 감정표현 처리
    if request.is_ajax():
        # ajax 요청일 경우
        user = request.user # 현재 유저의 정보를 받아온다.
        pledge = get_object_or_404(Pledge, pk=pledge_pk) # 현재 공약 인스턴스 생성
        emotion_name = request.GET.get('emotion_name','') # url GET 정보에 담겨있는 감정정보를 받아온다.
        if user.pledge_emotion_set.filter(pledge=pledge).exists():
            # 해당 공약에 감정 표현을 이미 해놓은 경우
            pledge_emotion = user.pledge_emotion_set.get(pledge=pledge) # 해당유저가 컨텐츠에 해놓은 감정표현을 정보를 받아와
            pledge_emotion.name = emotion_name # 감정을 바꿔준 후 저장
            pledge_emotion.save()
        else:
            # 감정표현을 처음 하는 경우 새롭게 생성
            PledgeEmotion.objects.create(
                user=user,
                pledge=pledge,
                name=emotion_name,
            )
        context = {}
        context['status'] = 'success'

    else:
        context = {}
        context['message'] = '잘못된 접근입니다.'
        context['status'] = 'fail'

    # dic 형식을 json 형식으로 바꾸어 전달한다.
    return HttpResponse(json.dumps(context), content_type='application/json')

def congressman_emotion(request, congressman_pk):
    # 컨텐츠의 감정표현 처리
    if request.is_ajax():
        # ajax 요청일 경우
        user = request.user # 현재 유저의 정보를 받아온다.
        congressman = get_object_or_404(Congressman, pk=congressman_pk) # 현재 콘텐츠 인스턴스 생성
        emotion_name = request.GET.get('emotion_name','') # url GET 정보에 담겨있는 감정정보를 받아온다.
        if user.congressman_emotion_set.filter(congressman=congressman).exists():
            # 해당 컨텐츠에 감정 표현을 이미 해놓은 경우
            congressman_emotion = user.congressman_emotion_set.get(congressman=congressman) # 해당유저가 컨텐츠에 해놓은 감정표현을 정보를 받아와
            congressman_emotion.name = emotion_name # 감정을 바꿔준 후 저장
            congressman_emotion.save()
        else:
            # 감정표현을 처음 하는 경우 새롭게 생성
            CongressmanEmotion.objects.create(
                user=user,
                congressman=congressman,
                name=emotion_name,
            )
        context = {}
        context['status'] = 'success'

    else:
        context = {}
        context['message'] = '잘못된 접근입니다.'
        context['status'] = 'fail'

    # dic 형식을 json 형식으로 바꾸어 전달한다.
    return HttpResponse(json.dumps(context), content_type='application/json')
