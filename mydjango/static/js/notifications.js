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

});
