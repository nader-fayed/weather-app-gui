# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Modern Weather App with GUI

Features:
- Beautiful animated GUI interface
- Real-time weather data from Tomorrow.io API
- Location detection
- Temperature unit conversion
- Detailed weather information display
- Executable distribution"

# Create new repository on GitHub using GitHub CLI
gh repo create weather-app-gui --public --description "A modern weather application with animated GUI, built with Python and Tomorrow.io API" --source=. --remote=origin --push
