# Generated by Django 5.0.dev20230322100140 on 2023-04-02 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apis', '0002_alter_trip_departure_station_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='station',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='trip',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]