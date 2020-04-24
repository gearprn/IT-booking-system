from django.shortcuts import render, redirect
from mainapp.models import Room, Booking
from datetime import date

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

def createBook(request, roomId):
    context = {}

    booking = Booking.objects.create(
        title = request.POST.get('title'),
        purpose = request.POST.get('purpose'),
        
        startDate = request.POST.get('startDate'),
        endDate = request.POST.get('endDate'),
        startTime = request.POST.get('startTime'),
        endTime = request.POST.get('endTime'),

        bookDate = date.today(),
        
        bookBy_id = 1
    )
    return redirect('index')

    
