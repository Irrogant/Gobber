from django.contrib import admin
from .models import Message, AccessKey


class MessageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,      {'fields': ['message_text']}),
        ('Dates',   {'fields': ['pub_date']}),
    ]
    list_display = ('message_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['message_text']

class AccessKeyAdmin(admin.ModelAdmin):
    model = AccessKey
    fieldsets = [
        ('Key',      {'fields': ['key']}),
    ]


admin.site.register(Message, MessageAdmin)
admin.site.register(AccessKey)