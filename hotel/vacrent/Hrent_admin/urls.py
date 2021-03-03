from django.urls import path
from Hrent_admin import views

urlpatterns = [
	path("",views.index,name="index"),
	path("about/",views.about,name="about"),
	path("rooms/",views.rooms,name="rooms"),
	path("contact/",views.contact,name="contact"),
	path("bookings/",views.bookings,name="bookings"),
]