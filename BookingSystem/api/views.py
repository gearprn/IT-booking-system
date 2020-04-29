from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from mainapp.models import RoomType_Facility

import json
# Create your views here.

@csrf_exempt
def addNewFacility(request):
    data = json.loads(request.body)

    facilityId = data['facilityId']
    roomTypeId = data['roomTypeId']
    amount = data['amount']

    if amount == '':
        res = {
            'message' : 'Invalid amount number.'
        }
        return JsonResponse(res, status=400)

    else:
        roomType_facility = RoomType_Facility.objects.create(
            roomType_id = roomTypeId,
            facility_id = facilityId,
            amount = amount
        )

        res = {
            'message' : 'Add new facility successfuly.'
        }
        return JsonResponse(res, status=200)

@csrf_exempt
def removeFacility(request):
    data = json.loads(request.body)

    roomType_facility_id = data['roomType_facility_id']

    roomType_facility = RoomType_Facility.objects.get(id=roomType_facility_id)
    roomType_facility.delete()

    res = {
        'message' : 'Remove roomType-facility successfuly.'
    }
    return JsonResponse(res, status=200)