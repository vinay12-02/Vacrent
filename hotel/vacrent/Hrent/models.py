from django.db import models
from django.contrib.auth.models import User

class Hotel(models.Model):
	name 	= models.CharField(max_length=30,blank=True,null=True)
	desc 	= models.TextField(max_length= 200,blank=True,null=True)
	address = models.TextField(max_length = 100,blank=True,null=True)
	phone   = models.CharField(max_length=12, null=True,blank=True)

	def __str__(self):
		return self.name
	class Meta:
		db_table = "Hotel"
		verbose_name_plural = "Hotels"


class Room_catagories(models.Model):
	name = models.CharField(max_length=30,blank=True,null=True)
	def __str__(self):
		return self.name
	class Meta:
		db_table = "Room_catagories"
		verbose_name_plural = "Room_catagories"


class Rooms(models.Model):
	num_of_person = models.PositiveIntegerField(blank=True,null=True)
	num_of_rooms  = models.PositiveIntegerField(blank=True,null=True)
	catagory_id   = models.ForeignKey(Room_catagories,on_delete=models.CASCADE)
	hotel_id      = models.ForeignKey(Hotel, on_delete=models.CASCADE)

	def __str__(self):
		return self.catagory_id.name
	class Meta:
		db_table = "Room"
		verbose_name_plural = "Rooms"


class Room_image(models.Model):
	room_id  = models.ForeignKey(Rooms,on_delete=models.CASCADE)
	image    = models.ImageField(upload_to= 'pics',blank=True,null=True)

	def __str__(self):
		return self.room_id.catagory_id.name
	class Meta:
		db_table = "Room_image"
		verbose_name_plural = "Room_images"



class Bookings(models.Model):
	from_date  = models.DateTimeField(blank=True,null=True)
	to_date    = models.DateTimeField(blank=True,null=True)
	user_id    = models.ForeignKey(User, on_delete=models.CASCADE)
	room_id    = models.ForeignKey(Rooms, on_delete=models.CASCADE)

	def __str__(self):
		return self.from_date
	class Meta:	
		db_table = "Booking"
		verbose_name_plural = "Bookings"


class Contact_us(models.Model):
	name    = models.CharField(max_length=30,blank=True,null=True)
	email   = models.EmailField(max_length = 50,blank=True,null=True)
	title   = models.CharField(max_length= 50,blank=True,null=True)
	message = models.TextField(max_length= 300,blank=True,null=True)

	def __str__(self):
		return self.name

	class Meta:
		db_table = "Contact_us" 
		verbose_name_plural = "Contact_us"














