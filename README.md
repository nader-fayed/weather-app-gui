# Weather App GUI 🌤️

[![License: Educational](https://img.shields.io/badge/License-Educational%20Use%20Only-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

A modern, animated weather application with a beautiful GUI interface. Get real-time weather information for any location with a sleek, user-friendly design.

> **Educational Project**: This application was developed as part of my first-year Computer & Information Sciences studies at Egyptian E-Learning University (EUI). It is intended for educational purposes only and may not be used for commercial purposes.

![Weather App Screenshot](screenshots/app.png)

## ✨ Features

- 🎨 Modern, animated GUI interface
- 🌍 Real-time weather data from Tomorrow.io API
- 📍 Automatic location detection
- 🌡️ Temperature unit conversion (Celsius/Fahrenheit)
- 🎯 Detailed weather information:
  - Temperature
  - Weather conditions with animated icons
  - Humidity
  - Wind speed
  - Precipitation probability
  - Cloud cover
- 💫 Smooth animations and transitions
- 📦 Available as standalone executable

## 🚀 Quick Start

### Using the Executable

1. Download the latest release from the [Releases](https://github.com/nader-fayed/weather-app-gui/releases) page
2. Extract the ZIP file
3. Run `WeatherApp.exe`

### Running from Source

1. Clone the repository:
```bash
git clone https://github.com/nader-fayed/weather-app-gui.git
cd weather-app-gui
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your Tomorrow.io API key:
```
TOMORROW_API_KEY=your_api_key_here
```

4. Run the application:
```bash
python weather_gui_animated.py
```

## 🔧 Configuration

The app uses the Tomorrow.io API for weather data. To get an API key:
1. Sign up at [Tomorrow.io](https://www.tomorrow.io/)
2. Navigate to your account settings
3. Generate an API key
4. Add the key to your `.env` file

## 🎯 Usage

1. **Search Location**: Enter a city name or address in the search box
2. **Get Current Location**: Click the "📍 Get My Location" button
3. **Change Temperature Unit**: Toggle between Celsius and Fahrenheit
4. **View Weather Details**: See comprehensive weather information with animated icons

## 🛠️ Development

### Prerequisites
- Python 3.11 or higher
- pip package manager
- Git

### Setting up Development Environment

1. Clone the repository:
```bash
git clone https://github.com/nader-fayed/weather-app-gui.git
cd weather-app-gui
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -r requirements.txt
```

### Building the Executable

```bash
python -m PyInstaller weather.spec
```

## 📝 Contributing

Contributions for educational purposes are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed for **EDUCATIONAL USE ONLY** - see the [LICENSE](LICENSE) file for details.

**Important Notice:**
- Commercial use is strictly prohibited
- Selling or buying this software or any derivatives is forbidden
- This software is intended for educational purposes only

## 📞 Contact & Support

- **Author**: Nader Fayed
- **Education**: First Year CIS Student at Egypt University for Informatics (EUI)
- **Email**: naderfayed166@gmail.com
- **GitHub**: [@nader-fayed](https://github.com/nader-fayed)

## 🙏 Acknowledgments

- [Tomorrow.io](https://www.tomorrow.io/) for providing the weather API
- [Tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI framework
- All contributors who help improve this project
- Egyptian E-Learning University (EUI) for the educational opportunity

---

Made with ❤️ by [Nader Fayed](https://github.com/nader-fayed) | First Year CIS Student at EUI
