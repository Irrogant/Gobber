from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Message
from .forms import MessageForm

class IndexView(generic.ListView):
    #context_object_name provides which name to use for the list in the chosen template html
    template_name = 'gobber/index.html'
    context_object_name = 'latest_message_list'

    def get_queryset(self):
        #return Message.objects.order_by('-pub_date')[:5]
        return Message.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Message
    template_name = 'gobber/detail.html'
    
    def get_queryset(self):
        #TODO VULNERABILITY! remove access
        return Message.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DeleteView):
    model = Message
    template_name = 'gobber/results.html'


#update 'chats' name to gobber, addChats becomes /chats

def accessChat(reqest):

    #ask for password

    #if password == correct
        #return gobbler/chats

    #else
        #return to same page, display OHNONO-message

    return

def addChat(request):
    print('post data is:', request.POST)
    messageList = Message.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:7]
    
    if request.method == "POST":
        #takes in form data and checks if it is valid
        form = MessageForm(request.POST)
        if form.is_valid():
            #save to DB
            #message = form.save()
            #message.pub_date = timezone.now()
            form.save()
            #refresh page
            return HttpResponseRedirect(reverse('gobber:addChat'))
    else:
        form = MessageForm()
    return render(request, 'gobber/index.html', {'messageList':messageList,'form': form})


def vote(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    try:
        selected_choice = message.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'gobber/detail.html', {'message':message, 'error_message': "Select a CHOICE stuoidass"})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('gobber:results',args=(message.id,)))
