import tkinter as tk
from tkinter import ttk, messagebox
import requests
from dotenv import load_dotenv
import os
from datetime import datetime
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
from PIL import Image, ImageTk
import json
import base64

# Load environment variables
load_dotenv()

# Get API key from environment variable
API_KEY = os.getenv('TOMORROW_API_KEY')
BASE_URL = "https://api.tomorrow.io/v4/weather/forecast"

# Define color scheme
COLORS = {
    'bg': '#1e1e2e',
    'fg': '#ffffff',
    'accent': '#89b4fa',
    'secondary': '#313244',
    'text': '#cdd6f4'
}

class ModernButton(tk.Button):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.config(
            background=COLORS['accent'],
            foreground=COLORS['bg'],
            activebackground=COLORS['secondary'],
            activeforeground=COLORS['fg'],
            relief=tk.FLAT,
            borderwidth=0,
            padx=15,
            pady=8,
            font=('Segoe UI', 10, 'bold'),
            cursor='hand2'
        )
        self.bind('<Enter>', self.on_enter)
        self.bind('<Leave>', self.on_leave)

    def on_enter(self, e):
        self.config(background=COLORS['secondary'], foreground=COLORS['fg'])

    def on_leave(self, e):
        self.config(background=COLORS['accent'], foreground=COLORS['bg'])

class ModernEntry(ttk.Entry):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.config(
            font=('Segoe UI', 11)
        )

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Weather App")
        self.root.geometry("800x600")
        self.root.configure(bg=COLORS['bg'])
        self.root.minsize(800, 600)
        
        # Configure styles
        self.configure_styles()
        
        # Create frames
        self.create_header_frame()
        self.create_search_frame()
        self.create_results_frame()
        
        # Initialize weather icons
        self.weather_icons = {
            'Clear': '☀️',
            'Partly cloudy': '⛅',
            'Cloudy': '☁️',
            'Rainy': '🌧️',
            'Snowy': '🌨️'
        }
        
        # Create loading indicator
        self.loading_var = tk.StringVar(value="")
        self.loading_label = ttk.Label(
            self.results_frame,
            textvariable=self.loading_var,
            style='Loading.TLabel'
        )
        self.loading_label.grid(row=1, column=0, columnspan=2, pady=20)

    def configure_styles(self):
        style = ttk.Style()
        style.configure('Header.TLabel',
                       background=COLORS['bg'],
                       foreground=COLORS['fg'],
                       font=('Segoe UI', 24, 'bold'))
        
        style.configure('SubHeader.TLabel',
                       background=COLORS['bg'],
                       foreground=COLORS['text'],
                       font=('Segoe UI', 14))
        
        style.configure('Info.TLabel',
                       background=COLORS['bg'],
                       foreground=COLORS['text'],
                       font=('Segoe UI', 12))
        
        style.configure('Loading.TLabel',
                       background=COLORS['bg'],
                       foreground=COLORS['accent'],
                       font=('Segoe UI', 12, 'italic'))
        
        style.configure('Weather.TFrame', background=COLORS['bg'])
        
        # Configure custom entry style
        style.configure('Search.TEntry',
                       fieldbackground=COLORS['secondary'],
                       foreground=COLORS['text'],
                       insertcolor=COLORS['text'])

    def create_header_frame(self):
        self.header_frame = ttk.Frame(self.root, style='Weather.TFrame')
        self.header_frame.pack(fill=tk.X, padx=20, pady=(20, 0))
        
        ttk.Label(
            self.header_frame,
            text="Weather Forecast",
            style='Header.TLabel'
        ).pack(anchor='center')

    def create_search_frame(self):
        self.search_frame = ttk.Frame(self.root, style='Weather.TFrame')
        self.search_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Search container
        search_container = ttk.Frame(self.search_frame, style='Weather.TFrame')
        search_container.pack(anchor='center')
        
        # Location entry
        self.location_entry = ModernEntry(
            search_container,
            width=40,
            style='Search.TEntry'
        )
        self.location_entry.grid(row=0, column=0, padx=(0, 10))
        self.location_entry.bind('<Return>', lambda e: self.get_weather())
        
        # Search button
        self.search_button = ModernButton(
            search_container,
            text="Search",
            command=self.get_weather
        )
        self.search_button.grid(row=0, column=1)
        
        # Temperature unit selection
        unit_frame = ttk.Frame(search_container, style='Weather.TFrame')
        unit_frame.grid(row=0, column=2, padx=(20, 0))
        
        self.temp_unit = tk.StringVar(value="C")
        
        style = ttk.Style()
        style.configure('Unit.TRadiobutton',
                       background=COLORS['bg'],
                       foreground=COLORS['text'],
                       font=('Segoe UI', 10))
        
        ttk.Radiobutton(
            unit_frame,
            text="°C",
            variable=self.temp_unit,
            value="C",
            style='Unit.TRadiobutton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Radiobutton(
            unit_frame,
            text="°F",
            variable=self.temp_unit,
            value="F",
            style='Unit.TRadiobutton'
        ).pack(side=tk.LEFT, padx=5)

    def create_results_frame(self):
        self.results_frame = ttk.Frame(self.root, style='Weather.TFrame')
        self.results_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Weather info labels
        self.location_label = ttk.Label(
            self.results_frame,
            text="",
            style='SubHeader.TLabel',
            justify=tk.CENTER
        )
        self.location_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Create a frame for weather details
        self.weather_details = ttk.Frame(self.results_frame, style='Weather.TFrame')
        self.weather_details.grid(row=2, column=0, columnspan=2, sticky='nsew')
        self.weather_details.grid_columnconfigure(0, weight=1)
        
        # Initialize weather info labels
        self.weather_labels = {}
        self.create_weather_label('temp', "Temperature")
        self.create_weather_label('conditions', "Conditions")
        self.create_weather_label('humidity', "Humidity")
        self.create_weather_label('wind', "Wind Speed")
        self.create_weather_label('precip', "Precipitation")
        self.create_weather_label('cloud', "Cloud Cover")

    def create_weather_label(self, key, title):
        container = ttk.Frame(self.weather_details, style='Weather.TFrame')
        container.pack(fill=tk.X, pady=5)
        
        title_label = ttk.Label(
            container,
            text=f"{title}:",
            style='Info.TLabel'
        )
        title_label.pack(side=tk.LEFT, padx=(0, 10))
        
        value_label = ttk.Label(
            container,
            text="",
            style='Info.TLabel'
        )
        value_label.pack(side=tk.LEFT)
        
        self.weather_labels[key] = value_label

    def update_weather_labels(self, weather_data):
        temp = weather_data['temperature']
        if self.temp_unit.get() == "F":
            temp = (temp * 9/5) + 32
            unit = "°F"
        else:
            unit = "°C"
        
        conditions = self.get_weather_description(weather_data)
        icon = self.weather_icons.get(conditions, '')
        
        updates = {
            'temp': f"{temp:.1f}{unit}",
            'conditions': f"{conditions} {icon}",
            'humidity': f"{weather_data['humidity']:.1f}%",
            'wind': f"{weather_data['windSpeed']:.1f} m/s",
            'precip': f"{weather_data['precipitationProbability']:.1f}%",
            'cloud': f"{weather_data['cloudCover']:.1f}%"
        }
        
        for key, value in updates.items():
            self.weather_labels[key].config(text=value)

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
        
        # Show loading indicator
        self.loading_var.set("Fetching weather data...")
        self.root.update()
        
        try:
            # Get coordinates
            lat, lon, address = self.get_coordinates(location)
            if not lat or not lon:
                self.loading_var.set("")
                messagebox.showerror("Error", "Location not found")
                return
            
            # Prepare API request
            params = {
                'location': f"{lat},{lon}",
                'apikey': API_KEY
            }
            
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Extract current conditions
            current = data['timelines']['minutely'][0]['values']
            
            # Update UI with weather data
            self.location_label.config(text=address)
            self.update_weather_labels(current)
            
            # Clear loading indicator
            self.loading_var.set("")
            
        except requests.exceptions.RequestException as e:
            self.loading_var.set("")
            messagebox.showerror("Error", f"Error fetching weather data: {str(e)}")
        except Exception as e:
            self.loading_var.set("")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
