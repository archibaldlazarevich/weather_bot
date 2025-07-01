"""
Модуль для работы по определению населелнных пунктов по координатам
"""

import asyncio
from geopy.geocoders import Nominatim

geolocator = Nominatim(
    user_agent="geo_locator",
    timeout=10,
)


async def define_address(coord: tuple[float, float]) -> str | None:
    """
    Метод для определения города по координатам,
    запроса к бд для получения id города в бд city
    :param coord: координаты (latitude, longitude)
    :return: Название города если True или False,
    город не найден по данным координатам (пример: если это деревня, то None)
    """
    geolocator = Nominatim(user_agent="GetLoc", timeout=10)
    location = await asyncio.to_thread(
        geolocator.reverse, coord, language="ru"
    )
    if not location:
        return '"Местоположение не определено"'
    if "locality" in location.raw["address"]:
        answer = f"около н.п. {location.raw['address']['locality']}, {location.raw['address']['city']}"
    elif "village" in location.raw["address"]:
        answer = f"д. {location.raw['address']['village']}"
    elif "town" in location.raw["address"]:
        answer = f"г. {location.raw['address']['town']}"
    elif "city" in location.raw["address"]:
        answer = f"г. {location.raw['address']['city']}"
    else:
        answer = location
    return answer
