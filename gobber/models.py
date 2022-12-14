from django.db import models

class Message(models.Model):
    message_text = models.CharField(max_length=300)
    # Publish date is set automatically when the message is saved
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message_text

class AccessKey(models.Model):
    key = models.CharField(max_length=10)

    def __str__(self):
        return self.key 