# Generated by Django 5.0.dev20230322100140 on 2023-04-02 10:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0004_alter_trip_departure_station_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trip',
            old_name='departure_station_id',
            new_name='departure_station',
        ),
        migrations.RenameField(
            model_name='trip',
            old_name='return_station_id',
            new_name='return_station',
        ),
    ]
