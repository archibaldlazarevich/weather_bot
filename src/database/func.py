from sqlalchemy import insert, select, update

from src.database.create_db import get_db_session
from src.database.models import User


async def check_user_id(user_id: int):
    """
    Метод для проверки наличия пользователя в бд
    :param user_id:
    :return:
    """
    async with get_db_session() as session:
        result_data = await session.execute(
            select(User).where(User.tel_id == user_id)
        )
    result = result_data.scalar_one_or_none()
    return result if result else None


async def add_new_user(user_id: int):
    """
    Функция доавляяет нового пользователя в бд
    :param user_id:
    :return:
    """
    async with get_db_session() as session:
        await session.execute(insert(User).values(tel_id=user_id))
        await session.commit()


async def check_position(user_id: int) -> None | tuple[float, float]:
    """
    Метод для проверки наличия последней геопозиции пользователя, если геопозиции нет,
    то возвращает id пользоваетеля, если нет пользователя, то добавляет его id в бд, и возвращает id
    :param user_id: id пользователя из телеграмма
    :return: bool | tuple[float, float]
    """

    check_user = await check_user_id(user_id=user_id)
    if check_user:
        return (
            (check_user.latitude, check_user.longitude)
            if check_user.latitude
            else None
        )
    await add_new_user(user_id=user_id)
    return None


async def add_coord(coord_with_user_id: tuple) -> None:
    """
    Добавление координат последней геопозиции пользователя
    :param coord_with_user_id: координаты пользователя (latitude, longitude, city_id, user_id)
    :return:
    """
    async with get_db_session() as session:
        await session.execute(
            update(User)
            .where(User.tel_id == coord_with_user_id[2])
            .values(
                latitude=coord_with_user_id[0],
                longitude=coord_with_user_id[1],
            )
        )
        await session.commit()


async def get_users_coord(
    user_id: int,
) -> tuple | None:
    """
    Получение координат по id пользователя
    :param user_id:
    :return: tuple | None
    """
    async with get_db_session() as session:
        result_data = await session.execute(
            select(User.latitude, User.longitude).where(User.tel_id == user_id)
        )
    result = result_data.all()[0]
    return result if result[0] else None
