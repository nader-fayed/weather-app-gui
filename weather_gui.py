import tkinter as tk
from tkinter import ttk, messagebox
import requests
from dotenv import load_dotenv
import os
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

# Load environment variables
load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv('TOMORROW_API_KEY')
BASE_URL = "https://api.tomorrow.io/v4/weather/forecast"

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')
        
        # Configure style
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 10))
        style.configure('Header.TLabel', font=('Helvetica', 12, 'bold'))
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Search frame
        self.search_frame = ttk.Frame(self.main_frame)
        self.search_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky=tk.W+tk.E)
        
        # Location entry
        ttk.Label(self.search_frame, text="Enter Location:", style='Header.TLabel').grid(row=0, column=0, padx=5)
        self.location_entry = ttk.Entry(self.search_frame, width=40)
        self.location_entry.grid(row=0, column=1, padx=5)
        
        # Search button
        self.search_button = ttk.Button(self.search_frame, text="Search", command=self.get_weather)
        self.search_button.grid(row=0, column=2, padx=5)
        
        # Temperature unit selection
        self.temp_unit = tk.StringVar(value="C")
        self.celsius_radio = ttk.Radiobutton(self.search_frame, text="Celsius", variable=self.temp_unit, value="C")
        self.fahrenheit_radio = ttk.Radiobutton(self.search_frame, text="Fahrenheit", variable=self.temp_unit, value="F")
        self.celsius_radio.grid(row=0, column=3, padx=5)
        self.fahrenheit_radio.grid(row=0, column=4, padx=5)
        
        # Results frame
        self.results_frame = ttk.Frame(self.main_frame, padding="10")
        self.results_frame.grid(row=1, column=0, columnspan=2, sticky=tk.W+tk.E)
        
        # Weather info labels
        self.location_label = ttk.Label(self.results_frame, text="", style='Header.TLabel')
        self.location_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        self.temp_label = ttk.Label(self.results_frame, text="")
        self.temp_label.grid(row=1, column=0, sticky=tk.W)
        
        self.conditions_label = ttk.Label(self.results_frame, text="")
        self.conditions_label.grid(row=2, column=0, sticky=tk.W)
        
        self.humidity_label = ttk.Label(self.results_frame, text="")
        self.humidity_label.grid(row=3, column=0, sticky=tk.W)
        
        self.wind_label = ttk.Label(self.results_frame, text="")
        self.wind_label.grid(row=4, column=0, sticky=tk.W)
        
        self.precip_label = ttk.Label(self.results_frame, text="")
        self.precip_label.grid(row=5, column=0, sticky=tk.W)
        
        self.cloud_label = ttk.Label(self.results_frame, text="")
        self.cloud_label.grid(row=6, column=0, sticky=tk.W)
        
        # Bind Enter key to search
        self.location_entry.bind('<Return>', lambda e: self.get_weather())

    def get_coordinates(self, location):
        """Get coordinates for a location using geopy."""
        try:
            geolocator = Nominatim(user_agent="weather_app")
            location_data = geolocator.geocode(location)
            if location_data:
                return location_data.latitude, location_data.longitude, location_data.address
            return None, None, None
        except GeocoderTimedOut:
            messagebox.showerror("Error", "Geocoding service timed out. Please try again.")
            return None, None, None

    def get_weather_description(self, conditions):
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

    def get_weather(self):
        """Get weather data and update the UI."""
        location = self.location_entry.get().strip()
        if not location:
            messagebox.showwarning("Warning", "Please enter a location")
            return
            
        # Get coordinates
        lat, lon, address = self.get_coordinates(location)
        if not lat or not lon:
            messagebox.showerror("Error", "Location not found")
            return
            
        # Prepare API request
        params = {
            'location': f"{lat},{lon}",
            'apikey': API_KEY
        }
        
        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Extract current conditions
            current = data['timelines']['minutely'][0]['values']
            
            # Update UI with weather data
            self.location_label.config(text=f"Weather for {address}")
            
            # Temperature
            temp = current['temperature']
            if self.temp_unit.get() == "F":
                temp = (temp * 9/5) + 32
                unit = "°F"
            else:
                unit = "°C"
            
            self.temp_label.config(text=f"Temperature: {temp:.1f}{unit}")
            self.conditions_label.config(text=f"Conditions: {self.get_weather_description(current)}")
            self.humidity_label.config(text=f"Humidity: {current['humidity']:.1f}%")
            self.wind_label.config(text=f"Wind Speed: {current['windSpeed']:.1f} m/s")
            self.precip_label.config(text=f"Precipitation Probability: {current['precipitationProbability']:.1f}%")
            self.cloud_label.config(text=f"Cloud Cover: {current['cloudCover']:.1f}%")
            
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Error fetching weather data: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
