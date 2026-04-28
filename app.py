import os
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("WEATHER_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    data = request.json
    city = data.get('city')
    
    if not city:
        return jsonify({"error": "Please enter a city name"}), 400

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url)
        weather_data = response.json()

        if response.status_code != 200:
            return jsonify({"error": weather_data.get("message", "City not found")}), 404

        # Clean data for the frontend
        payload = {
            "name": weather_data["name"],
            "country": weather_data["sys"]["country"],
            "temp": round(weather_data["main"]["temp"]),
            "feels_like": round(weather_data["main"]["feels_like"]),
            "humidity": weather_data["main"]["humidity"],
            "wind": weather_data["wind"]["speed"],
            "condition": weather_data["weather"][0]["main"], # Rain, Clouds, Clear, etc.
            "description": weather_data["weather"][0]["description"].capitalize(),
            "icon": weather_data["weather"][0]["icon"]
        }
        return jsonify(payload)

    except Exception as e:
        return jsonify({"error": "Internal Server Error"}), 500

if __name__ == '__main__':
    app.run(debug=True)