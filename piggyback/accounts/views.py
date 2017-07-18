from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from accounts.forms import ProfileForm, TagForm
from accounts.models import Profile

@login_required
def signup_info(request):
    # 회원 가입 정보 입력 페이지
    print(request.POST)
    if Profile.objects.filter(user=request.user).exists():
        # 사용자 프로필 정보가 이미 존재할 경우 메인 페이지로
        return redirect('cast:index')

    if request.method == 'POST' :
        form = ProfileForm(request.POST)
        print(form)
        if form.is_valid():
            profile = form.save(commit=False) # 사용자한테 받아온 정보로 프로필 폼 인스턴스 생성(모델에 저장하지 않음)
            profile.user = request.user # 프로필 유저에 유저 정보 저장
            profile.user.username = profile.user.socialaccount_set.first().extra_data['properties']['nickname'] # 유저의 이름은 카카오톡 닉네임으로 저장
            profile.user.email = profile.user.socialaccount_set.first().extra_data['kaccount_email'] # 유저의 이메일은 카카오톡 아이디로 저장
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

    user = request.user.profile # 현재 유저의 프로필 정보
    if request.method == 'POST':
        user.tag = request.POST.get('tag','') # 요청 유저의 태그 정보를 받아온 태그 정보로 저장
        user.save() # 디비에 프로필 정보 저장
        return redirect('accounts:profile')
    else:
        form = TagForm(instance = user) # 유저 정보를 받아와 폼 인스턴스 생성
    return render(request, 'accounts/tag_form.html', {
        'form': form,
        })

@login_required
def profile(request):
    profile = get_object_or_404(Profile, user=request.user)

    context = {}
    context['profile'] = profile

    return render(request, 'accounts/profile.html', context )
