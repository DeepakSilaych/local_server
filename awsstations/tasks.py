from celery import shared_task
import logging
from django.utils import timezone
from datetime import datetime
import pytz
from django.shortcuts import get_object_or_404

from .models import AWSStation, StationData, TrainStation
from .utils.aws import fetch_aws_data
from .utils.gfs import download_gfs_data
from .utils.hourly_prediction import predict_hourly
from .utils.DayWisePrediction import dailyprediction



logger = logging.getLogger(__name__)

@shared_task
def scheduled_15_min():
    fetch_and_store_data()
    update_trainstations()
    logger.info("-----------------------15 Min Task Done")
    
# free up the memory after function is done to optimize the performance
@shared_task
def scheduled_daily():
    download_gfs_data()
    dailyprediction()
    logger.info("++++++++++++++++++++++++Daily Prediction Done")
    

@shared_task
def scheduled_hourly():
    predict_hourly()
    logger.info("************************Hourly Prediction Done")
#---------------------------------------------------------------------------------------------------------------------
def fetch_and_store_data():
    stations = AWSStation.objects.all()
    for station in stations: 
        data = fetch_aws_data(station.station_id)
        if data:
            save_station_data(station, data)

def save_station_data(station, data):
    rainfall = data.get('rain', 0)
    temperature = data.get('temp_out', 0)
    humidity = data.get('out_humidity', 0)
    wind_speed = data.get('wind_speed', 0)

    station.curr_temp = temperature
    station.curr_windspeed = wind_speed
    station.save()

    
    StationData.objects.create(
        station=station,
        rainfall=rainfall,
        temperature=temperature,
        humidity=humidity,
        wind_speed=wind_speed,
        timestamp=timezone.now()
    )

def update_trainstations():
    all_stations = TrainStation.objects.all()
    for station in all_stations:
        last_data = StationData.objects.filter(station=station.neareststation).order_by('-timestamp')[:4]
        if last_data:
            max_rainfall = max(data.rainfall for data in last_data)
            if max_rainfall > 20:
                station.WarningLevel = 3
            elif max_rainfall > 15:
                station.WarningLevel = 2
            elif max_rainfall > 10:
                station.WarningLevel = 1
            else:
                station.WarningLevel = 0
           
