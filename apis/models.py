from django.db import models

class Station(models.Model):
	nimi = models.CharField(max_length=100)
	namn = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	osoite = models.CharField(max_length=100)
	adress = models.CharField(max_length=100)
	kaupunki = models.CharField(max_length=100)
	stad = models.CharField(max_length=100)
	kapasiteet = models.IntegerField(default=0)
	x = models.FloatField()
	y = models.FloatField()


class Trip(models.Model):
	departure_time = models.DateField()
	return_time = models.DateField()
	departure_station_id = models.ForeignKey(Station, null=True, on_delete=models.SET_NULL, related_name='departure_station')
	return_station_id = models.ForeignKey(Station, null=True, on_delete=models.SET_NULL, related_name='return_station')
	covered_distance = models.IntegerField(default=0)
	duration = models.IntegerField(default=0)