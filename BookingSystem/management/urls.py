from django.urls import path
from . import views

urlpatterns = [
    path('request', views.request, name='request'),
    path('<int:detail_id>', views.detail, name='detail'),
]