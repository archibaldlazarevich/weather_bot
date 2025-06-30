import asyncio
import datetime

from src.config.config import API_KEY

import aiohttp

now_url = "https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&lang=ru&appid={API_KEY}&units=metric"
five_day_url = "https://api.openweathermap.org/data/2.5/forecast?lat={latitude}&lon={longitude}&lang=ru&appid={API_KEY}&units=metric"


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
        return
    data = {
        "time": datetime.datetime.now().strftime("%d.%m.%Y, %H:%M"),
        "description": result["weather"][0]["main"],
        "temp": result["main"]["temp"],
        "city": result["name"],
    }
    return data


async def get_weather_five_day(coord: tuple[float, float]) -> dict | None:
    result = await aiohttp_session(
        url=five_day_url.format(
            latitude=coord[0], longitude=coord[1], API_KEY=API_KEY
        )
    )
    if isinstance(result, int):
        return
    data = dict()
    for i in result.get("list"):
        data["city"] = result["city"]["name"]
        if datetime.datetime.fromtimestamp(i["dt"]).hour == 12:
            data[i["dt_txt"]] = {
                "templ": i["main"]["temp"],
                "description": i["weather"][0]["main"],
            }
    return data


asyncio.run(get_weather_for_now((50, 50)))
asyncio.run(get_weather_five_day((53, 50)))
