# game/api_client.py
import requests
import json
import os
import sys
# from config import API_LOGIN, API_PASSWORD, API_BASE_URL
# import config
import game.my_python_api.config as config

class APIClient:
    def __init__(self):
        self.base_url = config.url_main
        self.token = None

    def authenticate(self):
        """Аутентификация на сервере и получение JWT токена."""
        print("Аутентификация на сервере и получение JWT токена.")
        auth_url = f"{self.base_url}/login"
        print(auth_url)
        auth_data = {
            "username": config.login,
            "password": config.psw
        }
        response = requests.post(auth_url, data=auth_data)
        # response = requests.post(auth_url, json=auth_data)

        if response.status_code == 200:
            self.token = response.json().get("access_token")
            print(f"Токен получен: {self.token}")
            return True
        else:
            print(f"Authentication failed: {response.status_code}")
            return False

    def get(self, endpoint, params=None):
        """Выполнение GET запроса к API."""
        if not self.token:
            if not self.authenticate():
                return None

        headers = {
            "Authorization": f"Bearer {self.token}",
            'Content-Type': 'application/json',
        }
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            print(response)
            print(response.json())
            return response.json()
        else:
            print(f"GET request failed: {response.status_code}")
            return None

    def post(self, endpoint, data=None):
        """Выполнение POST запроса к API."""
        if not self.token:
            if not self.authenticate():
                return None

        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        url = f"{self.base_url}/{endpoint}"
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"POST request failed: {response.status_code}")
            return None

# Создаем экземпляр APIClient для использования в других частях игры
api_client = APIClient()

