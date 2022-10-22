from django.contrib import admin
from .models import Message, AccessKey


class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_text', 'pub_date')
    list_filter = ['pub_date']
    search_fields = ['message_text']

class AccessKeyAdmin(admin.ModelAdmin):
    model = AccessKey
    fieldsets = [
        ('Key',      {'fields': ['key']}),
    ]


admin.site.register(Message, MessageAdmin)
admin.site.register(AccessKey)