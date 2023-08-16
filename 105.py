import httpx
from prefect import task, flow, get_run_logger
from prefect.tasks import task_input_hash
from datetime import timedelta


'''
Get weather info from open meteo using flows and tasks.
Note: persist_result will mess with cache parameter if both are set (in different tasks/ flows)
@task(retries=2, retry_delay_seconds=0.1, persist_result=True)
'''


@task(retries=2, retry_delay_seconds=0.1)
def fetch_weather(lat: float, lon: float):
    base_url = "https://api.open-meteo.com/v1/forecast/"
    weather = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly="temperature_2m"),
    )
    most_recent_temp = float(weather.json()["hourly"]["temperature_2m"][0])
    print(f"Most recent temp C: {most_recent_temp} degrees")
    return most_recent_temp

@task(retries=2, retry_delay_seconds=0.1, cache_key_fn=task_input_hash, cache_expiration=timedelta(minutes=2))
def fetch_dewpoint(lat: float, lon: float):
    base_url = "https://api.open-meteo.com/v1/forecast/"
    weather = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly="dewpoint_2m"),
    )
    most_recent_dewpoint = float(weather.json()["hourly"]["dewpoint_2m"][0])
    print(f"Most recent dewpoint C: {most_recent_dewpoint} degrees")
    return most_recent_dewpoint

@flow()
def save_weather(weather_report):
    with open('report.txt', '+w') as w:
        w.write(str(weather_report))
    w.close()

@flow
def weather_pipeline(lat: float, lon: float):
    logger = get_run_logger()
    weather = fetch_weather(lat, lon)
    dewpoint = fetch_dewpoint(lat, lon)

    weather_report = {
        "weather": weather,
        "dewpoint": dewpoint
    }
    
    save_weather(weather_report)


if __name__ == "__main__":
    weather_pipeline(38.9, -77.0)