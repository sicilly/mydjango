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


    // WebSocket连接，使用wss(https)或者ws(http)
    const ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
    const ws_path = ws_scheme + "://" + window.location.host + "/ws/" + active_user + "/";
    // 新建WebSocket实例
    const ws = new ReconnectingWebSocket(ws_path);
    //监听后端发送过来的消息
    ws.onmessage = function (event) {
        // 后端传过来是字典，要反序列化
        const data = JSON.parse(event.data);
        if(data.sender === active_user){  // 发送者为当前选中的用户
            $(".send-message").before(data.message)  // 将接收到的消息插入到聊天框
            scrollConversationScreen();  // 滚动条下拉到底
        }
    }
});


