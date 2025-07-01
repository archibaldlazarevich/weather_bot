# WeatherTestBot

## Описание

**WeatherTestBot** — это телеграм бот, который предосталяет данные о погоде по вашей геолокации в настоящее время и на ближайшие 5 дней.

---

## Установка

1. **Клонируйте репозиторий:**

    git clone https://github.com/archibaldlazarevich/weather_bot


2. **Установите зависимости:**

    pip install -r requirements.txt

3. **Настройте переменные окружения:**
  Создайте файл `.env` используя .env.template и добавьте токен бота и конфигурацию базы данных:
  ```
  BOT_TOKEN = ...

  DATABASE_URL = ...(пример - "sqlite+aiosqlite:///base.db")


4. **Запустите :**
    
    python -m src.main
    
5. **Запуск через Docker**
    Для удобства можно использовать Docker. 
    Запуск:
    docker compose up --build
    Остановка:
    docker compose down


---

## Использование

### WeatherTestBot

- `/start` — Запустить бота
- `/help` — Справка
- `/now` — Данные о погоде в настоящее время по вашей геолокации
- `/5_days` — Прогноз погоды на 5 дней по вашей геолокации
---

## Архитектура

- Данные для работы бота при взамодейстии с API OpenWeather.
- Для работы с данными используется SQlite(указать вашу БД: PostgreSQL, SQLite и т.д.).
- Взаимодействие с Telegram реализовано через библиотеку [aiogram](https://docs.aiogram.dev/).

---

## Требования

- Python 3.10+
- aiogram 3.x
- (другие зависимости — см. requirements.txt)

---

## Авторы

- Артур Лазаревич [archibaldlazarevich](https://github.com/archibaldlazarevich)

- почта [compact_00@mail.ru](mailto:compact_00@mail.ru)
---

