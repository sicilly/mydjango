$(function () {
    $('#newsFormModal').on('shown.bs.modal',function () {
        $('#newsInput').trigger('focus')    // 自动聚焦
    });

    $("#postNews").click(function () {
        if(currentUser===""){   //如果用户没有登陆
            alert("请登录后再发布新闻动态！")
            return;
        }else{                  //如果用户已登录
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
    })
})
