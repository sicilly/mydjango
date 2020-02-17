from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path
from chat.consumers import MessageConsumer


# self.scope['type']获取协议类型
application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                path('ws/<str:username>/', MessageConsumer)
            )
        )
    )
})
