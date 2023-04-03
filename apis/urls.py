# apis/urls.py
from django.urls import path

from . import views

urlpatterns = [
	path('import_stations/', views.import_stations, name='import_stations'),
	path('import_trips/', views.import_trips, name='import_trips'),
	path('test_function/', views.test_function, name='test_function'),
	path('trips/', views.trips_list, name='trips_list'),
	path('stations/', views.stations_list, name='stations_list'),
	path('stations/<int:station_id>/', views.station_details, name='station_details'),
	#path('stations/<int:station_id>/trips/', views.station_trips, name='station_trips'),
	path('stations/<int:station_id>/trips_from/', views.station_trips_departure, name='station_trips_departure'),
	path('stations/<int:station_id>/trips_to/', views.station_trips_return, name='station_trips_return'),
	path('trips/<int:trip_id>/', views.trip_details, name='trip_details'),
]