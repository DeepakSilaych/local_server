
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

class CheckView(APIView):
    def get(self, request):
        stations = AWSStation.objects.all()
        for station in stations:
            
            # fetch 15min interval data for last 24 hours
            stationdata = StationData.objects.filter(station=station, timestamp__gte=now()-timedelta(days=5)).values('timestamp').annotate(rainfall=Sum('rainfall')).order_by('timestamp')
            stationdata = pd.DataFrame(stationdata)

            #save in puja folder
            os.makedirs('puja', exist_ok=True)
            stationdata.to_csv(f'puja/{station.name}.csv', index=False)
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