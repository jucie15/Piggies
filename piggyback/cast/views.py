import json
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count, Max
from tagging.models import Tag, TaggedItem
from cast.models import *
from cast.forms import CommentForm, ReCommentForm
from accounts.models import Profile

def index(request):
    # 메인 페이지
    contents_list = Contents.objects.all()
    page = request.GET.get('page', 1) # 페이지 번호를 받아온다.
    paginator = Paginator(contents_list, 4) # 페이지 당 4개씩 표현

    try:
        # 페이지 번호가 있으면 해당 페이지로 이동
        contents_list = paginator.page(page)
    except PageNotAnInteger:
        # 페이지 번호가 숫자가 아닐 경우 첫페이지로 이동
        contents_list = paginator.page(1)
    except EmptyPage:
        # 페이지가 비어있을 경우 paginator.num_page = 총 페이지 개수
        contents_list = paginator.page(paginator.num_pages)

    context = {}
    context['contents_list'] = contents_list

    return render(request, 'cast/index.html', context)

def tagged_list(request):
    # 해당 태그가 포함 되어있는 전체 리스트
    tag = request.GET.get('tag','')

    pledge_list = TaggedItem.objects.get_by_model(Pledge, tag) # 공약 리스트
    contents_list = TaggedItem.objects.get_by_model(Contents, tag) # 콘텐츠 리스트
    congressman_list = TaggedItem.objects.get_by_model(Congressman, tag) # 국회의원 리스트

    context = {}
    context['contents_list'] = contents_list
    context['pledge_list'] = pledge_list
    context['congressman_list'] = congressman_list

    return render(request, 'cast/search.html', context)

def contents_detail(request, contents_pk):
    # 컨텐츠 세부 페이지

    contents = get_object_or_404(Contents, pk=contents_pk)

    if request.user.is_anonymous():
        # 로그인을 안했을 경우
        user_is_favorite = False
    else:
        if request.user.favorite_set.filter(contents=contents).exists():
            user_is_favorite = True
        else:
            user_is_favorite = False

    comment_form = CommentForm()

    context = {}
    context['contents'] = contents
    context['comment_form'] = comment_form
    context['user_is_favorite'] = user_is_favorite

    return render(request, 'cast/contents_detail.html', context)

def congressman_detail(request, congressman_pk):
    # 국회의원 세부 페이지

    congressman = get_object_or_404(Congressman, pk=congressman_pk)
    comment_form = CommentForm()

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
    context['comment_form'] = comment_form

    return render(request, 'cast/congressman_detail.html', context)

def pledge_detail(request, pledge_pk):
    # 공약 세부 페이지
    pledge = get_object_or_404(Pledge, pk=pledge_pk)
    comment_form = CommentForm()

    context = {}
    context['pledge'] = pledge
    context['comment_form'] = comment_form

    return render(request, 'cast/pledge_detail.html', context)

def contents_emotion(request, contents_pk):
    # 컨텐츠의 감정표현 처리
    if request.is_ajax():
        # ajax 요청일 경우
        user = request.user # 현재 유저의 정보를 받아온다.
        contents = get_object_or_404(Contents, pk=contents_pk) # 현재 콘텐츠 인스턴스 생성
        emotion_name = request.GET.get('emotion_name','') # url GET 정보에 담겨있는 감정정보를 받아온다.
        before_emotion_name = ''
        if user.contents_emotion_set.filter(contents=contents).exists():
            # 해당 컨텐츠에 감정 표현을 이미 해놓은 경우
            user_emotion = user.contents_emotion_set.get(contents=contents) # 해당유저가 컨텐츠에 해놓은 감정표현을 정보를 받아와
            before_emotion_name = user_emotion.name
            if user_emotion.name == emotion_name:
                # 같은 감정을 한번 더누르면 삭제.
                ContentsEmotion.objects.filter(contents=contents, user=user).delete() # 인스턴스 삭제
            else:
                # 다른 감정을 누를 경우
                user_emotion.name = emotion_name # 감정을 바꿔준 후 저장
                user_emotion.save()
        else:
            # 감정표현을 처음 하는 경우 새롭게 생성
            ContentsEmotion.objects.create(
                user=user,
                contents=contents,
                name=emotion_name,
            )

        emotion_count = ContentsEmotion.objects.filter(contents=contents, name=emotion_name).count()
        before_emotion_count = ContentsEmotion.objects.filter(contents=contents, name=before_emotion_name).count()

        context = {}
        context['status'] = 'success'
        context['emotion_count'] = emotion_count
        context['before_emotion_name'] = before_emotion_name
        context['before_emotion_count'] = before_emotion_count
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
            user_emotion = user.pledge_emotion_set.get(pledge=pledge) # 해당유저가 컨텐츠에 해놓은 감정표현을 정보를 받아와
            if user_emotion.name == emotion_name:
                # 같은 감정을 한번 더누르면 삭제.
                PledgeEmotion.objects.filter(pledge=pledge, user=user).delete() # 인스턴스 삭제
            else:
                # 다른 감정을 누를 경우
                user_emotion.name = emotion_name # 감정을 바꿔준 후 저장
                user_emotion.save()
        else:
            # 감정표현을 처음 하는 경우 새롭게 생성
            PledgeEmotion.objects.create(
                user=user,
                pledge=pledge,
                name=emotion_name,
            )

        context = {}
        context['status'] = 'success'
        data = json.dumps(context)
    else:
        context = {}
        context['message'] = '잘못된 접근입니다.'
        context['status'] = 'fail'
        data = json.dumps(context)

    mimetype = 'application/json'
    # dic 형식을 json 형식으로 바꾸어 전달한다.
    return HttpResponse(data, mimetype)

def congressman_emotion(request, congressman_pk):
    # 컨텐츠의 감정표현 처리
    if request.is_ajax():
        # ajax 요청일 경우
        user = request.user # 현재 유저의 정보를 받아온다.
        congressman = get_object_or_404(Congressman, pk=congressman_pk) # 현재 콘텐츠 인스턴스 생성
        emotion_name = request.GET.get('emotion_name','') # url GET 정보에 담겨있는 감정정보를 받아온다.
        if user.congressman_emotion_set.filter(congressman=congressman).exists():
            # 해당 컨텐츠에 감정 표현을 이미 해놓은 경우
            user_emotion = user.congressman_emotion_set.get(congressman=congressman) # 해당유저가 컨텐츠에 해놓은 감정표현을 정보를 받아와
            if user_emotion.name == emotion_name:
                # 같은 감정을 한번 더누르면 삭제.
                CongressmanEmotion.objects.filter(congressman=congressman, user=user).delete() # 인스턴스 삭제
            else:
                # 다른 감정을 누를 경우
                user_emotion.name = emotion_name # 감정을 바꿔준 후 저장
                user_emotion.save()
        else:
            # 감정표현을 처음 하는 경우 새롭게 생성
            CongressmanEmotion.objects.create(
                user=user,
                congressman=congressman,
                name=emotion_name,
            )
        context = {}
        context['status'] = 'success'
        data = json.dumps(context)
    else:
        context = {}
        context['message'] = '잘못된 접근입니다.'
        context['status'] = 'fail'
        data = json.dumps(context)

    mimetype = 'application/json'
    # dic 형식을 json 형식으로 바꾸어 전달한다.
    return HttpResponse(data, mimetype)

def comment_list(request, pk):
    # 각 컨텐츠별 댓글 리스트

    req_type = request.GET.get('type','') # 요청한 컨텐츠 타입이 무엇인지

    contents = get_object_or_404(Contents, pk=pk)
    best_comment_list = Comment.objects.filter(contents=contents).order_by('-like_number')[:5] # 좋아요 순 정렬
    comment_list = Comment.objects.filter(contents=contents).exclude(id__in=best_comment_list) # 베댓 제외한 나머지 댓글
    comment_form = CommentForm()

    context = {}
    context['comment_form'] = comment_form
    context['comment_list'] = comment_list
    context['best_comment_list'] = best_comment_list
    context['pk'] = pk

    return render(request, 'cast/comment_list.html', context)

@login_required
def comment_new(request, pk):
    # 각 컨텐츠내 댓글 쓰기

    req_type = request.GET.get('type','') # 요청한 컨텐츠 타입이 무엇인지
    redirect_path = request.GET.get('next','') # 해당 컨텐츠로 리디렉션 하기위한 url_path

    if request.method == 'POST':
        # 포스트 요청일 경우
        form = CommentForm(request.POST, request.FILES) # 받아온 데이터를 통해 폼 인스턴스 생성

        if form.is_valid():
            # 폼에 데이터가 유효할 경우
            comment = form.save(commit=False) # 디비에 저장하지 않고 인스턴스 생성
            comment.user = request.user # 댓글을 다는 유저 정보

            # 각 컨텐츠 별로 분기하여 인스턴스 생성
            if req_type == 'contents':
                # 컨텐츠일 경우
                contents = get_object_or_404(Contents, pk=pk)
                comment.contents = contents
            elif req_type == 'pledge':
                # 공약일 경우
                pledge = get_object_or_404(Pledge, pk=pk)
                comment.pledge = pledge
            else:
                # 국회의원일 경우
                congressman = get_object_or_404(Congressman, pk=pk)
                comment.congressman = congressman

            comment.save() # 유저와 해당 컨텐츠 연결 후 디비에 저장
            return redirect(redirect_path)
    else:
        # 포스트 요청이 아닐 경우 빈 폼 생성
        form = CommentForm()

    return render(request, 'cast/comment_form.html', {
        'form' : form,
        }) # 포스트 요청이 아닐 경우 빈 폼으로 페이지 렌더링

@login_required
def comment_edit(request, comment_pk):
    # 해당 댓글 수정
    comment = get_object_or_404(Comment, pk=comment_pk) # 해당 댓글 인스턴스
    redirect_path = request.GET.get('next','') # 해당 컨텐츠로 리디렉션 하기위한 url_path

    if comment.user != request.user:
        messages.warning(request, '댓글 작성자만 수정할 수 있습니다.')
        return redirect(redirect_path)

    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            comment = form.save()
            messages.success(request, '기존 댓글을 수정했습니다.')
            return redirect(redirect_path)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'cast/comment_form.html', {
        'form': form,
    })

@login_required
def comment_delete(request, comment_pk):
    # 해당 댓글 삭제
    comment = get_object_or_404(Comment, pk=comment_pk)
    redirect_path = request.GET.get('next','') # 해당 컨텐츠로 리디렉션 하기위한 url_path

    if comment.user != request.user:
        messages.warning(request, '댓글 작성자만 삭제할 수 있습니다.')
    else:
        comment.delete()
        messages.success(request, '댓글을 삭제했습니다.')
    return redirect(redirect_path)

def comment_emotion(request, comment_pk):
    # 해당 댓글의 좋아요/싫어요
    if request.is_ajax():
        # ajax 요청일 경우
        user = request.user # 현재 유저의 정보를 받아온다.
        comment = get_object_or_404(Comment, pk=comment_pk) # 현재 댓글 인스턴스 생성
        emotion_name = request.GET.get('emotion_name','') # url GET 정보에 담겨있는 즇아요/싫어요 정보를 받아온다.

        if user.comment_emotion_set.filter(comment=comment).exists():
            # 해당 댓글에 감정 표현을 이미 해놓은 경우
            user_emotion = user.comment_emotion_set.get(comment=comment) # 해당유저가 댓글에 해놓은 감정표현을 정보를 받아와
            if user_emotion.name == emotion_name:
                # 같은 감정을 한번 더누르면 삭제.
                CommentEmotion.objects.filter(comment=comment, user=user).delete() # 인스턴스 삭제
            else:
                # 다른 감정을 누를 경우
                user_emotion.name = emotion_name # 감정을 바꿔준 후 저장
                user_emotion.save()
                emotion_name = ('1','2')
        else:
            # 감정표현을 처음 하는 경우 새롭게 생성
            CommentEmotion.objects.create(
                user=user,
                comment=comment,
                name=emotion_name,
            )

        comment.update_emotion_number(emotion_name) # 감정 개수 업데이트
        like_number = comment.like_number
        dislike_number = comment.dislike_number

        context = {}
        context['status'] = 'success'
        context['like_number'] = like_number
        context['dislike_number'] = dislike_number
        data = json.dumps(context)
    else:
        context = {}
        context['message'] = '잘못된 접근입니다.'
        context['status'] = 'fail'
        data = json.dumps(context)

    mimetype = 'application/json'
    # dic 형식을 json 형식으로 바꾸어 전달한다.
    return HttpResponse(data, mimetype)

@login_required
def recomment_new(request, comment_pk):
    # 대댓글 달기

    comment = get_object_or_404(Comment, pk=comment_pk)
    redirect_path = request.GET.get('next','') # 해당 컨텐츠로 리디렉션 하기위한 url_path

    if request.method == 'POST':
        # 포스트 요청일 경우
        form = ReCommentForm(request.POST, request.FILES) # 받아온 데이터를 통해 폼 인스턴스 생성

        if form.is_valid():
            # 폼에 데이터가 유효할 경우
            recomment = form.save(commit=False) # 디비에 저장하지 않고 인스턴스 생성
            recomment.user = request.user
            recomment.comment = comment
            recomment.save() # 유저와 공약 연결 후 디비에 저장
            messages.success(request, '새 댓글을 저장했습니다.')

            return redirect(redirect_path)
    else:
        # 포스트 요청이 아닐 경우 빈 폼 생성
        form = CommentForm()

    return render(request, 'cast/comment_form.html', {
        'form' : form,
        }) # 포스트 요청이 아닐 경우 빈 폼으로 페이지 렌더링

@login_required
def recomment_delete(request, recomment_pk):
    # 공약 디테일 내 댓글 지우기

    recomment = get_object_or_404(ReComment, pk=recomment_pk)
    redirect_path = request.GET.get('next','') # 해당 컨텐츠로 리디렉션 하기위한 url_path

    if recomment.user != request.user:
        # 댓글 작성자와 현재 유저가 다를 경우
        messages.warning(request, '작성자만 삭제할 수 있습니다.')
    else:
        # 작성자와 동일할 경우
        recomment.delete() # 댓글 삭제
        messages.success(request, '댓글을 삭제했습니다.')

    return redirect(redirect_path)

def ajax_tag_autocomplete(request):
    # 태그 검색 자동완성 기능
    if request.is_ajax():
        # ajax 요청일 경우 실행
        term = request.GET.get('term','') # jquery autocomplete은 GET 방식으로 term이라는 키에 값을 넣어서 요청을 보내온다.
        tags = Tag.objects.filter(name__icontains=term)[:5] # tag_name에 key값이 포함되어 있는 리스트를 받아온다.
        results = []
        for tag in tags:
            # 검색된 태그 목록들을 json형식으로 넘겨주기 위해 사전형으로 구성된 자료로 바꾼 후 리스트에 담아놓는다.
            tag_json = {}
            tag_json['id'] = tag.id
            tag_json['label'] = tag.name
            tag_json['value'] = tag.name
            results.append(tag_json)
        data = json.dumps(results) # json형식으로 변환
        mimetype = 'application/json'
        return HttpResponse(data, mimetype)

def ajax_favorites(request, pk):
    # 즐겨찾기 버튼 클릭 시
    if request.is_ajax():
        # ajax 요청일 경우
        user = request.user
        req_type = request.POST.get('type','')

        isFavorite = False # 즐겨찾기 상태를 확인할 변수

        if req_type == 'contents':
            # 컨텐츠에서 요청이 왔을 경우
            contents = get_object_or_404(Contents, pk=pk) # 컨텐츠 인스턴스 생성
            if user.favorite_set.filter(contents=contents).exists():
                # 유저가 이미 해당 컨텐츠를 즐겨찾기 추가해놨으면 삭제
                Favorite.objects.filter(contents=contents, user=user).delete()
                isFavorite = False # 즐겨찾기 해제
            else:
                # 추가되어 있지 않았다면 추가
                Favorite.objects.create(
                    user=user,
                    contents=contents,
                    )
                isFavorite = True # 즐겨찾기 추가
        elif req_type == 'pledge':
            # 공약에서 요청이 왔을 경우
            pledge = get_object_or_404(Pledge, pk=pk) # 공약 인스턴스 생성
            if user.favorite_set.filter(pledge=pledge).exists():
                # 유저가 이미 해당 공약을 즐겨찾기 추가해놨으면 삭제
                Favorite.objects.filter(pledge=pledge, user=uesr).delete()
                isFavorite = False

            else:
                # 추가 되어 있지 않다면 추가
                Favorite.objects.create(
                    user=user,
                    pledge=pledge,
                    )
                isFavorite = True
        else:
            # 국회의원 페이지에서 요청이 왔을 경우
            congressman = get_object_or_404(Congressman, pk=pk) # 의원 인스턴스 생성
            if user.favorite_set.filter(congressman=congressman).exists():
                # 유저가 이미 해당 국회의원을 즐겨찾기에 추가해놨으면 삭제
                Favorite.objects.filter(congressman=congressman, user=user).delete()
                isFavorite = False

            else:
                # 추가되어있지 않았다면 추가
                Favorite.objects.create(
                    user=user,
                    congressman=congressman,
                    )
                isFavorite = True

        context = {}
        context['isFavorite'] = isFavorite
        context['status'] = 'success'
        data = json.dumps(context) # json 형식으로 파싱
    else:
        data = json.dumps({
            'status': 'fail',
            }) # json 형식으로 파싱
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def ajax_add_tag(request, pk):
    # 태그 추가 버튼 클릭시
    if request.is_ajax():
        # ajax 요청시
        tag = request.GET.get('tag','')
        req_type = request.GET.get('type','')

        if req_type == 'contents':
            objects = get_object_or_404(Contents, pk=pk)
        elif req_type == 'pledge':
            objects = get_object_or_404(Pledge, pk=pk)
        else:
            objects = get_object_or_404(Congressman, pk=pk)

        Tag.objects.add_tag(objects, tag) # 해당 인스턴스에 태그 추가

        data = json.dumps({
            'status': 'success',
            }) # json 형식으로 파싱

    else:
        data = json.dumps({
            'status': 'fail',
            }) # json 형식으로 파싱

    mimetype = 'application/json'
    return HttpResponse(data, mimetype)
