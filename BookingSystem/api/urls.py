from django.urls import path

from . import views

urlpatterns = [
    path('add/roomtype-facility', views.addNewFacility, name='addNewFacility'),
    path('remove/roomtype-facility', views.removeFacility, name='removeFacility'),
]