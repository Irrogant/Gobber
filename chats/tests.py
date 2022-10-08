import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Message

def create_message(message_text, days):
    time = timezone.now() + datetime.timedelta(days=days) 
    return Message.objects.create(message_text=message_text, pub_date=time)

class MessageModelTests(TestCase):

    def test_no_future_messages(self):
        #Future messages do not shoe
        time = timezone.now() + datetime.timedelta(days=30)
        future_message = Message(pub_date=time)
        self.assertIs(future_message.was_published_recently(), False)

    def test_published_recently_old(self):
        #Old messages do not show
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_message = Message(pub_date=time)
        self.assertIs(old_message.was_published_recently(), False)

    def test_published_recently_recent(self):
        #Recent messages show
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_message = Message(pub_date=time)
        self.assertIs(recent_message.was_published_recently(), True)

class MessageIndexViewTests(TestCase):
    def test_no_messages(self):
        response = self.client.get(reverse('chats:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No chats are available.")
        self.assertQuerysetEqual(response.context['latest_message_list'], [])

    def test_past_message(self):
        past_message = create_message(message_text='Past Message.', days=-5)
        url = reverse('chats:detail', args=(past_message.id,))
        response = self.client.get(url)
        self.assertContains(response, past_message.message_text)

    def test_future_message(self):
        future_message = create_message(message_text='Future message.', days=5)
        url = reverse('chats:detail', args=(future_message.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def test_future_message_and_past_message(self):
        create_message(message_text="Past message.", days=-30)
        create_message(message_text="Future message.", days=30)
        response = self.client.get(reverse('chats:index'))
        self.assertQuerysetEqual(response.context['latest_message_list'], ['<Message: Past message.>'])

