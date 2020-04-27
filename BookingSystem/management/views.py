from django.shortcuts import render
from django.contrib.auth.models import User
import datetime
from mainapp.models import Room, Booking, Student, RoomType_Facility
# Create your views here.

def request(request):
    context = {}

    allreq = Booking.objects.all()
    context['allreq'] = allreq

    return render(request, template_name='request.html', context=context)

def detail(request, detail_id):
    context = {}
    detail = User.objects.get(id= detail_id)
    context['detail'] = detail

    return render(request, template_name='detail.html', context=context)