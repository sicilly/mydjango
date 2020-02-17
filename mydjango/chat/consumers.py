import json

from channels.generic.websocket import AsyncWebsocketConsumer


class MessageConsumer(AsyncWebsocketConsumer):
    """处理聊天应用中的WebSocket请求"""
    async def connect(self):
        if self.scope['user'].is_anonymous:
            await self.close()  # 未登录用户直接断开连接
        else:
            await self.channel_layer.group_add(self.scope['user'].username, self.channel_name)
            await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        """接收聊天信息"""
        await self.send(text_data=json.dumps(text_data))

    async def disconnect(self, code):
        """离开聊天组"""
        await self.channel_layer.group_discard(self.scope['user'].username, self.channel_name)
