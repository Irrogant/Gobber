from unittest.util import _MAX_LENGTH
from django.utils import timezone
import datetime
from django.db import models

class Message(models.Model):
    message_text = models.CharField(max_length=300)
    # Publish date is set automatically when the message is saved
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class AccessKey(models.Model):
    key = models.CharField(max_length=10)

    #TODO prob should not exist
    def __str__(self):
        return self.key 