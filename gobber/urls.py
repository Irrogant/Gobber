from django.urls import path

from . import views

app_name = 'gobber'

urlpatterns = [

    # Accessing chats
    path('', views.access, name='access'),
    path('access/', views.access, name='access'),

    # Main view for chats
    path('chats/', views.chats, name='chats'),

    #add login path
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:message_id>/vote/', views.vote, name='vote'),
]