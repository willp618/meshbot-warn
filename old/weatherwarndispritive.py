import defusedxml.ElementTree as ET  # made by chatgpt, blame the bot for errors
from urllib.request import urlopen

class WeatherWarningsScraper:
    def __init__(self, region):
        self.region = region
        self.rss_url = f"https://www.metoffice.gov.uk/public/data/PWSCache/WarningsRSS/Region/{self.region}"

    def get_weather_warnings(self):
        try:
            with urlopen(self.rss_url) as Client:
                xml_page = Client.read()
                root = ET.fromstring(xml_page)
                warnings_output = []

                for item in root.iter("item"):
                    title = item.find("title").text.strip() if item.find("title") is not None else "No Title"
                    description = item.find("description").text.strip() if item.find("description") is not None else "No Description"
                    full_message = f"{title}\n{description}"
                    warnings_output.append(full_message)

                return "\n\n".join(warnings_output)

        except Exception as e:
            print("An error occurred:", e)
            return ""

# Example usage:
region = "wm"  # Replace with the desired region code
scraper = WeatherWarningsScraper(region)
weather_warnings = scraper.get_weather_warnings()

if weather_warnings:
    print("WXwarn:",weather_warnings)
else:
    print("No weather warnings found.")
