from django.shortcuts import render
from mainapp.models import Room

# Create your views here.

def index(request):
    context = {}

    # get all room
    rooms = Room.objects.all()
    context['rooms'] = rooms

    return render(request, template_name='index.html', context=context)

def book(request, roomId):
    context = {}

    # get specific room for booking
    room = Room.objects.get(id=roomId)
    context['room'] = room

    return render(request, template_name='booking.html', context=context)

    
