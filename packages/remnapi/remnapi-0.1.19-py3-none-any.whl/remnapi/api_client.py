import os
import requests
from dotenv import load_dotenv
import asyncio
import aiohttp

load_dotenv()  # Загружаем переменные окружения из .env


class APIClient:
    BASE_URL = os.getenv("PANEL_URL")  # Базовый URL API

    def __init__(self):
        print(f"✅ PANEL_URL: {self.BASE_URL}")  # Вывод значения для проверки
        self.token = os.getenv("API_TOKEN")  # Читаем токен из .env
        self.jwt_token = os.getenv("JWT_API_TOKENS_SECRET")  # Читаем токен из .env
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}" if self.token else None
        }

    async def request(self, method, endpoint, use_jwt=False, **kwargs):
        """Базовый метод для всех запросов."""
        url = f"{self.BASE_URL}{endpoint}"
        
        # Выбираем токен: если `use_jwt=True`, используем `JWT_API_TOKENS_SECRET`
        token = self.jwt_token if use_jwt else self.token

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}" if token else None
        }

        async with aiohttp.ClientSession() as session:
            async with session.request(method, url, headers=headers, **kwargs) as response:
                if response.status == 401:
                    raise Exception("Unauthorized: Проверьте токен API")
                elif response.status >= 400:
                    raise Exception(f"Ошибка {response.status}: {await response.text()}")
                return await response.json()
