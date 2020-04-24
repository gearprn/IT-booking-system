from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('book/<int:roomId>', views.book, name="book"),
    path('createbook/<int:roomId>', views.createBook, name="createBook")
]