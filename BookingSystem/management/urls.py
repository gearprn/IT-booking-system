from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('', views.adminSignIn, name="adminSignIn"),
    path('request', views.request, name='request'),
    path('<int:detail_id>', views.detail, name='detail'),
    path('createroom', views.createroom, name='createroom'),
    path('addfacility', views.addfacility, name='addfacility'), 
    path('addtype', views.addRoomtype, name='addtype'),
    path('deleteRoom/<int:room_id>', views.deleteRoom, name='deleteRoom'),
    path('deleteRoomType/<int:roomType_id>', views.deleteRoomType, name='deleteRoomType'),
    path('deleteFacility/<int:facility_id>', views.deleteFacility, name='deleteFacility'),
    path('allRoom', views.allRoom, name='allRoom'),
    path('allType', views.allRoomType, name='allRoomType'),
    path('allfacility', views.allfacility, name='allfacility'),
    path('room/e/<int:roomId>', views.editRoom, name="editRoom"),
    path('roomtype/e/<int:roomTypeId>', views.editRoomType, name="editRoomType"),
    path('facility/e/<int:facilityId>', views.editFacility, name="editFacility"),
    path('history', views.myApprove, name="myApprove"),
    path('approve/<int:bookBy_id>', views.btnApprove, name='btnApprove'),

]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 