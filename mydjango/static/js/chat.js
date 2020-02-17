$(function () {

    // 滚动条下拉到底
    function scrollConversationScreen() {
        $("input[name='msgcontent']").focus();
        $('.messages-list').scrollTop($('.messages-list')[0].scrollHeight);
    }

    // AJAX POST发送消息
    $("#send").submit(function () {
        $.ajax({
            url: '/chat/send-message/',
            data: $("#send").serialize(),
            cache: false,
            type: 'POST',
            success: function (data) {
                $(".send-message").before(data);  // 将接收到的消息插入到聊天框
                $("input[name='msgcontent']").val(''); // 消息发送框置为空
                scrollConversationScreen();  // 滚动条下拉到底
            }
        });
        return false;
    });
});


