import json
from urllib.request import urlopen

class PollenLevels():
    def __init__(self, locations):
        self.pollen_api = "https://air-quality-api.open-meteo.com/v1/air-quality?latitude={0}&longitude={1}&current=alder_pollen,birch_pollen,grass_pollen,mugwort_pollen,olive_pollen,ragweed_pollen"
        self.locations = locations

    def get_pollen_levels(self):
        response = []
        for lonlat in self.locations:
            try:
                lonlatResponse = []
                lonlatSplit = lonlat.split(",")
                with urlopen(self.pollen_api.format(lonlatSplit[0],lonlatSplit[1])) as Client:
                    data = json.load(Client)
                    if "current" in data:
                        for key in data["current"].keys():
                            if key.endswith("_pollen"):
                                lonlatResponse.append("{0} @ {1} {2}\n".format(key.replace("_", " ").capitalize(),str(data["current"][key]), data["current_units"][key]))
                        response.append("".join(lonlatResponse))
                    else:
                        print("Error pulling from API - could be invalid lon lat in config yaml or API limit exceeded..")
            except Exception as e:
                print("An error occurred:", e)
        return response