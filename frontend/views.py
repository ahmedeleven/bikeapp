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
