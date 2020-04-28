from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages import error
from django.shortcuts import render, redirect
from allauth.socialaccount.models import SocialAccount

import datetime
from mainapp.models import Room, Booking, Student, RoomType_Facility, Approve

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
    search = request.GET.get('search', '') # ดึงข้อมูลจากช่องค้นหา

    if search != '': 
        rooms = Room.objects.filter(name__icontains=search) # filter search name
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
    startTime = datetime.datetime.strptime(request.POST.get('startTime'), '%H:%M').time()
    endTime = datetime.datetime.strptime(request.POST.get('endTime'), '%H:%M').time()

    # if request date is past date or end date less than start date
    if (startDate < today) or (endDate < today) or (endDate < startDate):
        error(request, 'กรุณาใส่วันให้ถูกต้อง')
        return redirect('/book/'+str(roomId))

    # start time can't be less than end time
    if (endTime < startTime):
        error(request, 'กรุณาใส่เวลาให้ถูกต้อง')
        return redirect('/book/'+str(roomId))

    # if make to this past mean no error
    approve = Approve.objects.create(
        result = 'PENDING'
    )

    booking = Booking.objects.create(
        # request data
        title = request.POST.get('title'),
        purpose = request.POST.get('purpose'),
        room_id = roomId,
        approve = approve, # this approve is still don't have date, approve_by
        
        # time data
        startDate = request.POST.get('startDate'),
        endDate = request.POST.get('endDate'),
        startTime = request.POST.get('startTime'),
        endTime = request.POST.get('endTime'),
        bookDate = datetime.datetime.now(),
        
        # user that curently signed in data (maybe not the booker himself)
        bookBy_id = request.user.id,

        # booker data
        bookerFirstName = request.POST.get('name'),
        bookerLastName = request.POST.get('lastname'),
        bookerStudentId = request.POST.get('sid'),
        bookerYear = request.POST.get('year'),
        bookerBranch = request.POST.get('branch'),
    )
    return redirect('profile')

def profile(request):
    context = {}
    # เป็นการดึงข้อมูลจากโมเดลในฐานข้อมูล
    # ผู้ใช้งาน
    user = User.objects.get(id= request.user.id)
    context['user'] = user

    # รหัสนักศึกษา
    studentId = Student.objects.get(user_id=request.user.id)
    context['studentId'] = studentId

    # รูปแอคเคาท์
    socialAccount = SocialAccount.objects.get(user_id=request.user.id)
    context['socialAccount'] =socialAccount

    # ดึงประวัติการจอง ex วันที่ทำการจอง
    booking = Booking.objects.filter(bookBy_id=request.user.id)
    context['booking'] =booking

    # แขนงการเรียน
    track = Booking.objects.filter(bookBy_id=request.user.id)
    context['track'] =track

    return render(request, template_name='profile.html', context=context)
