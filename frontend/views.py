from django.shortcuts import render
from frontend.constants import SERVER_URL

# Create your views here.

import requests
from django.http import HttpResponse, JsonResponse


# test the api by calling the trips endpoint
def test_api(request):
	response = requests.get(SERVER_URL+'api/trips/')
	if response.status_code == 200:
		data = response.json()
		return render(request,"frontend/test.html",{'data':data,})
	else:
		return render(request,"frontend/test.html",{'data':'error',})



# Get all the stations paginated by calling the API
def stations_list(request):
	if request.GET.get('page'):
		response = requests.get(SERVER_URL+'api/stations/?page='+request.GET.get('page'))
	else:
		response = requests.get(SERVER_URL+'api/stations/')
	if response.status_code == 200:
		data = response.json()
		return render(request,"frontend/stations_list.html", {'data':data,})
	else:
		return render(request,"frontend/stations_list.html", {'data': "Error getting data from server",})


# Get all the trips paginated
def trips_list(request):
	if request.GET.get('page'):
		response = requests.get(SERVER_URL+'api/trips/?page='+request.GET.get('page'))
	else:
		response = requests.get(SERVER_URL+'api/trips/')
	if response.status_code == 200:
		data = response.json()
		return render(request,"frontend/trips_list.html", {'data':data,})
	else:
		return render(request,"frontend/trips_list.html", {'data': "Error getting data from server",})



# Get station details
def station_details(request,id):

	# Get one station
	get_station = requests.get(SERVER_URL+'api/stations/'+str(id))
	station = get_station.json()

	# Get the count of the trips from this station
	get_trips_from = requests.get(SERVER_URL+'api/stations/'+str(id)+'/trips_from/count/')
	trips_from = get_trips_from.json()

	# Get the count of the trips to this station
	get_trips_to = requests.get(SERVER_URL+'api/stations/'+str(id)+'/trips_to/count/')
	trips_to = get_trips_to.json()

	# Pass the data to the templates
	return render(request,"frontend/station_details.html", {'station':station, 'trips_from':trips_from, 'trips_to':trips_to})




# Get stats for homepage
def home(request):
	get_trips_by_duration = requests.get(SERVER_URL+'api/trips/top_duration/5')
	trips_by_duration = get_trips_by_duration.json()
	get_trips_by_distance = requests.get(SERVER_URL+'api/trips/top_distance/5')
	trips_by_distance = get_trips_by_distance.json()
	get_top_stations_from = requests.get(SERVER_URL+'api/trips/top_from/5')
	top_stations_from = get_top_stations_from.json()
	get_top_stations_to = requests.get(SERVER_URL+'api/trips/top_to/5')
	top_stations_to = get_top_stations_to.json()
	return render(request, "frontend/home.html", {'trips_by_duration':trips_by_duration, 'trips_by_distance':trips_by_distance, 'top_stations_from':top_stations_from, 'top_stations_to':top_stations_to})
