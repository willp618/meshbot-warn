import requests
from datetime import datetime

class WxFetcher:
    def __init__(self, location):
        self.location = location

    def get_coordinates(self):
        url = f"https://geocoding-api.open-meteo.com/v1/search?name={self.location}&count=1"
        response = requests.get(url)
        if response.status_code == 200:
            try:
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
            except ValueError:
                return None, None, "Invalid JSON"
        else:
            return None, None, f"Geocoding failed (HTTP {response.status_code})"

    def get_weather(self):
        lat, lon, location_name = self.get_coordinates()
        if lat is None or lon is None:
            return f"Failed to resolve location: {location_name}"

        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}&current_weather=true"
            f"&hourly=relativehumidity_2m,precipitation,pressure_msl,"
            f"windgusts_10m,uv_index,apparent_temperature"
            f"&windspeed_unit=mph"
            f"&timezone=auto"
        )
        response = requests.get(url)
        if response.status_code != 200:
            return f"Failed to fetch weather data. HTTP Status Code: {response.status_code}"

        try:
            data = response.json()
        except ValueError as e:
            return f"Error parsing weather data: {e}"

        current = data.get("current_weather", {})
        if not current:
            return "Current weather data not available."

        time_now = current.get("time")
        temperature = current.get("temperature", "N/A")
        windspeed = current.get("windspeed", "N/A")
        winddir = current.get("winddirection", "N/A")
        condition_code = current.get("weathercode", "N/A")

        # Defaults
        humidity = "N/A"
        pressure = "N/A"
        precip = "N/A"
        gust = "N/A"
        uv = "N/A"
        apparent_temp = "N/A"

        def parse_time(ts):
            return datetime.strptime(ts, "%Y-%m-%dT%H:%M")

        hourly = data.get("hourly", {})
        hourly_times = hourly.get("time", [])
        if hourly_times:
            current_time_dt = parse_time(time_now)
            parsed_times = [parse_time(t) for t in hourly_times]

            closest_index = min(
                range(len(parsed_times)),
                key=lambda i: abs(parsed_times[i] - current_time_dt)
            )

            humidity = hourly.get("relativehumidity_2m", ["N/A"])[closest_index]
            pressure = hourly.get("pressure_msl", ["N/A"])[closest_index]
            precip = hourly.get("precipitation", ["N/A"])[closest_index]
            gust = hourly.get("windgusts_10m", ["N/A"])[closest_index]
            uv = hourly.get("uv_index", ["N/A"])[closest_index]
            apparent_temp = hourly.get("apparent_temperature", ["N/A"])[closest_index]

        # Weather condition codes
        weather_emojis = {
            0: "☀️ Clear sky",
            1: "🌤️ Mainly clear",
            2: "⛅ Partly cloudy",
            3: "☁️ Overcast",
            45: "🌫️ Fog",
            48: "🌫️ Rime fog",
            51: "🌧️ Light drizzle",
            53: "🌧️ Moderate drizzle",
            55: "🌧️ Dense drizzle",
            61: "🌧️ Light rain",
            63: "🌧️ Moderate rain",
            65: "🌧️ Heavy rain",
            71: "❄️ Light snow",
            73: "❄️ Moderate snow",
            75: "❄️ Heavy snow",
            80: "🌧️ Rain showers",
            81: "🌧️ Heavy rain showers",
            95: "🌩️ Thunderstorm"
        }
        condition = weather_emojis.get(condition_code, "🌥️ Unknown")

        # Wind direction arrow and compass abbreviation
        detailed_compass = [
            (0, "N", "↑"), (22.5, "NNE", "↑"), (45, "NE", "↗"), (67.5, "ENE", "↗"),
            (90, "E", "→"), (112.5, "ESE", "↘"), (135, "SE", "↘"), (157.5, "SSE", "↓"),
            (180, "S", "↓"), (202.5, "SSW", "↓"), (225, "SW", "↙"), (247.5, "WSW", "↙"),
            (270, "W", "←"), (292.5, "WNW", "↖"), (315, "NW", "↖"), (337.5, "NNW", "↑"),
            (360, "N", "↑")
        ]

        def get_compass_direction(degrees):
            for i in range(len(detailed_compass) - 1):
                if degrees >= detailed_compass[i][0] and degrees < detailed_compass[i + 1][0]:
                    return detailed_compass[i][1], detailed_compass[i][2]
            return "N", "↑"

        try:
            direction_text, wind_arrow = get_compass_direction(winddir)
        except:
            direction_text, wind_arrow = "?", "↗"

        # Output
        output = f"{location_name}\n"
        output += f"{condition}\n"
        output += f"🌡️ Temp: {temperature}°C\n"
        output += f"🥵 Feels Like: {apparent_temp}°C\n"
        output += f"💧 Humidity: {humidity}%\n"
        output += f"🌬️ Wind: {wind_arrow} {windspeed} mph ({direction_text})\n"
        output += f"🌪️ Gusts: {gust} mph\n"
        output += f"🌨️ Precipitation: {precip} mm\n"
        output += f"📈 Pressure: {pressure} hPa\n"
        output += f"🔆 UV Index: {uv}\n"

        return output

# Example usage
if __name__ == "__main__":
    location = "bridgnorth"
    weather_fetcher = WxFetcher(location)
    print(weather_fetcher.get_weather())
