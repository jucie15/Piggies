from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from board.models import Feedback, BoardComment
from board.forms import FeedbackForm, BoardCommentForm


def feedback_list(request):
    # 피드백 게시판 리스트
    feedback_list = Feedback.objects.all()

    return render(request, 'board/feedback_list.html', {
            'feedback_list' : feedback_list,
        })

@login_required
def feedback_detail(request, feedback_pk):
    # 피드백 게시판 글 내용
    feedback = get_object_or_404(Feedback, pk=feedback_pk)
    comment_form = BoardCommentForm()

    feedback.hit_count() # 조회수 증가

    return render(request, 'board/feedback_detail.html', {
        'feedback': feedback,
        'comment_form': comment_form,
    })

@login_required
def feedback_new(request):
    # 피드백 게시판 글 쓰기
    if request.method == 'POST':
        # 포스트 요청일 경우
        form = FeedbackForm(request.POST, request.FILES) # 받아온 데이터를 통해 피드백 폼 인스턴스 생성

        if form.is_valid():
            # 값이 유효할 경우
            feedback = form.save(commit=False)
            feedback.user = request.user # 글쓴이를 현재 유저로 저장한 뒤
            feedback.save() # 글 저장
            messages.info(request, '포스팅을 잘 저장했습니다.')
            return redirect(feedback) # feedback get_absolute_url로 이동
    else:
        # 포스트 요청이 아닐경우 빈 폼 인스턴스 생성
        form = FeedbackForm()

    return render(request, 'board/feedback_form.html', {
        'form': form,
    })

@login_required
def feedback_edit(request, feedback_pk):
    # 피드백 게시판 글 수정
    feedback = get_object_or_404(Feedback, pk=feedback_pk) # 해당 게시글의 인스턴스 생성

    if  feedback.user != request.user:
        # 게시글 작성자와 현재 유저가 다를 경우 해당 게시글 페이지로 리다이렉트
        messages.warning(request, '게시글 작성자만 수정할 수 있습니다.')
        return redirect(feedback)

    if request.method == 'POST':
        # 포스트 요청일 경우
        form = FeedbackForm(request.POST, request.FILES, instance=feedback) # 받아온 데이터와 현재 피드백 인스턴스의 데이터를 통해 피드백 폼 인스턴스 생성
        if form.is_valid():
            # 값이 유효할 경우 바뀐 값을 통해 저장
            feedback = form.save(commit=True)
            messages.info(request, '포스팅을 잘 저장했습니다.')
            return redirect(feedback) # feedback get_absolute_url로 이동
    else:
        # 포스트 요청이 아닐 경우
        form = FeedbackForm(instance=feedback) # 현재 피드백 인스턴스의 값을 통해

    return render(request, 'board/feedback_form.html', {
        'form': form,
    })

@login_required
def feedback_delete(request, feedback_pk):
    # 피드백 게시판 글 삭제
    feedback = get_object_or_404(Feedback, pk=feedback_pk) # 해당 게시글의 인스턴스 생성

    if feedback.user != request.user:
        # 게시글의 작성자와 현재 유저가 다를 경우
        messages.warning(request, '게시글 작성자만 삭제할 수 있습니다.')
        redirect(feedback)
    else:
        # 현재 유저와 작성자가 같으면 게시글 삭제
        feedback.delete()
        return redirect('board:feedback_list')

def post_list(request):
    pass

@login_required
def comment_new(request, pk):
    # 각 컨텐츠내 댓글 쓰기

    req_type = request.GET.get('type','') # 요청한 컨텐츠 타입이 무엇인지
    redirect_path = request.GET.get('next','') # 해당 컨텐츠로 리디렉션 하기위한 url_path

    if request.method == 'POST':
        # 포스트 요청일 경우
        form = BoardCommentForm(request.POST, request.FILES) # 받아온 데이터를 통해 폼 인스턴스 생성

        if form.is_valid():
            # 폼에 데이터가 유효할 경우
            comment = form.save(commit=False) # 디비에 저장하지 않고 인스턴스 생성
            comment.user = request.user # 댓글을 다는 유저 정보

            # 각 컨텐츠 별로 분기하여 인스턴스 생성
            if req_type == 'feedback':
                # 피드백일 경우
                feedback = get_object_or_404(Feedback, pk=pk)
                comment.feedback = feedback

            comment.save() # 유저와 해당 컨텐츠 연결 후 디비에 저장
            return redirect(redirect_path)
    else:
        # 포스트 요청이 아닐 경우 빈 폼 생성
        form = BoardCommentForm()

    return render(request, 'board/comment_form.html', {
        'form' : form,
        }) # 포스트 요청이 아닐 경우 빈 폼으로 페이지 렌더링

@login_required
def comment_edit(request, comment_pk):
    # 해당 댓글 수정
    comment = get_object_or_404(BoardComment, pk=comment_pk) # 해당 댓글 인스턴스
    redirect_path = request.GET.get('next','') # 해당 컨텐츠로 리디렉션 하기위한 url_path

    if comment.user != request.user:
        messages.warning(request, '댓글 작성자만 수정할 수 있습니다.')
        return redirect(redirect_path)

    if request.method == 'POST':
        form = BoardCommentForm(request.POST, request.FILES, instance=comment)
        if form.is_valid():
            comment = form.save()
            messages.success(request, '기존 댓글을 수정했습니다.')
            return redirect(redirect_path)
    else:
        form = BoardCommentForm(instance=comment)
    return render(request, 'board/comment_form.html', {
        'form': form,
    })

@login_required
def comment_delete(request, comment_pk):
    # 해당 댓글 삭제
    comment = get_object_or_404(BoardComment, pk=comment_pk)
    redirect_path = request.GET.get('next','') # 해당 컨텐츠로 리디렉션 하기위한 url_path

    if comment.user != request.user:
        messages.warning(request, '댓글 작성자만 삭제할 수 있습니다.')
    else:
        comment.delete()
        messages.success(request, '댓글을 삭제했습니다.')
    return redirect(redirect_path)
