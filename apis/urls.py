# apis/urls.py
from django.urls import path

from . import views

urlpatterns = [
	path('import_stations/', views.import_stations, name='import_stations'),
	path('import_trips/', views.import_trips, name='import_trips'),
	path('import_sample_trips/', views.import_sample_trips, name='import_sample_trips'),
	path('test_function/', views.test_function, name='test_function'),
	path('trips/', views.trips_list, name='trips_list'),
	path('stations/', views.stations_list, name='stations_list'),
	path('stations/<int:station_id>/', views.station_details, name='station_details'),
	#path('stations/<int:station_id>/trips/', views.station_trips, name='station_trips'),
	path('stations/<int:station_id>/trips_from/', views.station_trips_departure, name='station_trips_departure'),
	path('stations/<int:station_id>/trips_to/', views.station_trips_return, name='station_trips_return'),
	path('stations/<int:station_id>/trips_from/count/', views.station_trips_departure_count, name='station_trips_departure_count'),
	path('stations/<int:station_id>/trips_to/count/', views.station_trips_return_count, name='station_trips_return_count'),
	path('trips/<int:trip_id>/', views.trip_details, name='trip_details'),
	path('trips/top_distance/<int:trips_count>/', views.top_trips_by_distance, name='top_trips_by_distance'),
	path('trips/top_duration/<int:trips_count>/', views.top_trips_by_duration, name='top_trips_by_duration'),
	path('trips/top_from/<int:n>/', views.top_trips_from, name='top_trips_from'),
	path('trips/top_to/<int:n>', views.top_trips_to, name='top_trips_to'),
]