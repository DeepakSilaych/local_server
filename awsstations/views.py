
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

class CheckView(APIView):
    def get(self, request):
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