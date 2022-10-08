from django.urls import path

from . import views

app_name = 'chats'

urlpatterns = [

    #ongelma: två views om båda vill visas, men kan bara visa en
    #funkar för att display messages
    #path('', views.IndexView.as_view(), name='index'),

    #funkar för att put to database
    path('', views.addChat, name='addChat'),

    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:message_id>/vote/', views.vote, name='vote'),
]

#current ongelma: current fiels used for writing messeage does
#not update database