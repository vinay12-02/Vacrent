from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
	return render(request,"index.html")
def about(request):
	return render(request,"about.html")
def rooms(request):
	return render(request,"rooms.html")
def contact(request):
	return render(request,"contact.html")
def bookings(request):
	return render(request,"bookings.html")
