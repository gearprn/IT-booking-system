from django.contrib.auth import logout
from django.shortcuts import render, redirect
from mainapp.models import Room, Booking, Student, RoomType_Facility
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

import datetime 

# Create your views here.

@login_required
def sign_out(request):
    """ sign user out and redirect to index.html  """
    logout(request)
    return redirect('index')

def index(request):
    context = {}

    # get all room
    rooms = Room.objects.all()
    context['rooms'] = rooms

    if request.user.is_authenticated:
        print('Authenticated.')
        stdId = request.user.email.split('@')[0]
        student = Student.objects.filter(studentId=stdId)

        # do noting if already create object
        if student.exists():
            pass

        # create new object after first time sign in
        else:
            if stdId.isdigit():
                print('User\'s student')
                year = ((datetime.datetime.now().year + 543) % 100) - int(stdId[0:2])
                year = 1 if year == 0 else year
                print(year, stdId)
                std = Student.objects.create(
                    user_id = request.user.id,
                    year = year,
                    studentId = stdId
                )
            else:
                # do nothing
                print('User\'s personnel')
        
        return render(request, template_name='index.html', context=context)

    # user is unauthenticated
    else:
        print('unauthenticated')
        return render(request, template_name='index.html', context=context)

def book(request, roomId):
    context = {}

    # get specific room for booking
    room = Room.objects.get(id=roomId)
    facility = RoomType_Facility.objects.filter(roomType_id=room.roomType.id)

    context['room'] = room
    context['facilities'] = facility

    return render(request, template_name='booking.html', context=context)

@login_required(redirect_field_name="index")
def createBook(request, roomId):
    context = {}

    booking = Booking.objects.create(
        # request data
        title = request.POST.get('title'),
        purpose = request.POST.get('purpose'),
        
        # time data
        startDate = request.POST.get('startDate'),
        endDate = request.POST.get('endDate'),
        startTime = request.POST.get('startTime'),
        endTime = request.POST.get('endTime'),
        bookDate = datetime.datetime.now(),
        
        # booker date
        bookBy_id = request.user.id
    )
    return redirect('index')

def profile(request):
    context = {}
    # user = User.objects.get(id= 1)
    user = User.objects.get(id= request.user.id)
    context['user'] = user
    
    return render(request, template_name='profile.html', context=context)
