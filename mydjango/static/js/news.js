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

    $('#newsFormModal').on('shown.bs.modal',function () {
        $('#newsInput').trigger('focus')    // 自动聚焦
    });

    //新增新闻动态
    $("#postNews").click(function () {
        if ($("#newsInput").val() === '') { //如果没有输入动态内容
            alert("请输入新闻动态的内容！");
            return;
        }
        if(currentUser===""){               //如果用户没有登陆
            alert("请登录后再发布新闻动态！")
            return;
        }else{                               //如果用户已登录
            // Ajax call after pushing button, to register a News object.
            $.ajax({
                url: '/news/post-news/',
                data: $("#postNewsForm").serialize(),
                type: 'POST',
                cache: false,
                success: function (data) {
                    $("ul.stream").prepend(data);
                    $("#newsInput").val("");
                    $("#newsFormModal").modal("hide");
                    // hide_stream_update();
                },
                error: function (data) {
                    alert(data.responseText);
                },
            });
        }
    });

    //点赞
    $("ul.stream").on("click", ".like", function () {
        let li = $(this).closest('li');
        let newsId = $(li).attr("news-id");
        let payload = {
            'newsId': newsId,
            'csrf_token': csrftoken
        };
        $.ajax({
            url: '/news/like/',
            data: payload,
            type: 'POST',
            cache: false,
            success: function (data) {
                $(".like .like-count", li).text(data.likers_count);
                if ($(".like .heart", li).hasClass("fa fa-heart")) {
                    $(".like .heart", li).removeClass("fa fa-heart");
                    $(".like .heart", li).addClass("fa fa-heart-o");
                } else {
                    $(".like .heart", li).removeClass("fa fa-heart-o");
                    $(".like .heart", li).addClass("fa fa-heart");
                }
            }
        });
    });

    //评论模态框
    $('#replyFormModal').on('show.bs.modal', function (event) {
        let button = $(event.relatedTarget); // Button that triggered the modal
        let recipient = button.data('who'); // Extract info from data-* attributes
        let newsid = button.data('newsid'); // Extract info from data-* attributes
        let modal = $(this);  //模态对话框
        modal.find('.modal-title').text('新的回复到： ' + recipient);
        modal.find('.modal-body input.recipient').val(recipient);
        modal.find('.modal-body input.newsid').val(newsid);
    });

    //发送回复内容
    $("#postReply").click(function () {
        //评论内容为空
        if ($("#reply-content").val() === '') {
            alert("请输入评论的内容！");
            return;
        }
        //用户未登录
        if (currentUser === "") {
            alert("请登录后再发布评论！");
        } else {
            // Ajax call after pushing button, to register a News object.
            $.ajax({
                url: '/news/post-reply/',
                data: $("#postReplyForm").serialize(),
                type: 'POST',
                cache: false,
                success: function (data) {
                    let li = $('[news-id=' + data.newsid + ']');  // 获得li
                    $(".reply .reply-count", li).text(data.replies_count);
                    $("#reply-content").val("");
                    $("#replyFormModal").modal("hide");
                    // hide_stream_update();
                },
                error: function (data) {
                    alert(data.responseText);
                },
            });
        }
    });

    // 获取评论列表
    $("ul.stream").on("click", ".reply", function () {
        let li = $(this).closest('li');
        let newsId = $(li).attr("news-id");
        $.ajax({
            url: '/news/get-replies/',
            data: {'newsId': newsId},
            cache: false,
            success: function (data) {
                $("#replyListModal .modal-body").html(data.replies_html);
            }
        });
    });
});
