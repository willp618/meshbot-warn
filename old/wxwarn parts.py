import defusedxml.ElementTree as ET
from urllib.request import urlopen

class WeatherWarningsScraper:
    def __init__(self, region):
        self.region = region
        self.rss_url = f"https://www.metoffice.gov.uk/public/data/PWSCache/WarningsRSS/Region/{self.region}"

    def abbreviate_description(self, text, max_length=180):
        replacements = {
            "weather warning": "WX warn",
            "heavy rainfall": "hvyrain",
            "possible disruption": "disruption",
            "localised flooding": "flooding",
            "take care when travelling": "drive safe",
            "public transport": "transit",
            "homes and businesses": "properties",
            "Yellow warning": "Y-Warn",
            "Amber warning": "Amb-Warn",
            "Red warning": "Red-Warn",
            "West Midlands": "W Mids",
            "Herefordshire": "Heref",
            "Shropshire": "Salop",
            "Worcestershire": "Worcs"
        }

        for full, abbr in replacements.items():
            text = text.replace(full, abbr)

        return text if len(text) <= max_length else text[:max_length].rstrip() + "..."

    def get_weather_warnings(self):
        try:
            with urlopen(self.rss_url) as Client:
                xml_page = Client.read()
                root = ET.fromstring(xml_page)
                warnings_output = []

                for item in root.iter("item"):
                    description = item.find("description").text.strip() if item.find("description") is not None else "No Description"
                    abbreviated = self.abbreviate_description(description)
                    warnings_output.append(abbreviated)

                return warnings_output  # Return list instead of joined string

        except Exception as e:
            print("An error occurred:", e)
            return []

# Example usage:
region = "wm"
scraper = WeatherWarningsScraper(region)
weather_warnings = scraper.get_weather_warnings()

if weather_warnings:
    print("WXwarns:")
    for msg in weather_warnings:
        print("-", msg)
else:
    print("No weather warnings found.")
