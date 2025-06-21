import requests

class WeatherAlertsScraper:
    def __init__(self, state):
        self.state = state
        # Use the weather.gov API endpoint for active alerts in a specific state
        self.api_url = f"https://api.weather.gov/alerts/active?area={self.state}"

    def get_alert_details(self, alert):
        """Extract and format alert details including severity, certainty, urgency, event, senderName, and headline."""
        alert_details = {
            "severity": alert.get("severity", "N/A"),
            "certainty": alert.get("certainty", "N/A"),
            "urgency": alert.get("urgency", "N/A"),
            "event": alert.get("event", "N/A"),
            "senderName": alert.get("senderName", "N/A"),
            "headline": alert.get("headline", "N/A")
        }
        return alert_details

    def get_weather_alerts(self):
        try:
            # Request active weather alerts for the specified state
            response = requests.get(self.api_url)
            
            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()

                # If the API returns alerts, process them
                if "features" in data:
                    alerts = data["features"]
                    weather_alerts = []

                    # Iterate through all the alerts
                    for alert in alerts:
                        alert_properties = alert["properties"]
                        alert_details = self.get_alert_details(alert_properties)
                        weather_alerts.append(alert_details)

                    # Format the output with relevant alert information
                    formatted_output = ""
                    for alert in weather_alerts:
                        formatted_output += (
                            f"Event: {alert['event']}\n"
                            f"Severity: {alert['severity']}\n"
                            f"Certainty: {alert['certainty']}\n"
                            f"Urgency: {alert['urgency']}\n"
                            f"Sender: {alert['senderName']}\n"
                            f"Headline: {alert['headline']}\n\n"
                        )

                    return formatted_output
                else:
                    return "No active weather alerts found for the specified state."
            else:
                return f"Error: Unable to fetch data. HTTP Status Code: {response.status_code}"

        except Exception as e:
            print("An error occurred:", e)
            return ""

# Example usage:
if __name__ == "__main__":
    state = "OK"  # Example: California, change to the state you want to query
    scraper = WeatherAlertsScraper(state)
    weather_alerts = scraper.get_weather_alerts()

    if weather_alerts:
        print("Active Weather Alerts:")
        print(weather_alerts)
    else:
        print("No weather alerts found.")
