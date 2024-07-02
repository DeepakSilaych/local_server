from django.contrib import admin
from django.urls import path, include
from crowdsource import views as crowdsource

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tweets/', crowdsource.tweet.as_view()),
    path('', include('awsstations.urls')),
]
