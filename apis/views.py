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
from django.utils import timezone




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


# import trips to trips table
def import_trips(request):
	# Get the data from the datasets and merge them in one dataframe
	trip_files = ["https://dev.hsl.fi/citybikes/od-trips-2021/2021-05.csv", "https://dev.hsl.fi/citybikes/od-trips-2021/2021-06.csv", "https://dev.hsl.fi/citybikes/od-trips-2021/2021-07.csv"]
	trips1 = pd.read_csv("https://dev.hsl.fi/citybikes/od-trips-2021/2021-05.csv")
	trips2 = pd.read_csv("https://dev.hsl.fi/citybikes/od-trips-2021/2021-06.csv")
	trips3 = pd.read_csv("https://dev.hsl.fi/citybikes/od-trips-2021/2021-07.csv")
	trips_df = pd.concat([pd.read_csv(file,usecols=["Departure","Return", "Departure station id", "Return station id", "Covered distance (m)", "Duration (sec.)"]) for file in trip_files])

	# Remove unused columns and rename the dataframe column to match the column names in the database
	trips_df = trips_df.rename(columns={"Departure":"departure_time","Return":"return_time","Departure station id":"departure_station_id", "Return station id":"return_station_id", "Covered distance (m)":"covered_distance", "Duration (sec.)":"duration"})

	# Replace null values with 0
	trips_df["covered_distance"] = trips_df["covered_distance"].fillna(0)
	trips_df["duration"] = trips_df["duration"].fillna(0)

	# Exclude trips that lasts less than 10 seconds and trips with less than 10 meters distance
	trips_df = trips_df.drop(trips_df[(trips_df["duration"] <= 10) & (trips_df["covered_distance"] <= 10)].index)


	# Get a list of trip objects
	trips = trips_df.to_dict(orient="records")
	#trip_objects = [Trip(**row) for row in trips]


	# Create Trip objects with progress bar
	with tqdm(total=len(trips)) as pbar:
		for trip in trips:
			trip['departure_time'] = timezone.make_aware(datetime.strptime(trip['departure_time'], '%Y-%m-%d %H:%M:%S'))
			trip['return_time'] = timezone.make_aware(datetime.strptime(trip['return_time'], '%Y-%m-%d %H:%M:%S'))
			trip_object = Trip(**trip)
			trip_objects.append(trip_object)
			pbar.update(1)



	batch_size = 10000  # number of objects to create in a batch
	num_batches = (len(trip_objects) // batch_size) + 1   # number of batches

	# Load data in batches and show progress bar
	with tqdm(total=len(trip_objects)) as progress_bar:
	    for i in range(num_batches):
	        batch = trip_objects[i*batch_size:(i+1)*batch_size]
	        Trip.objects.bulk_create(batch, ignore_conflicts=True)
	        progress_bar.update(len(batch))

	return HttpResponse("Done...")


# Function to test the api
@api_view(['GET'])
def test_function(request):
	return Response({'message': 'Hello!!'})



# Show all trips
@api_view(['GET'])
def trips_list(request):
	page_number = request.GET.get('page', 1) # current page number
	page_number = int(page_number) # page number as integer to perform calculations
	page_size = request.GET.get('page_size', 100) # number of items per page
	paginator = PageNumberPagination() # call the built in paginator function
	paginator.page_size = page_size # set the page size to the number of items already set
	trips = Trip.objects.select_related('departure_station', 'return_station').all()  # Get all the trips and its related stations from the database
	result_page = paginator.paginate_queryset(trips, request) # the data for the current page
	serializer = TripSerializer(result_page, many=True, context={'request': request})
	data = serializer.data

	# pages data
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



# show all trips the same way than stations 
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




# get station details for one single station
@api_view(['GET'])
def station_details(request, station_id):
	station = Station.objects.get(id=station_id)
	serializer = StationSerializer(station)
	return Response(serializer.data)



# get trip details for one single trip
@api_view(['GET'])
def trip_details(request, trip_id):
	trip = Trip.objects.get(id=trip_id)
	serializer = TripSerializer(trip)
	return Response(serializer.data)



# get all the trips starting from a single station
@api_view(['GET'])
def station_trips_departure(request, station_id):
	trips = Trip.objects.filter(departure_station_id=station_id)
	trips_count = trips.count()
	serializer = TripSerializer(trips, many=True)
	return Response({'count': trips_count, 'trips': serializer.data})


# get all the trips ends at a single station
@api_view(['GET'])
def station_trips_return(request, station_id):
	trips = Trip.objects.filter(return_station_id=station_id)
	trips_count = trips.count()
	serializer = TripSerializer(trips, many=True)
	return Response({'count': trips_count, 'trips': serializer.data})


# get the count of the trips starts at one single station
@api_view(['GET'])
def station_trips_departure_count(request, station_id):
	trips_count = Trip.objects.filter(departure_station_id=station_id).count()
	return Response({'count': trips_count})


# get all count of the trips ends at one single station
@api_view(['GET'])
def station_trips_return_count(request, station_id):
	trips_count = Trip.objects.filter(return_station_id=station_id).count()
	return Response({'count': trips_count})




