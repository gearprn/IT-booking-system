from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages import error
from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount

import datetime
from mainapp.models import Room, Booking, Student, RoomType_Facility

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

    return render(request, template_name='index.html', context=context)

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

def search(request):
    context = {}
    search = request.GET.get('search', '')

    if search != '':
        rooms = Room.objects.filter(name__icontains=search)
        context['search'] = search
        context['rooms'] = rooms
        
    return render(request, template_name='search.html', context=context)

def book(request, roomId):
    context = {}

    # get specific room for booking
    room = Room.objects.get(id=roomId)
    facility = RoomType_Facility.objects.filter(roomType_id=room.roomType.id)
    
    context['room'] = room
    context['facilities'] = facility

    if request.user.is_authenticated:
        student = Student.objects.get(user_id=request.user.id)
        context['student'] = student
    

    return render(request, template_name='booking.html', context=context)

@login_required(redirect_field_name="index")
def createBook(request, roomId):
    context = {}

    # todat dateobject
    today = datetime.datetime.now().date()

    # request dateobject
    startDate = datetime.datetime.strptime(request.POST.get('startDate'), '%Y-%m-%d').date()
    endDate = datetime.datetime.strptime(request.POST.get('endDate'), '%Y-%m-%d').date()

    # request timeobject
    # startTime = datetime.datetime
    # endTime = datetime.datetime
    print(request.POST.get('startTime'))

    # if request date is past date or end date less than start date
    if (startDate < today) or (endDate < today) or (today < startDate):
        error(request, 'กรุณาใส่วันให้ถูกต้อง')
        return redirect('/book/'+str(roomId))

    # booking = Booking.objects.create(
    #     # request data
    #     title = request.POST.get('title'),
    #     purpose = request.POST.get('purpose'),
        
    #     # time data
    #     startDate = request.POST.get('startDate'),
    #     endDate = request.POST.get('endDate'),
    #     startTime = request.POST.get('startTime'),
    #     endTime = request.POST.get('endTime'),
    #     bookDate = datetime.datetime.now(),
        
    #     # user that curently signed in data (maybe not the booker himself)
    #     bookBy_id = request.user.id,

    #     # booker data
    #     bookerFirstName = request.POST.get('name'),
    #     bookerLastName = request.POST.get('lastname'),
    #     bookerStudentId = request.POST.get('sid'),
    #     bookerYear = request.POST.get('year'),
    #     bookerBranch = request.POST.get('branch'),
    # )
    return redirect('index')

def profile(request):
    context = {}

    # get user
    user = User.objects.get(id= request.user.id)
    context['user'] = user

    # get student data
    studentId = Student.objects.get(user_id=request.user.id)
    context['studentId'] = studentId

    # get image profile
    socialAccount = SocialAccount.objects.get(user_id=request.user.id)
    context['socialAccount'] =socialAccount

    booking = Booking.objects.filter(bookBy_id=request.user.id)
    context['booking'] =booking

    track = Booking.objects.filter(bookBy_id=request.user.id)
    context['track'] =track

    return render(request, template_name='profile.html', context=context)
