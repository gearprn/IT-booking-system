from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/<int:roomId>', views.book, name="book"),
    path('book/schedule/', views.schedule, name="schedule"),
    path('createbook/<int:roomId>', views.createBook, name="createBook"),
    path('profile/', views.profile, name="profile"),
    path('search/', views.search, name="search"),
    path('room/status/', views.roomStatus, name="roomStatus")
]