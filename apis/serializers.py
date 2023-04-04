from rest_framework import serializers
from .models import Trip
from .models import Station



class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        fields = '__all__'


class TripSerializer(serializers.ModelSerializer):
    departure_station = StationSerializer()
    return_station = StationSerializer()

    class Meta:
        model = Trip
        fields = '__all__'