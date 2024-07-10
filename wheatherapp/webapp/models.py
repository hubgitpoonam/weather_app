from django.db import models

# Create your models here.
class Weather(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    weather_description = models.CharField(max_length=100)
    humidity = models.IntegerField()
    wind_speed = models.FloatField()

    def __str__(self):
        return self.city
        #return f"{self.city} - {self.weather}"