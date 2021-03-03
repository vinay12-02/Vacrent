from django.contrib import admin
from Hrent.models import Hotel, Room_catagories, Rooms, Room_image, Bookings, Contact_us
# Register your models here.

admin.site.register(Hotel)
admin.site.register(Room_catagories)
admin.site.register(Rooms)
admin.site.register(Room_image)
admin.site.register(Bookings)
admin.site.register(Contact_us)