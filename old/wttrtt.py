# import requests

# class Wx2Fetcher:
#     def __init__(self, location):
#         self.location = location

#     def get_weather(self):
#         url = f"https://wttr.in/{self.location}?format=%l+%C+%t+%f+%h+%w+%P+%p+%u+%S+%s"
#         response = requests.get(url)
        
#         if response.status_code == 200:
#             response_text = response.text.strip()  # Fetch the raw weather data
            
#             # Split the response text into parts
#             wx2_info = response_text.split()
            
#             # Ensure we have enough data
#             if len(wx2_info) < 10:
#                 return "Error: Invalid weather data received."

#             location = wx2_info[0].strip()
#             condition = " ".join(wx2_info[1:3]).strip()  # Join multi-word conditions like "Heavy drizzle"
#             temperature = wx2_info[3].strip()
#             feels = wx2_info[4].strip()
#             humidity = wx2_info[5].strip()
#             wind = wx2_info[6].strip()
#             pressure = wx2_info[7].strip()
#             precipitation = wx2_info[8].strip()
            
#             dawn = wx2_info[-2].strip()
#             sunset = wx2_info[-1].strip()

#             # Emoji mapping for weather conditions
#             emojis = {
#                 "☁️": ["Cloudy", "Overcast", "cloudy"],
#                 "🌤️": ["Partly cloudy", "Partly sunny"],
#                 "🌞": ["Sunny", "Clear", "Clear sky"],
#                 "🌧️": ["Rain", "Rainy", "Drizzle", "Light rain", "Heavy drizzle"],
#                 "🌩️": ["Thunderstorm"],
#                 "❄": ["Snow", "Light snow"],
#                 "🌨️": ["Snow shower", "Shower snow"],
#                 "🌬️": ["Windy"],
#                 "🌫️": ["Fog", "Mist"],
#             }

#             # Default emoji if no match is found
#             selected_emoji = "🌥️"  # Cloudy by default

#             # Find the emoji that matches the condition
#             for emoji, conditions in emojis.items():
#                 if any(cond.lower() in condition.lower() for cond in conditions):
#                     selected_emoji = emoji
#                     break

#             # Prepare the output string
#             output = f"{location}\n"
#             output += f"{selected_emoji} {condition}\n"
#             output += f"Temperature 🌡️ {temperature}\n"
#             output += f"Feels like 🌡️ {feels}\n"
#             output += f"Humidity 💧 {humidity}\n"
#             output += f"Wind speed 💨 {wind}\n"
#             output += f"Precipitation 🌨️ {precipitation}\n"
#             output += f"Pressure ⏲️ {pressure}\n"
#             output += f"Dawn 🌞 {dawn}\n"
#             output += f"Sunset 🌛 {sunset}\n"

#             return output
#         else:
#             return "Failed to fetch weather data."


# # Example usage uncomment to run by its self for testing
# location = "kidderminster"
# weather_fetcher = Wx2Fetcher(location)
# weather_report = weather_fetcher.get_weather()
# print(weather_report)

