import datetime

import aiohttp

from src.config.config import API_KEY

now_url = (
    "https://api.openweathermap.org/data/2.5/weather?lat="
    "{latitude}&lon={longitude}&appid={API_KEY}&lang=ru&units=metric"
)
five_day_url = (
    "https://api.openweathermap.org/data/2.5/forecast?lat="
    "{latitude}&lon={longitude}&lang=ru&appid="
    "{API_KEY}&lang=ru&units=metric"
)


async def aiohttp_session(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.request("GET", url=url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            return response.status


async def get_weather_for_now(coord: tuple[float, float]) -> dict | None:
    result = await aiohttp_session(
        url=now_url.format(
            latitude=coord[0], longitude=coord[1], API_KEY=API_KEY
        )
    )
    if isinstance(result, int):
        return None
    data = {
        "time": datetime.datetime.now().strftime("%d.%m.%Y \nвремя - %H:%M"),
        "description": result["weather"][0]["description"].capitalize(),
        "temp": result["main"]["temp"],
    }
    return data


async def get_weather_five_day(coord: tuple[float, float]) -> dict | None:
    result = await aiohttp_session(
        url=five_day_url.format(
            latitude=coord[0], longitude=coord[1], API_KEY=API_KEY
        )
    )
    if isinstance(result, int):
        return None
    data = dict()
    for i in result.get("list"):
        if datetime.datetime.fromtimestamp(i["dt"],tz=datetime.timezone.utc).hour == 12:
            data[datetime.datetime.fromtimestamp(i["dt"])] = {
                "templ": i["main"]["temp"],
                "description": i["weather"][0]["description"].capitalize(),
            }
    return data
