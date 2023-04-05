from django.shortcuts import render
from frontend.constants import SERVER_URL

# Create your views here.

import requests
from django.http import HttpResponse, JsonResponse


def test_api(request):
	response = requests.get('http://127.0.0.1:8000/api/trips/')
	if response.status_code == 200:
		data = response.json()
		#return JsonResponse(data)
		return render(request,"frontend/test.html",{'data':data,})
	else:
		return render(request,"frontend/test.html",{'data':'error',})
		#return JsonResponse({'error': 'Failed to retrieve data from API'})




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



def station_details(request,id):
	get_station = requests.get(SERVER_URL+'api/stations/'+str(id))
	station = get_station.json()

	get_trips_from = requests.get(SERVER_URL+'api/stations/'+str(id)+'/trips_from/count/')
	trips_from = get_trips_from.json()

	get_trips_to = requests.get(SERVER_URL+'api/stations/'+str(id)+'/trips_to/count/')
	trips_to = get_trips_to.json()

	return render(request,"frontend/station_details.html", {'station':station, 'trips_from':trips_from, 'trips_to':trips_to})