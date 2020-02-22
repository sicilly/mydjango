$(function () {
    const emptyMessage = '没有未读通知';
    const notice = $('#notifications');

    function CheckNotifications() {
        $.ajax({
            url: '/notifications/latest-notifications/',
            cache: false,
            success: function (data) {
                // 有通知就变红
                if (!data.includes(emptyMessage)) {
                    notice.addClass('btn-danger');
                }
            },
        });
    }

    CheckNotifications();  // 页面加载时执行

    function update_social_activity(id_value) {
        const newsToUpdate = $('[news-id=' + id_value + ']');
        $.ajax({
            url: '/news/update-interactions/',
            data: {'id_value': id_value},
            type: 'GET',
            cache: false,
            success: function (data) {
                $(".like-count", newsToUpdate).text(data.likes);
                $(".reply-count", newsToUpdate).text(data.replies);
            },
        });
    }

    notice.click(function () {
        if ($('.popover').is(':visible')) {
            notice.popover('hide');
            CheckNotifications();
        } else {
            notice.popover('dispose');
            $.ajax({
                url: '/notifications/latest-notifications/',
                cache: false,
                success: function (data) {
                    notice.popover({
                        html: true,         // 显示成html
                        trigger: 'focus',   // 点别处就折叠
                        container: 'body',
                        placement: 'bottom',
                        content: data,      // 弹出层的内容
                    });
                    notice.popover('show');
                    notice.removeClass('btn-danger')  // 移除红色
                },
            });
        }
        return false;  // 不是False
    });

    // WebSocket连接，使用wss(https)或者ws(http)
    const ws_scheme = window.location.protocol === "https:" ? "wss" : "ws";
    const ws_path = ws_scheme + "://" + window.location.host + "/ws/notification";
    // 新建WebSocket实例
    const ws = new ReconnectingWebSocket(ws_path);

    // 监听后端发送过来的消息
    ws.onmessage = function (event) {
        const data = JSON.parse(event.data);
        switch (data.key) {
            case "notification":
                if (currentUser !== data.actor_name) {  // 消息提示的发起者不提示
                    notice.addClass('btn-danger');
                }
                break;

            case "social_update":
                if (currentUser !== data.actor_name) {
                    notice.addClass('btn-danger');
                    update_social_activity(data.id_value);
                }
                break;

            case "additional_news":
                if (currentUser !== data.actor_name) {
                    // notice.addClass('btn-danger');
                    $('.stream-update').show();
                }
                break;

            default:
                console.log('error', data);
                break;
        }
    };
});
