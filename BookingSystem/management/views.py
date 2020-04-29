from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.template.context_processors import request

import datetime
from mainapp.models import (Booking, Facility, Room, RoomType, RoomType_Facility, Student, Approve)

# Create your views here.

def adminSignIn(request):
    context = {}
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('/management/request')
        else:
            context['error'] = 'username หรือ password ไม่ถูกต้อง'
            return render(request, template_name='signin.html', context=context)

    return render(request, template_name='signin.html', context=context)

# คำร้องขอทั้งหมด
@login_required(login_url='/management/')
@permission_required('is_staff', login_url='/management/')
def request(request):
    context = {}

    allreq = Booking.objects.filter(approve__result="PENDING")
    context['allreq'] = allreq
    return render(request, template_name='request.html', context=context)

# ดูประวัติที่เคยอนุมัติ
@login_required(login_url='/management/')
@permission_required('is_staff', login_url='/management/')
def myApprove(request):
    context = {}

    myApproval = Booking.objects.filter(approve__approveBy_id=request.user.id)
    context['myApproval'] = myApproval

    return render(request, template_name="myApproval.html", context=context)

# รายละเอียดทั้งหมด
@login_required(login_url='/management/')
@permission_required('is_staff', login_url='/management/')
def detail(request, detail_id):
    context = {}

    detail = Booking.objects.get(id= detail_id)
    context['detail'] = detail
    return render(request, template_name='detail.html', context=context)

# เพิ่มสถานที่
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

# เพิ่มสิ่งอำนวยความสะดวก
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

# เพิ่มประเภทห้อง
@login_required(login_url='/management/')
@permission_required('is_staff', login_url='/management/')
def addRoomtype(request):
    user = request.user.id
    if request.method == 'POST':
        roomType = request.POST.get('typeTitle')
    
        addType = RoomType.objects.create(typeTitle=roomType)
        return redirect('allRoomType')

    return render(request, template_name='createtype.html')

# ลบสถานที่/ห้อง
@login_required(login_url='/management/')
@permission_required('is_staff', login_url='/management/')
def deleteRoom(request, room_id):
    delRoom = Room.objects.get(pk= room_id)
    delRoom.delete()

    return redirect('allRoom')

# ลบประเภทของห้อง
@login_required(login_url='/management/')
@permission_required('is_staff', login_url='/management/')
def deleteRoomType(request, roomType_id):
    delRoomType = RoomType.objects.get(pk= roomType_id)
    delRoomType.delete()

    return redirect('allRoomType')

# ลบสิ่งอำนวยความสะดวก
@login_required(login_url='/management/')
@permission_required('is_staff', login_url='/management/')
def deleteFacility(request, facility_id):
    delFacility = Facility.objects.get(pk= facility_id)
    delFacility.delete()

    return redirect('allfacility')

# get allroom
@login_required(login_url='/management/')
@permission_required('is_staff', login_url='/management/')
def allRoom(request):
    context = {}
    
    rooms = Room.objects.all()
    context['rooms'] = rooms
    return render(request, template_name='allroom.html', context= context)

# get allroomtype
@login_required(login_url='/management/')
@permission_required('is_staff', login_url='/management/')
def allRoomType(request):
    context = {}
    
    types = RoomType.objects.all()
    context['types'] =  types
    return render(request, template_name='alltype.html', context= context)

# get allfacility
@login_required(login_url='/management/')
@permission_required('is_staff', login_url='/management/')
def allfacility(request):
    context = {}
    
    facilities = Facility.objects.all()
    context['facilities'] =  facilities
    return render(request, template_name='allfacility.html', context= context)

# การอนุมัติ/ไม่อนุมัติให้ใช้สถานที่
@login_required(login_url='/management/')
@permission_required('is_staff', login_url='/management/')
def btnApprove(request, bookBy_id):
    bookingStatus = Booking.objects.get(id=bookBy_id)
    approve = Approve.objects.get(id=bookingStatus.approve_id)

    # เก็บว่าใครเป็นคนอนุมัติเเละเวลาไหน
    approve.date = datetime.datetime.now()
    approve.approveBy_id = request.user.id
    approve.result = 'APPROVED'
    approve.save()

    return redirect('/management/request')

# เเก้ไขสถานที่
@login_required(login_url='/management/')
@permission_required('is_staff', login_url='/management/')
def editRoom(request, roomId):
    context = {}
    room = Room.objects.get(id=roomId)
    context['room'] = room

    allType = RoomType.objects.all()
    context['allType'] = allType

    photo = request.FILES.get('photo', '')
    
    # roomName = Room.objects.filter(name=request.POST.get('name'))

    if request.method == 'POST':
        room.name = request.POST.get('name')
        room.location = request.POST.get('location')
        room.roomType_id = request.POST.get('roomType_id')
        room.size = request.POST.get('size')
        room.photo = room.photo if photo == '' else photo
        room.save()
        return redirect('/management/allRoom')

    # elif request.method == 'POST' and roomName.exists() == True:
    #     context['error'] = "ชื่อสถานที่ซ้ำโปรดใช้ชื่ออื่น"

    return render(request, template_name="editroom.html", context=context)

# เเก้ไขประเภทสถานที่
@login_required(login_url='/management/')
@permission_required('is_staff', login_url='/management/')
def editRoomType(request, roomTypeId):
    context = {}

    roomType = RoomType.objects.get(id=roomTypeId)
    context['roomType'] = roomType

    hasFacilities = RoomType_Facility.objects.filter(roomType_id=roomTypeId)
    context['hasFacilities'] = hasFacilities

    facility =  Facility.objects.all()
    context['facilities'] = facility

    # roomTypeName = RoomType.objects.filter(typeTitle=request.POST.get('typeTitle'))

    if request.method == "POST":
        roomType.typeTitle = request.POST.get('typeTitle')
        roomType.save()
        return redirect('/management/allType')

    # elif request.method == "POST" and roomTypeName.exists() == True:
    #     context['error'] = "ชื่อประเภทสถานที่ซ้ำโปรดใช้ชื่ออื่น"
    
    return render(request, template_name="editroomtype.html", context=context)

# เเก้ไขประเภทสถานที่
@login_required(login_url='/management/')
@permission_required('is_staff', login_url='/management/')
def editFacility(request, facilityId):
    context = {}

    facility = Facility.objects.get(id=facilityId)
    context['facility'] = facility

    # facilityName = Facility.objects.filter(name=request.POST.get('name'))

    if request.method == "POST":
        facility.name = request.POST.get('name')
        facility.description = request.POST.get('description')
        facility.save()
        return redirect('/management/allfacility')

    # elif request.method == "POST" and facilityName.exists() == True:
    #     context['error'] = "ชื่อสิ่งอำนวยความสะดวกซ้ำโปรดใช้ชื่ออื่น"
    
    return render(request, template_name="editfacility.html", context=context)
    
