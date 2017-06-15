from django.contrib.auth.views import login as auth_login
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.templatetags.socialaccount import get_providers
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from accounts.forms import ProfileForm
from accounts.models import Profile

def login(request):
    # social_login 페이지
    providers = []
    for provider in get_providers(): # settings/INSTALLED_APPS 내에서 활성화된 목록
    # social_app속성은 provider에는 없는 속성입니다.
        try:
            # 실제 Provider별 Client id/secret 이 등록이 되어있는가?
            provider.social_app = SocialApp.objects.get(provider=provider.id, sites=settings.SITE_ID)
        except SocialApp.DoesNotExist:
            provider.social_app = None
        providers.append(provider)

    return auth_login(request,
        #authentication_form=LoginForm,
        template_name='accounts/login_form.html',
        extra_context={'providers': providers})

def signup_info(request):
    # 회원 가입 정보 입력 페이지

    if Profile.objects.filter(user=request.user).exists():
        # 사용자 프로필 정보가 이미 존재할 경우 관심 태그 입력 페이지로.
        return redirect('accounts:signup_tag')

    if request.method == 'POST' :
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False) # 사용자한테 받아온 정보로 프로필 폼 인스턴스 생성(모델에 저장하지 않음)
            profile.user = request.user # 프로필 유저에 유저 정보 저장
            profile.user.username = profile.user.socialaccount_set.first().extra_data['properties']['nickname'] # 유저의 이름은 카카오톡 닉네임으로 저장
            profile.user.email = profile.user.socialaccount_set.first().extra_data['kaccount_email'] # 유저의 이메일은 카카오톡 아이디로 저장
            profile.user.save() # 유저 모델에 저장
            profile.save() # 프로필 모델에 저장
            return redirect('accounts:signup_tag')
    else :
        form = ProfileForm()
    return render(request, 'accounts/signup_info.html', {
        'form': form,
    })

def signup_tag(request):
    return HttpResponse('adasdas')

@login_required
def profile(request):
 return render(request, 'accounts/profile.html')
