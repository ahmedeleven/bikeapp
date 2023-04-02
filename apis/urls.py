# apis/urls.py
from django.urls import path

from . import views

urlpatterns = [
	path('import_stations/',views.import_stations,name='import_stations'),
	path('import_trips/',views.import_trips,name='import_trips')
]