from django.contrib import admin
from .models import Choice, Message, AccessKey

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class MessageAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,      {'fields': ['message_text']}),
        ('Dates',   {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
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