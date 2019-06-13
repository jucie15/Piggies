from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as django_logout
from django.conf import settings
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import ProfileForm
from accounts.models import Profile
from tagging.models import Tag, TaggedItem
import json
import requests

def login(request):
    return render(request, 'accounts/login.html')

def logout(request):
    django_logout(request)
    return redirect('cast:index')

@login_required
def signup_info(request):
    # 회원 가입 정보 입력 페이지
    if Profile.objects.filter(user=request.user).exists():
        # 사용자 프로필 정보가 이미 존재할 경우 메인 페이지로
        return redirect('cast:index')

    if request.method == 'POST' :
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False) # 사용자한테 받아온 정보로 프로필 폼 인스턴스 생성(모델에 저장하지 않음)
            profile.user = request.user # 프로필 유저에 유저 정보 저장
            profile.user.username = profile.user.socialaccount_set.first().extra_data['properties']['nickname'] # 유저의 이름은 카카오톡 닉네임으로 저장
            profile.user.email = profile.user.socialaccount_set.first().extra_data['kaccount_email'] # 유저의 이메일은 카카오톡 아이디로 저장
            img = request.user.socialaccount_set.first().get_avatar_url() # 카카오 프로필의 이미지 경로를 받아온다.
            image = ContentFile(requests.get(img).content) # 불러온 이미지 데이터를 ContentFile객체로 랩핑한다.
            profile.image.save(profile.user.username, image) # 랩핑된 이미지 데이터를 profile에 저장
            profile.user.save() # 유저 모델에 저장
            profile.save() # 프로필 모델에 저장
            return redirect('accounts:set_tag')
    else :
        form = ProfileForm()

    return render(request, 'accounts/signup_info.html', {
        'form': form,
    })

@login_required
def set_tag(request):
    # 태그 추가/수정 페이지
    return render(request, 'accounts/tag_form.html')

def ajax_add_tag(request):
    # 태그 추가 버튼 클릭시
    if request.is_ajax():
        # ajax 요청시
        tag = request.GET.get('tag','')
        profile = request.user.profile

        Tag.objects.add_tag(profile, tag) # 해당 인스턴스에 태그 추가
        this_tag = Tag.objects.get(name=tag)
        tag_id = this_tag.id


        status = 200
        context = {}
        context['tag_id'] = tag_id
        context['status'] = 'true'
        context['message'] = 'success'
    else:
        status = 403
        context = {}
        context['status'] = 'false'
        context['message'] = 'bad request to not ajax'

    data = json.dumps(context)
    mimetype = 'application/json'
    return HttpResponse(data, mimetype, status=status)

@login_required
def profile(request):
    return render(request, 'accounts/profile.html' )

def tag_delete(request):
    if request.is_ajax():
        tag_id = request.POST.get('tag_id',None)
        tag = Tag.objects.get(id=tag_id)
        tag.delete()
        context={}
    else:
        context={

        }
    return HttpResponse(json.dumps(context), content_type='application/json')
