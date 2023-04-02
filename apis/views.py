from django.shortcuts import render
import numpy as np
import pandas as pd
from .models import Station
from .models import Trip
from django.http import HttpResponse
from tqdm import tqdm
from django.db.models import Q


# import stations to stations table
def import_stations(request):
	# read the stations from CSV file to a pandas dataframe
	stations_df = pd.read_csv("static/assets/helsinkistations.csv")
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
	trips1 = pd.read_csv("static/assets/2021-05.csv")
	trips2 = pd.read_csv("static/assets/2021-06.csv")
	trips3 = pd.read_csv("static/assets/2021-07.csv")
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

