from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User, Group																																																																																																																																																																																																																																																																																																																																																																																																																																																																																										 
from Hrent.models import Hotel, Room_catagories, Rooms, Room_image, Bookings, Contact_us
from Hrent.serializer import UserSerializer, HotelSerializer, Room_CatagoriesSerializer, RoomsSerializer, Room_imageSerializer, BookingsSerializer,Contact_usSerializer

def open(request):
	return render(request,"index.html")
@api_view(['POST'])
def signupcustomer(request):
	try:
		first_name = request.data["first_name"]
		last_name  = request.data["last_name"]
		email     = request.data["email"]
		username  = request.data["username"]
		password  = request.data["password"]
		user = User.objects.create(first_name=first_name,last_name=last_name,email=email,username=username,
				password=make_password(password))
		g = Group.objects.get(name="Customer")
		g.user_set.add(user)
		if user is not None:
			return Response({"status":"1","message":"successfully Done"},status=status.HTTP_200_OK)
		else:
			return Response({"message":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	except Exception as e:
		print(e)
		return Response({"messgage":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@api_view(['POST'])
def logincustomer(request):
	try:
		if request.method == "POST":
			user = authenticate(username=request.data['username'],password=request.data['password'])
			if user is not None:
				token = ''
				try:
					u_w_t=Token.objects.get(user=user)
				except:
					u_w_t=None

				if u_w_t is None:
					token1 = Token.objects.create(user=user)
					token = token1.key
				else:
					Token.objects.get(user=user).delete()
					token1 = Token.objects.create(user=user)
					token = token1.key
				userS = UserSerializer(user).data
				#userS = UserSerializer(userList, many=True).data
				return Response({"message":"successful","token":token, "user":userS},status=status.HTTP_200_OK)
			else:
				return Response({"message":"need to sign up"},status=status.HTTP_401_UNAUTHORISED)
		return Response({"message":"forbidden"},status=status.HTTP_400_BAD_REQUEST)
	except:
		return Response({"message":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


		
@api_view(['GET'])
def show_hotel(request):
	if request.method == "GET":
		hotel = Hotel.objects.all()
		serializer = HotelSerializer(hotel,many=True).data
		return Response({"message":"displaying all the hotels","serializer":serializer},status=status.HTTP_200_OK)
		# return render(request,"index.html")
	return Response({"message":"NOT IMPLEMENTED"},status=status.HTTP_501_NOT_IMPLEMENTED)



@api_view(['POST'])
def addhotel(request):
	API_Key = request.META.get('HTTP_USERAPI')
	if API_Key is not None:
		try:
			token1 = Token.objects.get(key=API_Key)
			user = token1.user
			print(user)
		except:
			return Response({"message":"NEED TO LOGIN AGAIN"},status=status.HTTP_401_UNAUTHORIZED)
		try:
			checkgroup = user.groups.filter(name="Admin").exists()
			print(checkgroup)
			checkgroup1 = user.groups.filter(name="Customer").exists()
			print(checkgroup1)
		except:
			return Response({"message":"lol"},status=status.HTTP_400_BAD_REQUEST)
		try:
			if checkgroup1:
				return Response({"message":"not authorised"},status=status.HTTP_401_UNAUTHORIZED)
			elif checkgroup:
				hotel 	= Hotel(name = request.data['name'],desc=request.data['desc'],address=request.data['address'],phone=request.data['phone'])
				if hotel is not None:
					hotel.save()
					serializer = HotelSerializer(hotel).data
					return Response({"message":"created ","serializer":serializer},status=status.HTTP_200_OK)
				else:
					return Response({"message":"something went wrong"},status=status.HTTP_400_BAD_REQUEST)
			else:
				return Response({"message":"well things needs to be done preciesly"},status=status.HTTP_400_BAD_REQUEST)
		except:
			return Response({"message":"internal error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	else:
		return Response({"message":"YOU ARE NOT AUTHORISED"},status=status.HTTP_401_UNAUTHORIZED)



@api_view(["PUT"])
def updatehotel(request,pk):
	if request.method == "PUT":
		API = request.META.get('HTTP_USERAPI')
		if API is not None:
			try:
				token1 = Token.objects.get(key=API)
				user = token1.user
			except:
				return Response({"message":"PLEASE LOGIN AGAIN"},status=status.HTTP_401_UNAUTHORIZED)
			chkgrp1 = user.groups.filter(name="Admin").exists()
			chkgrp2 = user.groups.filter(name="Customer").exists()
			if chkgrp1:
				Hotel.objects.filter(id = pk).update(name=request.data['name'],desc=request.data['desc'],address=request.data['address'],phone=request.data['phone'])
				hotel = Hotel.objects.get(id=pk)
				serializer = HotelSerializer(hotel).data
				return Response({"message":"updated","serializer":serializer},status=status.HTTP_200_OK)
			elif chkgrp2:
				return Response({"message":"you're not authorised"},status=status.HTTP_401_UNAUTHORIZED)
			else:
				return Response({"message":"RESTRICTED"},status=status.HTTP_403_FORBIDDEN)
		else:
			return Response({"message":"internal error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	else:
		return Response({"message":"not implemented"},status=status.HTTP_501_NOT_IMPLEMENTED)			

@api_view(['DELETE'])
def deletehotel(request,pk):
	API = request.META.get('HTTP_USERAPI')
	try:
		token1 = Token.objects.get(key=API)
		user = token1.user
	except:
		return Response({"message":"PLEASE RE_LOG_IN"},status=status.HTTP_401_UNAUTHORIZED)
	chkgrp1 = user.groups.filter(name="Admin").exists()
	chkgrp2 = user.groups.filter(name="Customer").exists()
	if chkgrp1:
		a = Hotel.objects.get(id = pk)
		a.delete()
		return Response({"message":"DONE"},status=status.HTTP_200_OK)
	elif chkgrp2:
		return Response({"message":"you're not authorized"},status=status.HTTP_401_UNAUTHORIZED)
	else:
		return Response({"message":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def roomcatagory(request):
	if request.method == "GET":
		rcat = Room_catagories.objects.all()
		serializer = Room_CatagoriesSerializer(rcat, many=True).data
		return Response({"message":"all room catagories","serializer":serializer},status=status.HTTP_200_OK)
	return Response({"message":"NOT IMPLEMENTED"},status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['POST'])
def addroomcatagory(request):
	if request.method =="POST":
		API = request.META.get('HTTP_USERAPI')
		try:
			token1 = Token.objects.get(key=API)
			user = token1.user
		except:
			return Response({"message":"PLEASE LOGIN AGAIN"},status=status.HTTP_401_UNAUTHORIZED)
		chkgrp1 = user.groups.filter(name="Admin").exists()
		chkgrp2 = user.groups.filter(name="Customer").exists()
		if chkgrp1:
			a = Room_catagories(name= request.data['name'])
			a.save()
			serializer = Room_CatagoriesSerializer(a).data
			return Response({"message":"successfully created","serailizer":serializer},status=status.HTTP_200_OK)
		elif chkgrp2:
			return Response({"message":"you're not authorized"}, status=status.HTTP_401_UNAUTHORIZED)
		else:
			return Response({"message":"internal error"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	else:
		return Response({"message":"NOT IMPLEMENTED"},status=status.HTTP_501_NOT_IMPLEMEMTED)

@api_view(['PUT'])
def updateroomcatagory(request,pk):
	if request.method == 'PUT':
		API = request.META.get("HTTP_USERAPI")
		try:
			token1 = Token.objects.get(key=API)
			user = token1.user
		except:
			return Response({"message":"PLEASE LOGIN AGAIN"},status= status.HTTP_401_UNAUTHORIZED)
		chkgrp1 = user.groups.filter(name="Admin").exists()
		chkgrp2 = user.groups.filter(name="Customer").exists()
		if chkgrp1:
			Room_catagories.objects.filter(id=pk).update(name= request.data['name'])
			r = Room_catagories.objects.get(id=pk)
			serializer = Room_catagories(r).data
			return Response({"message":"updated","serializer":serializer},status=status.HTTP_200_OK)
		elif chkgrp2:
			return Response({"message":"you're not authorized"},status=status.HTTP_401_UNAUTHORIZED)
		else:
			return Response({"message":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def roomcatagoryid(request,pk):
	if request.method =="GET":
		a = Room_catagories.objects.get(id=pk)
		serializer = Room_CatagoriesSerializer(a)
		return Response({"message":"there you go","serializer":serializer.data},status=status.HTTP_200_OK)
	return Response({"message":"not implemented"},status=status.HTTP_501_NOT_IMPLEMENTED)

@api_view(['DELETE'])
def deleteroomcatagory(request,pk):
	if request.method == "DELETE":
		API = request.META.get("HTTP_USERAPI")
		try:
			token1 = Token.objects.get(key=API)
			user = token1.user
		except:
			return Response({"message":"PLEASE RELOGIN"},status=status.HTTP_401_UNAUTHORIZED)
		chkgrp1 = user.groups.filter(name="Admin").exists()
		chkgrp2 = user.groups.filter(name="Customer").exists()
		if chkgrp1:
			Room_catagories.objects.filter(id=pk).delete()
			return Response({"message":"successfully deleted"},status=status.HTTP_200_OK)
		elif chkgrp2:
			return Response({"messgae":"you're not authorized"},status=status.HTTP_401_UNAUTHORIZED)
		else:
			return Response({"message":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	return Response({"message":"not implemented"},status=status.HTTP_501_NOT_IMPLEMENTED)

@api_view(['GET'])
def contact(request):
	if request.method == "GET":
		cont = Contact_us.objects.all()
		serializer = Contact_usSerializer(cont,many = True).data
		return Response({"message":"successfull","serializer":serializer},status=status.HTTP_200_OK)
	return Response({"message":"NOT IMPLEMENTED"},status=status.HTTP_501_NOT_IMPLEMENTED)



@api_view(['POST'])
def addcontactus(request):
	if request.method =='POST':
		API = request.META.get("HTTP_USERAPI")
		try:
			token1 = Token.objects.get(key=API)
			user = token1.user
		except:
			return Response({"message":"PLEASE LOGIN AGAIN"},status=status.HTTP_401_UNAUTHORIZED)
		chkgrp1 = user.groups.filter(name="Admin").exists()
		chkgrp2 = user.groups.filter(name="Customer").exists()
		if chkgrp1:
			a = Contact_us(name=request.data['name'],email=request.data['email'],title=request.data['title'],message=request.data['message'])
			a.save()
			serializer = Contact_usSerializer(a).data
			return Response({"message":"successful","serializer":serializer})
		elif chkgrp2:
			return Response({"message":"you're not authorized"},status=status.HTTP_401_UNAUTHORIZED)
		else:
			return Response({"message":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	return Response({"message":"NOT IMPLEMENTED"},status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(["GET"])
def rooms(request):
	if request.method == "GET":
		rooms = Rooms.objects.all()
		serializer = RoomsSerializer(rooms,many=True).data
		return Response({"message":"successful","serializer":serializer},status=status.HTTP_200_OK)
	return Response({"message":"NOT IMPLEMENTED"},status=status.HTTP_501_NOT_IMPLEMENTED)



@api_view(['POST'])	
def addroom(request,pk,id):
	if request.method =="POST":
		API = request.META.get("HTTP_USERAPI")
		try:
			token1 = Token.objects.get(key=API)
			user = token1.user
		except:
			return Response({"message":"PLEASE LOGIN AGAIN"},status=status.HTTP_401_UNAUTHORIZED)
		chkgrp1 = user.groups.filter(name= "Admin").exists()
		chkgrp2 = user.groups.filter(name="Customer").exists()
		catagories = Room_catagories.objects.get(id=pk)
		hotel = Hotel.objects.get(id=id)
		if chkgrp2:
			return Response({"message":"you're not authorized"},status=status.HTTP_401_UNAUTHORIZED)
		elif chkgrp1:
			a = Rooms(num_of_person=request.data['person'],num_of_rooms=request.data['rooms'],catagory_id=catagories,hotel_id=hotel)
			a.save()
			serializer = RoomsSerializer(a).data
			return Response({"message":"successfully done","serializer":serializer},status=status.HTTP_200_OK)
		else:
			return Response({"message":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	return Response({"message":"not implemented"},status=status.HTTP_501_NOT_IMPLEMENTED)

@api_view(["PUT"])
def updateroom(request,pk):
	API = request.META.get("HTTP_USERAPI")
	try:
		token1 = Token.objects.get(key=API)
		user = token1.user
	except:
		return Response({"message":"PLEASE LOG IN AGAIN"},status = status.HTTP_401_UNAUTHORIZED)
	chkgrp1 = user.groups.filter(name="Admin").exists()
	chkgrp2 = user.groups.filter(name="Customer").exists()
	if chkgrp2:
		return Response({"message":"you're not authorized"},status=status.HTTP_401_UNAUTHORIZED)
	elif chkgrp1:
		Rooms.objects.filter(id=pk).update(num_of_person=request.data['person'],num_of_rooms=request.data['rooms'],catagory_id=request.data['catagory'],hotel_id=request.data['hotel'])
		a = Rooms.objects.get(id=pk)
		serializer = RoomsSeralizer(a).data
		return Response({"message":"successfully updated","serializer":serializer},status=status.HTTP_200_OK)
	else:
		return Response({"message":"internal server error "},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['DELETE'])
def removeroom(request,pk):
	if request.method =="DELETE":
		API = request.META.get("HTTP_USERAPI")
		try:
			token1 = Token.objects.get(key=API)
			user = token1.user
		except:
			return Response({"message":"PLEASE LOG IN AGAIN"},status=status.HTTP_401_UNAUTHORIZED)
		chkgrp1 = user.groups.filter(name="Customer").exists()
		chkgrp2 = user.groups.filter(name="Admin").exists()
		if chkgrp1:
			return Response({"message":"you're not authorized"},status=status.HTTP_401_UNAUTHORIZED)
		elif chkgrp2:
			Rooms.objects.filter(id=pk).delete()
			return Response({"message":"successfully deleted"},status=status.HTTP_200_OK)
		else:
			return Response({"message":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	return Response({"message":"NOT IMPLEMETED"},status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['GET'])
def image(request):
	if request.method == "GET":
		a = Room_image.objects.all()
		serializer = Room_imageSerializer(a,many=True).data
		return Response({"message":"successful","serializer":serializer},status=status.HTTP_200_OK)
	return Response({"message":"NOT IMPLEMENTED"},status=status.HTTP_501_NOT_IMPLEMENTED)


@api_view(['POST'])
def addimage(request,pk):
	if request.method == "POST":
		API = request.META.get("HTTP_USERAPI")
		try:
			token1 = Token.objects.get(key=API)
			user = token1.user
		except:
			return Response({"message":"PLEASE LOGIN AGAIN"},status=status.HTTP_401_UNAUTHORIZED)
		chkgrp1 = user.groups.filter(name="Admin").exists()
		chkgrp2 = user.groups.filter(name="Customer").exists()
		if chkgrp2:
			return Response({"message":"you're not authorized"},status=status.HTTP_401_UNAUTHORIZED)
		elif chkgrp1:
			roomid = Rooms.objects.get(id=pk)
			a = Room_image(room_id=roomid,image=request.data['image'])
			a.save()
			serializer = Room_imageSerializer(a).data
			return Response({"message":"successfully uploaded","serializer":serializer},status=status.HTTP_200_OK)
		else:
			return Response({"message":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	return Response({"message":"NOT IMPLEMENTED"},status=status.HTTP_501_NOT_IMPLEMENTED)

@api_view(["PUT"])
def updateroomimage(request,pk):
	if request.method == "PUT":
		API = request.META.get("HTTP_USERAPI")
		try:
			token1 = Token.objects.get(key=API)
			user = token1.user
		except:
			return Response({"message":"PLEASE LOGIN AGAIN"},status=status.HTTP_401_UNAUTHORIZED)
		chkgrp1 = user.groups.filter(name="Admin").exists()
		chkgrp2 = user.groups.filter(name="Customer").exists()
		if chkgrp2:
			return Response({"message":"you're not authorized"},status=status.HTTP_401_UNAUTHORIZED)
		elif chkgrp1:
			b = Room_image.objects.get(id=pk)
			b.image = request.data["image"]
			# b.room_id = request.data["roomid"]
			b.save()
			Room_image.objects.filter(id=pk).update(room_id=request.data['roomid'])
			# b.save()
			a = Room_image.objects.get(id=pk)
			serializer = Room_imageSerializer(a).data
			return Response({"message":"successfully updated","serializer":serializer},status=status.HTTP_200_OK)
		else:
			return Response({"message":"something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
	return Response({"message":"NOT IMPLEMENTED"},status=status.HTTP_501_NOT_IMPLEMENTED)
