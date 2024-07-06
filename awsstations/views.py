
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


class CheckView(APIView):
    def get(self, request):
        df = pd.read_csv('predict.csv')
        temp = []

        # delete all previous data with timestamp of 2024-06-30 00:00:00
# 2024-07-01 00:00:00
# 2024-07-02 00:00:00
# 2024-07-03 00:00:00
# 2024-07-04 00:00:00
# 2024-07-05 00:00:00
# 2024-07-06 00:00:00
        
        data = StationData.objects.filter(timestamp__gte='2024-06-30 00:00:00', timestamp__lt='2024-07-06 00:00:00')
        data.delete()
        
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