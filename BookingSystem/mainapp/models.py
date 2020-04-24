from django.db import models

# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)

    available_Status = (
        ('AVAILABLE', 'Available'),
        ('UNDER MAINTENANCE', 'Under Maintenance')
    )

    availableStatus = models.CharField(max_length=17, choices=available_Status, default='AVAILABLE')

    size = models.IntegerField()
    photo = models.ImageField(upload_to='RoomPhotos')
    roomType = models.ForeignKey('mainapp.RoomType', on_delete=models.CASCADE)

class RoomType(models.Model):
    typeTitle = models.CharField(max_length=255)

class Facility(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

class RoomType_Facility(models.Model):
    roomType = models.ForeignKey('mainapp.RoomType', on_delete=models.CASCADE)
    facility = models.ForeignKey('mainapp.Facility', on_delete=models.CASCADE)
    amount = models.IntegerField()