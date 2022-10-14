from django.urls import path

from . import views

app_name = 'gobber'

urlpatterns = [

    # Accessing chats
    path('', views.access, name='access'),

    # Main view for chats
    path('chats/', views.chats, name='chats'),
]