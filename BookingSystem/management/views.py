from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.template.context_processors import request


import datetime
from mainapp.models import (Booking, Facility, Room, RoomType, RoomType_Facility, Student)

# Create your views here.

def adminSignIn(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('/management/request')
        else:
            return redirect('index')

    return render(request, template_name='signin.html')

@login_required(login_url='/management/')
@permission_required('is_staff', login_url='/management/')
def request(request):
    context = {}

    allreq = Booking.objects.all()
    context['allreq'] = allreq

    return render(request, template_name='request.html', context=context)

@login_required(login_url='/management/')
@permission_required('is_staff', login_url='/management/')
def detail(request, detail_id):
    context = {}

    detail = Booking.objects.get(id= detail_id)
    context['detail'] = detail

    return render(request, template_name='detail.html', context=context)

@login_required(login_url='/management/')
@permission_required('is_staff', login_url='/management/')
def createroom(request):
    user = request.user.id
    context = {}
    allType = RoomType.objects.all()
    context['allType'] = allType

    if request.method == 'POST':
        roomName = request.POST.get('name')
        roomType = request.POST.get('roomType_id')
        roomLocation = request.POST.get('location')
        roomSize = request.POST.get('size')
        roomStatus = request.POST.get('availableStatus')
        roomPhoto = request.FILES.get('photo')
            
        addRoom = Room.objects.create(name=roomName, location=roomLocation, availableStatus='AVAILABLE', size=roomSize, photo=roomPhoto, roomType_id=roomType)
        return redirect('allRoom')

    return render(request, template_name='createroom.html', context=context)

@login_required(login_url='/management/')
@permission_required('is_staff', login_url='/management/')
def addfacility(request):
    user = request.user.id
    if request.method == 'POST':
        facilityName = request.POST.get('name')
        facilityDesc = request.POST.get('description')

        addFacility = Facility.objects.create(name=facilityName, description=facilityDesc)
        return redirect('allfacility')

    return render(request, template_name='createfacility.html')

@login_required(login_url='/management/')
@permission_required('is_staff', login_url='/management/')
def addRoomtype(request):
    user = request.user.id
    if request.method == 'POST':
        roomType = request.POST.get('typeTitle')
    
        addType = RoomType.objects.create(typeTitle=roomType)
        return redirect('allRoomType')

    return render(request, template_name='createtype.html')

@login_required(login_url='/management/')
@permission_required('is_staff', login_url='/management/')
def deleteRoom(request, room_id):
    delRoom = Room.objects.get(pk= room_id)
    delRoom.delete()

    return redirect('allRoom')

@login_required(login_url='/management/')
@permission_required('is_staff', login_url='/management/')
def deleteRoomType(request, roomType_id):
    delRoomType = RoomType.objects.get(pk= roomType_id)
    delRoomType.delete()

    return redirect('allRoomType')

@login_required(login_url='/management/')
@permission_required('is_staff', login_url='/management/')
def deleteFacility(request, facility_id):
    delFacility = Facility.objects.get(pk= facility_id)
    delFacility.delete()

    return redirect('allfacility')

@login_required(login_url='/management/')
@permission_required('is_staff', login_url='/management/')
def allRoom(request):
    context = {}
    # get allroom
    rooms = Room.objects.all()
    context['rooms'] = rooms
    return render(request, template_name='allroom.html', context= context)

@login_required(login_url='/management/')
@permission_required('is_staff', login_url='/management/')
def allRoomType(request):
    context = {}
    # get allroomtype
    types = RoomType.objects.all()
    context['types'] =  types
    return render(request, template_name='alltype.html', context= context)

@login_required(login_url='/management/')
@permission_required('is_staff', login_url='/management/')
def allfacility(request):
    context = {}
    # get allroomtype
    facilities = Facility.objects.all()
    context['facilities'] =  facilities
    return render(request, template_name='allfacility.html', context= context)
