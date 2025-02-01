#!/usr/bin/env python3
import os
import click
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv('TOMORROW_API_KEY')
BASE_URL = "https://api.tomorrow.io/v4/weather/forecast"

def get_weather(location):
    """Get weather data for a location (latitude,longitude)."""
    if not API_KEY:
        raise click.ClickException("Please set your Tomorrow.io API key in the .env file")

    try:
        lat, lon = map(float, location.split(','))
    except ValueError:
        raise click.ClickException("Location must be in format: latitude,longitude (e.g., 42.3478,-71.0466)")

    params = {
        'location': f"{lat},{lon}",
        'apikey': API_KEY
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # Extract current conditions from the first timestep
        current = data['timelines']['minutely'][0]['values']
        
        weather = {
            'temperature': round(current['temperature'], 1),
            'description': get_weather_description(current),
            'humidity': round(current['humidity'], 1),
            'wind_speed': round(current['windSpeed'], 1),
            'precipitation': round(current['precipitationProbability'], 1),
            'cloud_cover': round(current['cloudCover'], 1)
        }
        return weather

    except requests.exceptions.RequestException as e:
        raise click.ClickException(f"Error fetching weather data: {str(e)}")

def get_weather_description(conditions):
    """Generate a weather description based on conditions."""
    if conditions['precipitationProbability'] > 50:
        if conditions['temperature'] <= 0:
            return "Snowy"
        return "Rainy"
    elif conditions['cloudCover'] > 70:
        return "Cloudy"
    elif conditions['cloudCover'] > 30:
        return "Partly cloudy"
    else:
        return "Clear"

@click.command()
@click.argument('location')
@click.option('--celsius', '-c', is_flag=True, help='Show temperature in Celsius (default)')
@click.option('--fahrenheit', '-f', is_flag=True, help='Show temperature in Fahrenheit')
def main(location, celsius, fahrenheit):
    """
    Get current weather information for a LOCATION (latitude,longitude).
    
    Example: python weather.py "42.3478,-71.0466"
    """
    try:
        weather_data = get_weather(location)
        
        # Display the weather information
        click.echo(f"\nWeather for location {location}:")
        click.echo("------------------------")
        
        temp = weather_data['temperature']
        if fahrenheit:
            temp = (temp * 9/5) + 32
            click.echo(f"Temperature: {temp}°F")
        else:
            click.echo(f"Temperature: {temp}°C")
            
        click.echo(f"Conditions: {weather_data['description']}")
        click.echo(f"Humidity: {weather_data['humidity']}%")
        click.echo(f"Wind Speed: {weather_data['wind_speed']} m/s")
        click.echo(f"Precipitation Probability: {weather_data['precipitation']}%")
        click.echo(f"Cloud Cover: {weather_data['cloud_cover']}%")
        
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

if __name__ == '__main__':
    main()
