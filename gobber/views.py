from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.db import connection
from django.contrib import messages

import random, time

from .models import Message, AccessKey
from .forms import MessageForm, AccessForm

def access(request):
    
    # Default value for session counter is set to 0 if none has been initliazed
    accessCount = request.session.setdefault('accessCount',0)

    if request.method == "POST":
        form = AccessForm(request.POST)
        #TODO: ihan bad practice att convert to string
        if (request.POST.get('key')==str(AccessKey.objects.first())):
            # Updating session key to allow access to /chats
            request.session['access'] = True
            request.session['accessCount'] = 0
            # Sleeping
            time.sleep(1)
            return HttpResponseRedirect(reverse('gobber:chats'))
        else:
            # Display failure message
            messages.error(request, random.choice(["Think ya can fool me?!","That's wrong, innit?", "GET OUTTA HERE YOU LIL' PRICK!", "Yer getting on me nerves!"]))
            request.session['accessCount'] += 1
            if accessCount > 2:
                time.sleep(5)
            return HttpResponseRedirect(reverse('gobber:access'))
    else:
        request.session['access'] = False
        form = AccessForm()
    return render(request, 'gobber/access.html', {'form':form})


    #use get_object_or_404()
    # message = get_object_or_404(Message, pk=message_id)
    # try:
    #     selected_choice = message.choice_set.get(pk=request.POST['choice'])
    # except (KeyError, Choice.DoesNotExist):
    #     return render(request, 'gobber/detail.html', {'message':message, 'error_message': "Select a CHOICE stuoidass"})

def chats(request):

    # If no access variable is found, the value is set to False
    access = request.session.get('access','False')

    if access == True:

        # FLAWED: 
        query = 'SELECT * FROM gobber_message ORDER BY pub_date DESC LIMIT 12'
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
                messages.error(request, "NO SPECIAL CHARACTERS ALLOWED")
            cursor.close()
            return HttpResponseRedirect(reverse('gobber:chats'))
        else:
            form = MessageForm()

        return render(request, 'gobber/chats.html', {'messageList':messageList,'form': form})

        # SECURITY FIX:

        # messageList = Message.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:12]

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
