# webapp/views.py

import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from .models import Weather

def get_weather(request):
    Base_Url = "http://api.openweathermap.org/data/2.5/weather?"
    API_KEY = "1ee2b321ddb0cca538bcba328aba9022"  # Use your actual API key here
    cities = ["London", "Paris", "New York", "Tokyo", "Sydney"]  # List of cities

    weather_data_list = []

    for city in cities:
        url = Base_Url + "appid=" + API_KEY + "&q=" + city
        response = requests.get(url)
        data = response.json()


        # Convert temperature from Kelvin to Celsius
        temperature_celsius = data["main"]["temp"] - 273.15
        temperature_celsius = round(temperature_celsius, 2) 

        weather_data = {
            "city": data["name"],
            "temperature": temperature_celsius,
            "weather_description": data["weather"][0]["description"],  # Updated field name
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }

        # Save the data to the database
        Weather.objects.create(
            city=weather_data['city'],
            temperature=temperature_celsius,
            weather_description=weather_data['weather_description'],  # Updated field name
            humidity=weather_data['humidity'],
            wind_speed=weather_data['wind_speed']
        )

        weather_data_list.append(weather_data)

    return JsonResponse(weather_data_list, safe=False)


def weather_list(request):
    weather_data = Weather.objects.all()
    return render(request, 'weatherapp/weather_list.html', {'weather_data': weather_data})

@csrf_exempt
def weather_detail(request, pk):
    weather = get_object_or_404(Weather, pk=pk)
    return JsonResponse({
        'city': weather.city,
        'temperature': weather.temperature,
        'weather_description': weather.weather_description,
        'humidity': weather.humidity,
        'wind_speed': weather.wind_speed
    })

@csrf_exempt
def weather_create(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        weather = Weather.objects.create(
            city=data['city'],
            temperature=data['temperature'],
            weather_description=data['weather_description'],
            humidity=data['humidity'],
            wind_speed=data['wind_speed']
        )
        return JsonResponse({'message': 'Weather created successfully!'})
    return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def weather_update(request, pk):
    weather = get_object_or_404(Weather, pk=pk)
    if request.method == 'PUT':
        data = json.loads(request.body)
        weather.city = data.get('city', weather.city)
        weather.temperature = data.get('temperature', weather.temperature)
        weather.weather_description = data.get('weather_description', weather.weather_description)
        weather.humidity = data.get('humidity', weather.humidity)
        weather.wind_speed = data.get('wind_speed', weather.wind_speed)
        weather.save()
        return JsonResponse({'message': 'Weather updated successfully!'})
    return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def weather_delete(request, pk):
    weather = get_object_or_404(Weather, pk=pk)
    if request.method == 'DELETE':
        weather.delete()
        return JsonResponse({'message': 'Weather deleted successfully!'})
    return JsonResponse({'error': 'Invalid request method'})