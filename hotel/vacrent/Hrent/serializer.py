from django.contrib.auth.models import User
from rest_framework import serializers
from Hrent.models import Hotel, Room_catagories, Rooms, Room_image, Bookings, Contact_us



##this section for example of how to add foreignkey reference
# class MyTableSerializer(serializers.ModelSerializer):
#     user = UserSerializer(many=False, read_only=True)
#     user_id = serializers.IntegerField(write_only=True)

#     class Meta:
#         fields = '__all__'
#         model = MyTable



class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'first_name', 'last_name', 'email', 'password')

class HotelSerializer(serializers.ModelSerializer):
	class Meta:
		model  = Hotel
		fields = ('id','name','desc','address','phone')

class Room_CatagoriesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Room_catagories
		fields = ('id','name')

class RoomsSerializer(serializers.ModelSerializer):
	catagory_id=Room_CatagoriesSerializer()
	hotel_id = HotelSerializer()
	class Meta:
		model = Rooms
		fields = ('id','num_of_person','num_of_rooms','catagory_id','hotel_id')

class Room_imageSerializer(serializers.ModelSerializer):
	room_id = RoomsSerializer()
	class Meta:
		model  = Room_image
		fields = ('id', 'room_id','image')

class BookingsSerializer(serializers.ModelSerializer):
	user_id = UserSerializer()
	room_id = RoomsSerializer()
	class Meta:
		model  = Bookings
		fields = ('id','from_date','to_date','user_id','room_id')

class Contact_usSerializer(serializers.ModelSerializer):
	class Meta:
		model  = Contact_us
		fields = ('id','name','email','title','message')

		