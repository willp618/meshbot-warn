import requests

class WxFetcher:
    def __init__(self, location):
        self.location = location

    def get_weather(self):
        # Requesting JSON data from wttr.in using the correct format `?format=j1`
        url = f"https://wttr.in/{self.location}?format=j1"
        response = requests.get(url)

        # Check if the response is valid and contains JSON data
        if response.status_code == 200:
            try:
                weather_data = response.json()  # Parse the JSON response
            except ValueError as e:
                return f"Error: Unable to parse JSON data. {e}"

            # Extract the necessary data from the JSON
            location = weather_data.get('nearest_area', [{}])[0].get('areaName', [{}])[0].get('value', 'Unknown location')
            condition = weather_data.get('current_condition', [{}])[0].get('weatherDesc', [{}])[0].get('value', 'Unknown')
            temperature = weather_data.get('current_condition', [{}])[0].get('temp_C', 'N/A')
            feels = weather_data.get('current_condition', [{}])[0].get('FeelsLikeC', 'N/A')
            humidity = weather_data.get('current_condition', [{}])[0].get('humidity', 'N/A')
            wind_speed = weather_data.get('current_condition', [{}])[0].get('windspeedMiles', 'N/A')
            wind_dir = weather_data.get('current_condition', [{}])[0].get('winddir16Point', 'N/A')  # Wind direction
            pressure = weather_data.get('current_condition', [{}])[0].get('pressure', 'N/A')
            precipitation = weather_data.get('current_condition', [{}])[0].get('precipMM', 'N/A')
            dawn = weather_data.get('weather', [{}])[0].get('astronomy', [{}])[0].get('sunrise', 'N/A')
            sunset = weather_data.get('weather', [{}])[0].get('astronomy', [{}])[0].get('sunset', 'N/A')

            # Map the 16-point wind directions to arrow emojis
            wind_direction_map = {
                "N": "↑", "NNE": "↗", "NE": "→", "ENE": "↗",
                "E": "→", "ESE": "↘", "SE": "↓", "SSE": "↘",
                "S": "↓", "SSW": "↙", "SW": "←", "WSW": "↖",
                "W": "←", "WNW": "↖", "NW": "↑", "NNW": "↖"
            }

            # Default wind direction to an arrow if not found
            wind_dir_arrow = wind_direction_map.get(wind_dir, "↗")  # Default to "↗" if unknown

            # Format wind information: "Wind speed ↗26 Mph"
            if wind_dir != 'N/A' and wind_speed != 'N/A':
                wind = f"Wind speed {wind_dir_arrow} {wind_speed} Mph"
            else:
                wind = "Wind data unavailable"

            # Emoji mapping for weather conditions
            emojis = {
                "☁️": ["Cloudy", "Overcast", "cloudy"],
                "🌤️": ["Partly cloudy", "Partly sunny"],
                "🌞": ["Sunny", "Clear", "Clear sky"],
                "🌧️": ["Rain", "Rainy", "Drizzle", "Light rain", "Heavy drizzle"],
                "🌩️": ["Thunderstorm"],
                "❄": ["Snow", "Light snow"],
                "🌨️": ["Snow shower", "Shower snow"],
                "🌬️": ["Windy"],
                "🌫️": ["Fog", "Mist"],
            }

            # Default emoji if no match is found
            selected_emoji = "🌥️"  # Cloudy by default

            # Find the emoji that matches the condition
            for emoji, conditions in emojis.items():
                if any(cond.lower() in condition.lower() for cond in conditions):
                    selected_emoji = emoji
                    break

            # Prepare the output string
            output = f"{location}\n"
            output += f"{selected_emoji} {condition}\n"
            output += f"Temp {temperature}°C\n"
            output += f"Feels like {feels}°C\n"
            output += f"Humidity {humidity}%\n"
            output += f"{wind}\n"  # Display formatted wind information
            output += f"Precip 🌨️ {precipitation} mm\n"
            output += f"Pressure {pressure} hPa\n"
            output += f"Dawn {dawn}\n"
            output += f"Sunset {sunset}\n"

            return output
        else:
            return f"Failed to fetch weather data. HTTP Status Code: {response.status_code}"

# Example usage uncomment to run by itself for testing
location = "kidderminster"  # Replace with your location of choice
weather_fetcher = WxFetcher(location)
weather_report = weather_fetcher.get_weather()
print(weather_report)

