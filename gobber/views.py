from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Message, AccessKey
from .forms import MessageForm, AccessForm

class IndexView(generic.ListView):
    #context_object_name provides which name to use for the list in the chosen template html
    template_name = 'gobber/chats.html'
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

def access(request):
    if request.method == "POST":
        form = AccessForm(request.POST)
        print('posted:', request.POST.get('key'))
        print('key', str(AccessKey.objects.first()))
        
        #TODO: ihan bad practice att convert to string
        if (request.POST.get('key')==str(AccessKey.objects.first())):
            # make variable to access granted
            request.session['access'] = True
            return HttpResponseRedirect(reverse('gobber:chats'))
        else:
            print('fail')
            return HttpResponseRedirect(reverse('gobber:access'))
    else:
        #TODO display OHNONONO message
        request.session['access'] = False
        form = AccessForm()
    return render(request, 'gobber/access.html', {'form':form})

def chats(request):
    print('post data is:', request.POST)
    print('uägh', request.POST.get('message_text'))

    # Session variable cannot be modified by user
    access = request.session.get('access','false')

    if access:
        messageList = Message.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:7]
        
        if request.method == "POST":
            #takes in form data and checks if it is valid
            form = MessageForm(request.POST)
            #TODO: what if invalid
            if form.is_valid():
                # Save to DB

                form.save()
                # Refresh page
                return HttpResponseRedirect(reverse('gobber:chats'))
        else:
            form = MessageForm()
        return render(request, 'gobber/chats.html', {'messageList':messageList,'form': form})
    
    else:
       return HttpResponseRedirect(reverse('gobber:access'))

    


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
