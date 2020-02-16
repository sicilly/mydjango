from django.contrib import admin

from mydjango.chat.models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ['uuid_id', 'sender', 'reciever', 'message', 'unread']


admin.site.register(Message, MessageAdmin)
