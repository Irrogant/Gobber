from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.db import connection

from .models import Message, AccessKey
from .forms import MessageForm, AccessForm

def access(request):
    if request.method == "POST":
        form = AccessForm(request.POST)
        print('posted:', request.POST.get('key'))
        print('key', str(AccessKey.objects.first()))
        
        #TODO: ihan bad practice att convert to string
        if (request.POST.get('key')==str(AccessKey.objects.first())):
            # Updating session key to allow access to /chats
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


    #use get_object_or_404(?
    # message = get_object_or_404(Message, pk=message_id)
    # try:
    #     selected_choice = message.choice_set.get(pk=request.POST['choice'])
    # except (KeyError, Choice.DoesNotExist):
    #     return render(request, 'gobber/detail.html', {'message':message, 'error_message': "Select a CHOICE stuoidass"})

def chats(request):

    # Session variable cannot be modified by user
    access = request.session.get('access','False')

    if access == True:

        # FLAWED: 
        query = 'SELECT * FROM gobber_message ORDER BY pub_date DESC LIMIT 7'
        messageList = Message.objects.raw(query)

        if request.method == "POST":

            cursor = connection.cursor()
            form = MessageForm(request.POST)
            messageText = (Message(message_text=request.POST.get('message_text')))
            messageDate = timezone.now()
            query2 = "INSERT INTO gobber_message (message_text, pub_date) VALUES ('%s','%s')" % (messageText, messageDate)
            try: 
                cursor.execute(query2)
            except:
                print('NO SPECIAL CHARACTERS')
            cursor.close()
            return HttpResponseRedirect(reverse('gobber:chats'))
        else:
            form = MessageForm()

        return render(request, 'gobber/chats.html', {'messageList':messageList,'form': form})

        # SECURITY FIX:

        # messageList = Message.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:7]

        # if request.method == "POST":
        #     form = MessageForm(request.POST)
        #     if form.is_valid():
        #         # Save to DB
        #         form.save()
        #         # Refresh page
        #         return HttpResponseRedirect(reverse('gobber:chats'))
        # else:
        #     form = MessageForm()

        # return render(request, 'gobber/chats.html', {'messageList':messageList,'form': form})

    else:
       return HttpResponseRedirect(reverse('gobber:access'))
