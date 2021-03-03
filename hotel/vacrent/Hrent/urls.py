from django.urls import path
from Hrent import views

urlpatterns = [
#     # path('<int:pk>/',views.home,name= "home"),
#     path('',views.home,name="home"),
#     path('room/',views.room,name ="room"),
#     path('bookings/',views.bookings,name= "bookings"),
#     path('about/',views.about,name="about"),
#     path('contact/',views.contact,name="contact")
	path("in/",views.open,name = "index"),
	path("signup/",views.signupcustomer,name = "signup"),
	path("login/",views.logincustomer,name="login"),
	path("hotel/",views.show_hotel,name="hotel"),
	path("addhotel/",views.addhotel,name="addhotel"),
	path("updatehotel/<int:pk>",views.updatehotel,name="updatehotel"),
	path("deletehotel/<int:pk>",views.deletehotel,name="deletehotel"),
	path("roomcatagory/",views.roomcatagory,name="roomcatagory"),
	path("addroomcatagory",views.addroomcatagory,name="addroomcatagory"),
	path("updateroomcat/<int:pk>",views.updateroomcatagory,name="updateroomcat"),
	path("catagoryid/<int:pk>",views.roomcatagoryid,name="catagoryid"),
	path("deleteroomcatagory/<int:pk>",views.deleteroomcatagory,name="deleteroomcatagory"),
	path("contact/",views.contact,name="contact"),
	path("addcontactus/",views.addcontactus,name="addcontactus"),
	path("rooms/",views.rooms,name="rooms"),
	path("addroom/<int:pk>/<int:id>",views.addroom,name="addroom"),
	path("updateroom/<int:pk>",views.updateroom,name="updateroom"),
	path("removeroom/<int:pk>",views.removeroom,name="removeroom"),
	path("roomimage/",views.image,name="roomimage"),
	path("addimage/<int:pk>",views.addimage,name="addimage"),
	path("updateroomimage/<int:pk>",views.updateroomimage,name="updateroomimage"),

]
