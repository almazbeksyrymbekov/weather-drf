import requests
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from config import settings
from django.core.cache import cache


@api_view(['GET'])
def weather_view(request: Request):
    city = request.query_params.get('city', None)
    if not city:
        return Response({'message': 'Please provide city'}, status=status.HTTP_400_BAD_REQUEST)
    cached_data = cache.get(city)
    if cached_data:
        return Response(cached_data)
    api_key_url = f'https://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': city,
        'units': 'metric',
        'appid': settings.API_KEY
    }
    response = requests.get(api_key_url, params=params)
    if response.status_code != 200:
        return Response({'error': 'Something went wrong'}, status=response.status_code)
    data = response.json()
    weather_data = {
        'temperature': data['main']['temp'],
        'pressure': data['main']['pressure'],
        'wind_speed': data['wind']['speed']
    }
    cache.set(city, weather_data, timeout=1800)
    return Response(weather_data, status=status.HTTP_200_OK)
