import json
from urllib.request import urlopen

class PollenLevels():
    def __init__(self, locations):
        self.pollen_api = "https://air-quality-api.open-meteo.com/v1/air-quality?latitude={0}&longitude={1}&current=alder_pollen,birch_pollen,grass_pollen,mugwort_pollen,ragweed_pollen,european_aqi"
        self.locations = locations

    def get_pollen_level_description(self, value):
        """Return the pollen level description based on the given value."""
        if value <= 25:
            return "Low"
        elif value <= 50:
            return "Mod"
        elif value <= 150:
            return "High"
        else:
            return "V High"

    def get_aqi_description(self, aqi_value):
        """Return the AQI description based on the European Air Quality Index."""
        if aqi_value <= 50:
            return "Good"
        elif aqi_value <= 100:
            return "Fair"
        elif aqi_value <= 150:
            return "Moderate"
        elif aqi_value <= 200:
            return "Poor"
        else:
            return "Very Poor"

    def get_pollen_levels(self):
        response = []
        for lonlat in self.locations:
            try:
                lonlatResponse = []
                lonlatSplit = lonlat.split(",")
                latitude, longitude = lonlatSplit[0], lonlatSplit[1]
                # Add location at the top of the report
                lonlatResponse.append(f"Location: {latitude}, {longitude}\n")

                with urlopen(self.pollen_api.format(latitude, longitude)) as Client:
                    data = json.load(Client)
                    if "current" in data:
                        # Check for european_aqi and add it to the top of the output
                        if "european_aqi" in data["current"]:
                            aqi_value = data["current"]["european_aqi"]
                            aqi_description = self.get_aqi_description(aqi_value)
                            lonlatResponse.append("European AQI: {0} ({1})\n".format(str(aqi_value), aqi_description))

                        # Add the pollen levels below the European AQI
                        for key in data["current"].keys():
                            if key.endswith("_pollen"):
                                pollen_value = data["current"][key]
                                level_description = self.get_pollen_level_description(pollen_value)
                                # Remove the word 'pollen' from the key and format the output
                                lonlatResponse.append("{0} @ {1} {2} ({3})\n".format(
                                    key.replace("_pollen", "").replace("_", " ").capitalize(),
                                    str(pollen_value),
                                    data["current_units"][key],
                                    level_description
                                ))

                        response.append("".join(lonlatResponse))
                    else:
                        print("Error pulling from API - could be invalid lon lat in config yaml or API limit exceeded..")
            except Exception as e:
                print("An error occurred:", e)
        return response

# Example usage (uncomment to run by itself for testing)

if __name__ == "__main__":
    locations = ["52.002259,-2.1443099"]  # Example locations (latitude,longitude)
    pollen_fetcher = PollenLevels(locations)
    pollen_report = pollen_fetcher.get_pollen_levels()
    for report in pollen_report:
        print(report)
