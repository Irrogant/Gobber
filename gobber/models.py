from unittest.util import _MAX_LENGTH
from django.utils import timezone
import datetime
from django.db import models

class Message(models.Model):
    message_text = models.CharField(max_length=300)
    #Publish date is set automatically when the message is saved
    pub_date = models.DateTimeField(auto_now=True)
    #pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.message_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Choice(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class AccessKey(models.Model):
    key = models.CharField(max_length=10)

    def __str__(self):
        return self.key 
    #TODO: lägga __str här = flaw? cus then can see key