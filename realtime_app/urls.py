from django.urls import path
from .views import chat_home, chat_room

urlpatterns = [
    path('chat/', chat_home, name='chat_home'),
    path('chat/<str:username>/', chat_room, name='chat_room'),
]
