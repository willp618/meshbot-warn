import requests
from datetime import datetime

class WxFetcher:
    def __init__(self, location):
        if "," in location:
            parts = location.split(",", 1)
            self.location = parts[0].strip()
            self.country_code = parts[1].strip().upper()
        else:
            self.location = location.strip()
            self.country_code = None

    def get_coordinates(self):
        base_url = "https://geocoding-api.open-meteo.com/v1/search"
        url = f"{base_url}?name={self.location}&count=5"
        response = requests.get(url)

        if response.status_code == 200:
            try:
                data = response.json()
                results = data.get("results", [])
                if not results:
                    return None, None, "Unknown location"

                # Prefer exact country match if user provided a code
                if self.country_code:
                    for result in results:
                        if result.get("country_code", "").upper() == self.country_code:
                            lat = result["latitude"]
                            lon = result["longitude"]
                            name = result["name"]
                            country = result.get("country", "")
                            return lat, lon, f"{name}, {country}"

                # Fallback to first result if no country match
                lat = results[0]["latitude"]
                lon = results[0]["longitude"]
                name = results[0]["name"]
                country = results[0].get("country", "")
                return lat, lon, f"{name}, {country}"
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
            f"&hourly=relativehumidity_2m,precipitation,pressure_msl"
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

        humidity = "N/A"
        pressure = "N/A"
        precip = "N/A"

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

            humidity = hourly["relativehumidity_2m"][closest_index]
            pressure = hourly["pressure_msl"][closest_index]
            precip = hourly["precipitation"][closest_index]

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
            return "N", "↑"  # fallback

        try:
            direction_text, wind_arrow = get_compass_direction(winddir)
        except:
            direction_text, wind_arrow = "?", "↗"

        output = f"{location_name}\n"
        output += f"{condition}\n"
        output += f"🌡️ Temp: {temperature}°C\n"
        output += f"💧 Humidity: {humidity}%\n"
        output += f"🌬️ Wind: {wind_arrow} {windspeed} mph ({direction_text})\n"
        output += f"🌨️ Precipitation: {precip} mm\n"
        output += f"📈 Pressure: {pressure} hPa\n"

        return output

# Example usage
if __name__ == "__main__":
    location = "worcester,gb"  # Try "worcester,US", "paris,FR", etc.
    weather_fetcher = WxFetcher(location)
    print(weather_fetcher.get_weather())
