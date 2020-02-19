# from channels.auth import AuthMiddlewareStack
# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.security.websocket import AllowedHostsOriginValidator
# from django.urls import path
# from chat.consumers import MessagesConsumer
#
#
# # self.scope['type']获取协议类型
# application = ProtocolTypeRouter({
#     'websocket': AllowedHostsOriginValidator(
#         AuthMiddlewareStack(
#             URLRouter([
#                 path('ws/<str:username>/', MessagesConsumer),
#             ])
#         )
#     )
# })
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path

from mydjango.chat.consumers import MessagesConsumer

# self.scope['type']获取协议类型
# self.scope['url_route']['kwargs']['username']获取url中关键字参数
# channels routing是scope级别的，一个连接只能由一个consumer接收和处理


application = ProtocolTypeRouter({
    # 普通的HTTP请求不需要我们手动在这里添加，框架会自动加载
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path('ws/<str:username>/', MessagesConsumer),
            ])
        )
    )
})
