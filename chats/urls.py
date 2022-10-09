from django.urls import path

from . import views

app_name = 'chats'

urlpatterns = [

    #funkar för att display messages
    #path('', views.IndexView.as_view(), name='index'),

    #funkar för att put to database
    path('', views.addChat, name='addChat'),

    #add login path
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:message_id>/vote/', views.vote, name='vote'),
]