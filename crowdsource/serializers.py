from rest_framework import serializers
from .models import CSFormData, Tweet

class CSFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSFormData
        fields = ['latitude', 'longitude', 'feet', 'inch', 'location', 'timestamp']

class FormDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CSFormData
        fields = '__all__'

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = '__all__'