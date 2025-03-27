import defusedxml.ElementTree as ET   #made by chatgpt blame the bot for errors
from urllib.request import urlopen

class WeatherWarningsScraper:
    def __init__(self, region=""):# CHANGE THIS FOR DIFFRENT REAGONS CURRENTLY WEST MIDS
        # Change the RSS feed URL to the weather warning URL
        self.rss_url = f"https://www.metoffice.gov.uk/public/data/PWSCache/WarningsRSS/Region/{region}"

    def get_weather_warnings(self):
        try:
            # Open the RSS feed URL and read its content
            with urlopen(self.rss_url) as Client:
                xml_page = Client.read()

                # Parse the XML feed content
                root = ET.fromstring(xml_page)

                # Create a list to store the titles of the weather warnings
                weather_warning_titles = []

                # Iterate through all <item> elements and extract titles
                for item in root.iter("item"):
                    title = item.find("title").text
                    if title:
                        weather_warning_titles.append(title)

                # Format the output to match the required format
                formatted_output = ""
                for title in weather_warning_titles:
                    formatted_output += f"{title}\n"

                return formatted_output

        except Exception as e:
            print("An error occurred:", e)
            return ""

# Example usage:
scraper = WeatherWarningsScraper(region="uk")  # You can change the region if needed
weather_warnings = scraper.get_weather_warnings()

if weather_warnings:
    print("Weather Warning Titles:")
    print(weather_warnings)
else:
    print("No weather warnings found.")
