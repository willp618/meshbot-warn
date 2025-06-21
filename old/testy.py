elif "#wxwarn" in message:
    transmission_count += 1

    # Fetch weather warnings from the scraper
    weather_warnings = wxwarn_scraper.get_weather_warnings()
    time.sleep(15)

    # Debug print — check what get_weather_warnings() is returning
    print("[DEBUG] weather_warnings:", weather_warnings)
    print("[DEBUG] Type:", type(weather_warnings))

    # Send weather warnings if they exist
    if isinstance(weather_warnings, list) and weather_warnings:
        for i, chunk in enumerate(weather_warnings, start=1):
            part_message = f"Part {i}/{len(weather_warnings)}: {chunk}"
            interface.sendText(part_message, wantAck=True, destinationId=sender_id)
            time.sleep(5)
    else:
        interface.sendText("No current weather warnings available.", wantAck=True, destinationId=sender_id)
