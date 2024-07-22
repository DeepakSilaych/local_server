
# Create your views here.
from .models import AWSStation, StationData, DaywisePrediction, HourlyPrediction, TrainStation
from .serializers import AWSStationSerializer, TrainStationSerializer ,StationDataSerializer, DaywisePredictionSerializer, HourlyPredictionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models.functions import TruncDate, TruncHour
from django.db.models import Sum
from django.utils.timezone import now, timedelta
import pandas as pd
from .utils.DayWisePrediction import dailyprediction
from .utils.gfs import download_gfs_data
from .utils.hourly_prediction import predict_hourly
from .tasks import scheduled_15_min, scheduled_hourly, scheduled_daily, update_trainstations
import os
from datetime import datetime
import csv
from io import StringIO
from rest_framework import status
from django.utils.timezone import make_aware



class CheckView(APIView):
    def get(self, request):
        data = [
            {"Place": "Andheri", "18/07": 103.63, "19/07": 70.81, "20/07": 117.33},
            {"Place": "B ward", "18/07": 63.21, "19/07": 49.66, "20/07": 79.26},
            {"Place": "Bandra", "18/07": 86.76, "19/07": 93.85, "20/07": 115.3},
            {"Place": "Byculla", "18/07": 56.52, "19/07": 54.47, "20/07": 69.17},
            {"Place": "C ward", "18/07": 48.74, "19/07": 31.77, "20/07": 73.36},
            {"Place": "Chembur", "18/07": 87.53, "19/07": 94.12, "20/07": 97.37},
            {"Place": "Chincholi", "18/07": 87.56, "19/07": 93.67, "20/07": 157.15},
            {"Place": "Colaba", "18/07": 47.94, "19/07": 85.36, "20/07": 84.72},
            {"Place": "D Ward", "18/07": 61.99, "19/07": 57.71, "20/07": 59.99},
            {"Place": "Dahisar", "18/07": 99.17, "19/07": 87.39, "20/07": 142.19},
            {"Place": "Dindoshi", "18/07": 94.69, "19/07": 103.36, "20/07": 98.18},
            {"Place": "F North", "18/07": 92.5, "19/07": 89.61, "20/07": 91.91},
            {"Place": "F South", "18/07": 81.29, "19/07": 81.29, "20/07": 81.29},
            {"Place": "G South", "18/07": 81.93, "19/07": 88.3, "20/07": 95.83},
            {"Place": "Gowanpada", "18/07": 96.06, "19/07": 45.5, "20/07": 93.08},
            {"Place": "H West ward", "18/07": 81.36, "19/07": 88.89, "20/07": 88.21},
            {"Place": "K East ward", "18/07": 93.2, "19/07": 99.81, "20/07": 134.07},
            {"Place": "K West ward", "18/07": 110.23, "19/07": 73.59, "20/07": 147.55},
            {"Place": "Kandivali", "18/07": 117.79, "19/07": 106.23, "20/07": 125.41},
            {"Place": "Kurla", "18/07": 65.26, "19/07": 95.86, "20/07": 94.91},
            {"Place": "L ward", "18/07": 94.72, "19/07": 89.51, "20/07": 94.72},
            {"Place": "Marol", "18/07": 88.23, "19/07": 93.5, "20/07": 106.13},
            {"Place": "MCGM 1", "18/07": 47.57, "19/07": 37.23, "20/07": 85.88},
            {"Place": "M West ward", "18/07": 46.52, "19/07": 42.51, "20/07": 69.57},
            {"Place": "Malvani", "18/07": 38.74, "19/07": 86.38, "20/07": 87},
            {"Place": "Memonwada", "18/07": 69.27, "19/07": 42.73, "20/07": 106.13},
            {"Place": "Mulund", "18/07": 55.61, "19/07": 86, "20/07": 133.87},
            {"Place": "N ward", "18/07": 86.78, "19/07": 91.97, "20/07": 91.34},
            {"Place": "Nariman Fire", "18/07": 34.12, "19/07": 40.5, "20/07": 68.62},
            {"Place": "Thakare natya", "18/07": 114.68, "19/07": 101.54, "20/07": 144.73},
            {"Place": "Rawali camp", "18/07": 61.15, "19/07": 71.9, "20/07": 81.19},
            {"Place": "SWD Workshop dadar", "18/07": 71.19, "19/07": 70.54, "20/07": 75.44},
            {"Place": "S ward", "18/07": 75.06, "19/07": 88, "20/07": 99},
            {"Place": "Vikhroli", "18/07": 75.38, "19/07": 122.28, "20/07": 77.35},
            {"Place": "vileparle W", "18/07": 74.22, "19/07": 92.39, "20/07": 70},
            {"Place": "Worli", "18/07": 84.79, "19/07": 84.79, "20/07": 85}
        ]

        for d in data:
            name = d['Place']
            station = AWSStation.objects.get(name=name)

            for i in ['18/07', '19/07', '20/07']:
                timestamp = datetime.strftime(datetime.strptime(i, '%d/%m'), '%Y-%m-%d 23:59:00')
                DaywisePrediction.objects.create(station=station, timestamp=timestamp, day1_rainfall=d[i], day2_rainfall=d[i], day3_rainfall=d[i])

        return Response({   
            'status': 'done'
        })
    
class Train(APIView):
    def get(self, request):
        update_trainstations()
        return Response({
            'status': 'done'
        })
    
class GFSDataView(APIView):
    def get(self, request):
        download_gfs_data()
        return Response({
            'status': 'done'
        })

class HourlyPredictionView(APIView):
    def get(self, request):
        predict_hourly()
        return Response({
            'status': 'done'
        })

class DailyPredictionView(APIView):
    def get(self, request):
        dailyprediction()
        return Response({
            'status': 'done'
        })

class UpadeStationData(APIView):
    def get(self, request):
        for station in AWSStation.objects.all():
            station.rainfall = DaywisePrediction.objects.filter(station=station).order_by('-timestamp').first().day1_rainfall
            station.save()

class UploadData(APIView):
    def get(self, request):
        df = pd.read_csv('data.csv')
        temp = []
        
        for index, row in df.iterrows():
            timestamp = datetime.strptime(row['DateTime'], '%Y-%m-%d %H:%M:%S')
            for station in AWSStation.objects.all():
                StationData.objects.create(station=station, timestamp=timestamp, rainfall=row[station.name])
                temp.append({
                    'station': station.name,
                    'timestamp': timestamp,
                    'rainfall': row[station.name]
                })
        
        return Response({
            'status': 'done',
            'data': temp
        })