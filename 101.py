import httpx
from prefect import task, flow

'''
Get weather info from open meteo using flows and tasks.
'''

@task
def fetch_weather(lat: float, lon: float):
    base_url = "https://api.open-meteo.com/v1/forecast/"
    weather = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly="temperature_2m"),
    )
    most_recent_temp = float(weather.json()["hourly"]["temperature_2m"][0])
    print(f"Most recent temp C: {most_recent_temp} degrees")
    return most_recent_temp

@task
def fetch_dewpoint(lat: float, lon: float):
    base_url = "https://api.open-meteo.com/v1/forecast/"
    weather = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly="dewpoint_2m"),
    )
    most_recent_dewpoint = float(weather.json()["hourly"]["dewpoint_2m"][0])
    print(f"Most recent dewpoint C: {most_recent_dewpoint} degrees")
    return most_recent_dewpoint
@task
def fetch_windspeed(lat: float, lon: float):
    base_url = "https://api.open-meteo.com/v1/forecast/"
    weather = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly="windspeed_10m"),
    )
    most_recent_windspeed = float(weather.json()["hourly"]["windspeed_10m"][0])
    print(f"Most recent windspeed C: {most_recent_windspeed} degrees")
    return most_recent_windspeed

@flow
def weather_pipeline(lat: float, lon: float):
    fetch_weather(lat, lon)

    fetch_dewpoint(lat, lon)
    
    fetch_windspeed(lat, lon)


if __name__ == "__main__":
    weather_pipeline(38.9, -77.0)