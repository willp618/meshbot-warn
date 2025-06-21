import requests
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class WxFetcher:
    def __init__(self, location):
        self.location = location

    def get_coordinates(self):
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={self.location}&count=1"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            results = data.get("results")
            if results:
                lat = results[0]["latitude"]
                lon = results[0]["longitude"]
                name = results[0]["name"]
                country = results[0].get("country", "")
                return lat, lon, f"{name}, {country}"
            else:
                return None, None, "Unknown location"
        except Exception as e:
            logging.error(f"Geocoding error: {e}")
            return None, None, f"Geocoding failed: {e}"

    def get_forecast(self):
        lat, lon, location_name = self.get_coordinates()
        if lat is None or lon is None:
            return f"Failed to resolve location: {location_name}"

        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_sum,"
            f"windspeed_10m_max,winddirection_10m_dominant,uv_index_max"
            f"&timezone=auto"
        )

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            logging.error(f"Forecast fetch error: {e}")
            return f"Failed to fetch forecast data: {e}"

        daily = data.get("daily", {})
        if not daily:
            return "Forecast data not available."

        dates = daily.get("time", [])
        weather_codes = daily.get("weathercode", [])
        t_max = daily.get("temperature_2m_max", [])
        t_min = daily.get("temperature_2m_min", [])
        precip = daily.get("precipitation_sum", [])
        wind_speed = daily.get("windspeed_10m_max", [])
        wind_dir = daily.get("winddirection_10m_dominant", [])
        uv_index = daily.get("uv_index_max", [])

        weather_emojis = {
            0: "☀️ Clear",
            1: "🌤️ Mainly clear",
            2: "⛅ Partly cloudy",
            3: "☁️ Overcast",
            45: "🌫️ Fog",
            48: "🌫️ Rime fog",
            51: "🌦️ Light drizzle",
            53: "🌦️ Moderate drizzle",
            55: "🌧️ Dense drizzle",
            61: "🌧️ Light rain",
            63: "🌧️ Moderate rain",
            65: "🌧️ Heavy rain",
            71: "❄️ Light snow",
            73: "❄️ Moderate snow",
            75: "❄️ Heavy snow",
            80: "🌦️ Rain showers",
            81: "🌧️ Heavy rain showers",
            82: "🌧️ Violent rain showers",
            85: "🌨️ Snow showers",
            86: "❄️ Heavy snow showers",
            95: "🌩️ Thunderstorm",
            96: "⛈️ Thunderstorm w/ slight hail",
            99: "⛈️ Thunderstorm w/ heavy hail"
        }

        direction_arrows = ["↑", "↗", "→", "↘", "↓", "↙", "←", "↖"]

        output = f"📍 {location_name} - 5-Day Forecast:\n\n"
        for i in range(min(5, len(dates))):
            try:
                date_obj = datetime.strptime(dates[i], "%Y-%m-%d")
                date_str = date_obj.strftime("%A, %b %d")
            except:
                date_str = dates[i]

            code = weather_codes[i]
            condition = weather_emojis.get(code, "🌥️ Unknown")

            try:
                idx = int(((wind_dir[i] + 22.5) % 360) / 45)
                wind_arrow = direction_arrows[idx]
            except:
                wind_arrow = "↗"

            output += f"📅 {date_str}\n"
            output += f"{condition}\n"
            output += f"🌡️ {t_min[i]}°C / {t_max[i]}°C\n"
            output += f"🌬️ {wind_arrow} {wind_speed[i]} mph\n"
            output += f"🌧️ {precip[i]} mm\n"
            output += f"🌞 UV Index: {uv_index[i]}\n"
            output += "----------------------\n"

        return output

# Example usage
if __name__ == "__main__":
    location = "bridgnorth"
    weather_fetcher = WxFetcher(location)
    print(weather_fetcher.get_forecast())
