import datetime

from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.template.context_processors import request

from mainapp.models import (Booking, Facility, Room, RoomType, RoomType_Facility, Student, Approve)

# Create your views here.

# คำร้องขอทั้งหมด
def request(request):
    context = {}

    allreq = Booking.objects.all()
    context['allreq'] = allreq
    return render(request, template_name='request.html', context=context)

# รายละเอียดทั้งมหด
def detail(request, detail_id):
    context = {}

    detail = Booking.objects.get(id= detail_id)
    context['detail'] = detail
    return render(request, template_name='detail.html', context=context)

# เพิ่มสถานที่
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
def addfacility(request):
    user = request.user.id
    if request.method == 'POST':
        facilityName = request.POST.get('name')
        facilityDesc = request.POST.get('description')

        addFacility = Facility.objects.create(name=facilityName, description=facilityDesc)
        return redirect('allfacility')

    return render(request, template_name='createfacility.html')

# เพิ่มประเภทห้อง
def addRoomtype(request):
    user = request.user.id
    if request.method == 'POST':
        roomType = request.POST.get('typeTitle')
    
        addType = RoomType.objects.create(typeTitle=roomType)
        return redirect('allRoomType')

    return render(request, template_name='createtype.html')

# ลบสถานที่/ห้อง
def deleteRoom(request, room_id):
    delRoom = Room.objects.get(pk= room_id)
    delRoom.delete()

    return redirect('allRoom')

# ลบประเภทของห้อง
def deleteRoomType(request, roomType_id):
    delRoomType = RoomType.objects.get(pk= roomType_id)
    delRoomType.delete()

    return redirect('allRoomType')

# ลบสิ่งอำนวยความสะดวก
def deleteFacility(request, facility_id):
    delFacility = Facility.objects.get(pk= facility_id)
    delFacility.delete()

    return redirect('allfacility')

# get allroom
def allRoom(request):
    context = {}
    
    rooms = Room.objects.all()
    context['rooms'] = rooms
    return render(request, template_name='allroom.html', context= context)

# get allroomtype
def allRoomType(request):
    context = {}
    
    types = RoomType.objects.all()
    context['types'] =  types
    return render(request, template_name='alltype.html', context= context)

# get allfacility
def allfacility(request):
    context = {}
    
    facilities = Facility.objects.all()
    context['facilities'] =  facilities
    return render(request, template_name='allfacility.html', context= context)

# การอนุมัติ/ไม่อนุมัติให้ใช้สถานที่
def btnApprove(request, bookBy_id):
    context = {}
    bookingStatus = Booking.objects.get(id=bookBy_id)
    approve = Approve.objects.get(id=bookingStatus.approve_id)

    approve.result = 'APPROVED'
    approve.save()

    context['detail'] =bookingStatus
    context['approve'] =approve
    return render(request, template_name='detail.html', context= context)