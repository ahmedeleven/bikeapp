from django.urls import path

from . import views

urlpatterns = [
	path('test_api/', views.test_api, name='test_api'),
	path('stations/', views.stations_list, name='stations_list'),
	path('stations/<int:id>/', views.station_details, name='station_details'),
	path('trips/', views.trips_list, name='trips_list'),
	path('', views.home, name='home'),
]