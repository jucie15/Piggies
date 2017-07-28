$('.comment-emo-btn').click(function(){

    var emotion_name = $(this).attr('value'); // 클릭한 요소의 attribute 중 value의 값을 가져온다.
    var comment_pk = $(this).attr('id');

    $.ajax({
        url: "/cast/comment-emotion/"+comment_pk+"/?emotion_name=" + emotion_name, // 통신할 url을 지정한다.
        data: {'csrfmiddlewaretoken': '{{ csrf_token }}'}, // 서버로 데이터를 전송할 때 이 옵션을 사용한다.
        dataType: "json", // 서버측에서 전송한 데이터를 어떤 형식의 데이터로서 해석할 것인가를 지정한다. 없으면 알아서 판단한다.

        success: function(res){
            // 요청이 성공했을 경우 눌려있는 버튼 모양을 바꿔준다.
            $('#comment-like-count-' + comment_pk).text(res.like_number)
            $('#comment-dislike-count-' + comment_pk).text(res.dislike_number)
        },
        error: function(error){
            console.log(error)
            // 요청이 실패했을 경우
        }
    });
});
