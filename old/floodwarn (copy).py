import defusedxml.ElementTree as ET  # made by chatgpt blame the bot for errors
from urllib.request import urlopen
import yaml  # To load the RSS URL from the settings.yaml file

class FloodWarningsScraper:
    def __init__(self):
        # Load RSS URL from settings.yaml file
        with open('settings.yaml', 'r') as file:
            settings = yaml.safe_load(file)
            self.rss_url = settings.get("FLOOD_RSS_FEED_URL", "https://environment.data.gov.uk/flood-widgets/rss/feed-England.xml")
            # Fallback to the default URL if the setting is not found.

    def get_flood_warnings(self):
        try:
            # Open the RSS feed URL and read its content
            with urlopen(self.rss_url) as Client:
                xml_page = Client.read()

                # Parse the XML feed content
                root = ET.fromstring(xml_page)

                # Create a list to store the titles of the flood warnings
                flood_warning_titles = []

                # Iterate through all <item> elements and extract titles
                for item in root.iter("item"):
                    title = item.find("description").text
                    if title:
                        flood_warning_titles.append(title)

                # Format the output to match the required format
                formatted_output = ""
                for title in flood_warning_titles:
                    formatted_output += f"{title}\n"

                return formatted_output

        except Exception as e:
            print("An error occurred:", e)
            return ""

# Example usage:
scraper = FloodWarningsScraper()
flood_warnings = scraper.get_flood_warnings()

if flood_warnings:
    print("Flood Warning Titles:")
    print(flood_warnings)
else:
    print("No flood warnings found.")
