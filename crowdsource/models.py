from django.db import models


# form data model
class CSFormData(models.Model):
    
    location = models.TextField(blank=True, null=True)
    feedback = models.TextField(blank=True, null=True)

    feet = models.IntegerField(blank=True, null=True)
    inch = models.IntegerField(blank=True, null=True)

    timestamp = models.DateTimeField(auto_now=True, null=True)

    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.location + " " + str(self.feet) + "ft " + str(self.inch) + "in"
    

class Tweet(models.Model):
    text = models.CharField(max_length=200)
    date = models.DateField()
    sentiment = models.BooleanField() # True for positive, False for negative
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.text
    