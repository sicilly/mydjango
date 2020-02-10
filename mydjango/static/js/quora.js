$(function () {
    //从 cookie 里面获取 csrftoken
    let csrftoken = getCookie('csrftoken');

    // 这个设置会让所有Ajax POST/DELETE请求在其请求头中都携带 X-CSRFToken 信息
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $(".question-vote").click(function () {
        let span = $(this);
        let questionId = $(this).closest(".question").attr("question-id");
        let vote = null;
        if ($(this).hasClass("up-vote")) {
            vote = "U";
        } else {
            vote = "D";
        }
        $.ajax({
            url: '/quora/question/vote/',
            data: {
                'questionId': questionId,
                'value': vote
            },
            type: 'post',
            cache: false,
            success: function (data) {
                $('.vote', span).removeClass('voted');
                if (vote === "U") {
                    $(span).addClass('voted');
                }
                if (vote === "D") {
                    $(span).addClass('voted');
                }
                $("#questionVotes").text(data.votes);
            }
        });
    });

    $(".answer-vote").click(function () {
        // Vote on an answer.
        let span = $(this);
        let answerId = $(this).closest(".answer").attr("answer-id");
        vote = null;
        if ($(this).hasClass("up-vote")) {
            vote = "U";
        } else {
            vote = "D";
        }
        $.ajax({
            url: '/quora/answer/vote/',
            data: {
                'answerId': answerId,
                'value': vote
            },
            type: 'post',
            cache: false,
            success: function (data) {
                $('.vote', span).removeClass('voted');
                if (vote === "U") {
                    $(span).addClass('voted');
                }
                if (vote === "D") {
                    $(span).addClass('voted');
                }
                $("#answerVotes-"+answerId).text(data.votes);
            }
        });
    });

    $(".acceptAnswer").click(function () {
        // Mark an answer as accepted.
        var span = $(this);
        var answerId = $(this).closest(".answer").attr("answer-id");
        $.ajax({
            url: '/quora/accept-answer/',
            data: {
                'answerId': answerId
            },
            type: 'post',
            cache: false,
            success: function (data) {
                $("#acceptAnswer-"+answerId).removeClass("accepted");
                $("#acceptAnswer-"+answerId).prop("title", "点击接受回答");
                $("#acceptAnswer-"+answerId).addClass("accepted");
                $("#acceptAnswer-"+answerId).prop("title", "该回答已被采纳");
            }
        });
    });

});
