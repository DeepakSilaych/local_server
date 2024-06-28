# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('check/', views.CheckView.as_view()),
    path('gfs/', views.GFSDataView.as_view()),
    path('hourly/', views.HourlyPredictionView.as_view()),
    path('daily/', views.DailyPredictionView.as_view()),
    path('train/', views.Train.as_view())
]
