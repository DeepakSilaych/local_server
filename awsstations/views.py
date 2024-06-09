
# Create your views here.
from .models import AWSStation, StationData, TrainStation
from .serializers import AWSStationSerializer, StationDataSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
import pandas as pd


def get_predictions(request):
    # predict_hourly()
    # download_gfs_data()     
    # predict_day1()
    # predict_day2()
    # predict_day3()
    return Response({'message': 'Predictions generated'})


class StationListView(APIView):
    def get(self, request):
        stations = AWSStation.objects.all()
        serializer = AWSStationSerializer(stations, many=True)
        return Response(serializer.data)

class StationDetailView(APIView):
    def get(self, request, station_id):
        station = AWSStation.objects.get(id=station_id)
        serializer = AWSStationSerializer(station)
        
        station_data = StationData.objects.filter(station_id=station_id)

        # last 30 data only
        station_data = station_data.order_by('-timestamp')[:30]
        station_data = station_data[::-1]
        station_data = StationDataSerializer(station_data, many=True)
        
        return Response({'station': serializer.data, 'data': station_data.data})
    
class Savedataincsv(APIView):
    def get(self, request):
        data = StationData.objects.all()
        pd = pd.DataFrame(data)
        pd.to_csv('data.csv')