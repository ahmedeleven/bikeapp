from django.shortcuts import render
import numpy as np
import pandas as pd
from .models import Station
from .models import Trip
from django.http import HttpResponse
from tqdm import tqdm
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TripSerializer, StationSerializer
from rest_framework.pagination import PageNumberPagination



# import stations to stations table
def import_stations(request):
	# read the stations from CSV file to a pandas dataframe
	stations_df = pd.read_csv("https://opendata.arcgis.com/datasets/726277c507ef4914b0aec3cbcfcbfafc_0.csv")
	# remove unnecessary columns from the dataframe
	stations_df = stations_df.drop(["FID","Operaattor"], axis=1)
	# change all columns to lower case to match our created models
	stations_df.columns = stations_df.columns.str.lower()
	stations = stations_df.to_dict(orient="records")
	# insert stations row by row to the database
	for row in stations:
		Station.objects.create(**row)
	return HttpResponse("Done..")


def import_trips(request):
	trips1 = pd.read_csv("https://dev.hsl.fi/citybikes/od-trips-2021/2021-05.csv")
	trips2 = pd.read_csv("https://dev.hsl.fi/citybikes/od-trips-2021/2021-06.csv")
	trips3 = pd.read_csv("https://dev.hsl.fi/citybikes/od-trips-2021/2021-07.csv")
	trips_df = pd.concat([trips1,trips2,trips3])
	trips_df = trips_df.drop(["Departure station name","Return station name"], axis=1)
	trips_df = trips_df.rename(columns={"Departure":"departure_time","Return":"return_time","Departure station id":"departure_station_id", "Return station id":"return_station_id", "Covered distance (m)":"covered_distance", "Duration (sec.)":"duration"})
	trips_df["covered_distance"] = trips_df["covered_distance"].fillna(0)
	trips_df["duration"] = trips_df["duration"].fillna(0)
	trips_df = trips_df.drop(trips_df[trips_df["duration"] <= 10].index)
	trips_df = trips_df.drop(trips_df[trips_df["covered_distance"] <= 10].index)

	trips = trips_df.to_dict(orient="records")
	trip_objects = [Trip(**row) for row in trips]

	batch_size = 10000  # number of objects to create in a batch
	num_batches = (len(trip_objects) // batch_size) + 1

	with tqdm(total=len(trip_objects)) as progress_bar:
	    for i in range(num_batches):
	        batch = trip_objects[i*batch_size:(i+1)*batch_size]
	        Trip.objects.bulk_create(batch, ignore_conflicts=True)
	        progress_bar.update(len(batch))

	return HttpResponse("Done...")



@api_view(['GET'])
def test_function(request):
	return Response({'message': 'Hello!!'})




@api_view(['GET'])
def trips_list(request):
	page_number = request.GET.get('page', 1)
	page_number = int(page_number)
	page_size = request.GET.get('page_size', 100)
	paginator = PageNumberPagination()
	paginator.page_size = page_size
	trips = Trip.objects.select_related('departure_station', 'return_station').all()
	result_page = paginator.paginate_queryset(trips, request)
	serializer = TripSerializer(result_page, many=True, context={'request': request})
	data = serializer.data
	pages = {
		'count': paginator.page.paginator.count,
		'num_pages': paginator.page.paginator.num_pages,
		'current_page': page_number,
		'next': page_number+1,
		'previous': page_number-1,
	}
	if paginator.get_previous_link():
		pages['previous_link'] = paginator.get_previous_link()
		pages['previous_pages'] = [page_number-i for i in range(1,3) if page_number-i>0]
	if paginator.get_next_link():
		pages['next_link'] = paginator.get_next_link()
		pages['next_pages'] = [page_number+i for i in range(1,3) if page_number+1<=paginator.page.paginator.num_pages]

	return Response({
		'data': data,
		'pages': pages,
	})



@api_view(['GET'])
def stations_list(request):
	page_number = request.GET.get('page',1)
	page_number = int(page_number)
	page_size = request.GET.get('page_size',20)
	paginator = PageNumberPagination()
	paginator.page_size = page_size
	stations = Station.objects.all()
	result_page = paginator.paginate_queryset(stations, request)
	serializer = StationSerializer(result_page, many=True, context={'request': request})
	data = serializer.data

	pages = {
		'count': paginator.page.paginator.count,
		'num_pages': paginator.page.paginator.num_pages,
		'current_page': page_number,
		'next': page_number+1,
		'previous': page_number-1,
	}
	if paginator.get_previous_link():
		pages['previous_link'] = paginator.get_previous_link()
		pages['previous_pages'] = [page_number-i for i in range(1,3) if page_number-i>0]
	if paginator.get_next_link():
		pages['next_link'] = paginator.get_next_link()
		pages['next_pages'] = [page_number+i for i in range(1,3) if page_number+1<=paginator.page.paginator.num_pages]

	return Response({
		'data': data,
		'pages': pages,
	})

	#return Response({'data':result_page})


@api_view(['GET'])
def station_details(request, station_id):
	#station_id = request.GET.get('id')
	station = Station.objects.get(id=station_id)
	serializer = StationSerializer(station)
	return Response(serializer.data)


@api_view(['GET'])
def trip_details(request, trip_id):
	trip = Trip.objects.get(id=trip_id)
	serializer = TripSerializer(trip)
	return Response(serializer.data)


'''@api_view(['GET'])
def station_trips(request, station_id):
	#station = Station.objects.get(id=station_id)
	#trips = Trip.objects.filter(departure_station_id=station_id)
	trips = Trip.objects.filter(Q(departure_station_id=station_id) | Q(return_station_id=station_id))
	#Q(destination='New York') | Q(destination='San Francisco')
	serializer = TripSerializer(trips, many=True)
	return Response(serializer.data)'''


@api_view(['GET'])
def station_trips_departure(request, station_id):
	trips = Trip.objects.filter(departure_station_id=station_id)
	trips_count = trips.count()
	serializer = TripSerializer(trips, many=True)
	return Response({'count': trips_count, 'trips': serializer.data})


@api_view(['GET'])
def station_trips_departure(request, station_id):
	trips = Trip.objects.filter(departure_station_id=station_id)
	trips_count = trips.count()
	serializer = TripSerializer(trips, many=True)
	return Response({'count': trips_count, 'trips': serializer.data})


@api_view(['GET'])
def station_trips_departure_count(request, station_id):
	trips_count = Trip.objects.filter(departure_station_id=station_id).count()
	return Response({'count': trips_count})


@api_view(['GET'])
def station_trips_return_count(request, station_id):
	trips_count = Trip.objects.filter(return_station_id=station_id).count()
	return Response({'count': trips_count})


@api_view(['GET'])
def station_trips_return(request, station_id):
	trips = Trip.objects.filter(return_station_id=station_id)
	trips_count = trips.count()
	serializer = TripSerializer(trips, many=True)
	return Response({'count': trips_count, 'trips': serializer.data})

