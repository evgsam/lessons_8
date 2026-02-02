#Модуль авторизации
import requests

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Этот код выполняется только для проверки типов
    # Не создает циклических импортов в runtime
    from http_client import HttpClient

def get_data(auth_data: dict, session: requests.Session, data:str) -> requests.Response:
    base_url = auth_data['url']
    id = auth_data['id']
    username = auth_data['username']
    password = auth_data['password']
   
    print(f"отправка на {base_url}")
    response = session.get(f"{base_url}{id}{data}")
    return response

def get_data_(client: 'HttpClient', data:str) -> requests.Response:
    print(f"отправка данных на {client.get_url()}")
    return client.get_data(data)