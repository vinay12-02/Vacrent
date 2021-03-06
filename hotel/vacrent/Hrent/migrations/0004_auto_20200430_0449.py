# Generated by Django 3.0.5 on 2020-04-30 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Hrent', '0003_auto_20200430_0439'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookings',
            options={'verbose_name_plural': 'Bookings'},
        ),
        migrations.AlterModelOptions(
            name='contact_us',
            options={'verbose_name_plural': 'Contact_us'},
        ),
        migrations.AlterModelOptions(
            name='room_image',
            options={'verbose_name_plural': 'Room_images'},
        ),
        migrations.AlterModelOptions(
            name='rooms',
            options={'verbose_name_plural': 'Rooms'},
        ),
        migrations.AlterField(
            model_name='bookings',
            name='from_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='bookings',
            name='to_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterModelTable(
            name='contact_us',
            table='Contact_us',
        ),
        migrations.AlterModelTable(
            name='room_catagories',
            table='Room_catagories',
        ),
    ]
