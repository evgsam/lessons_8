#Модуль авторизации
import requests

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    # Этот код выполняется только для проверки типов
    # Не создает циклических импортов в runtime
    from http_client import HttpClient

def authorization(client: 'HttpClient') -> requests.Response:
    print(f"попытка авторизации на {client.get_url()}")
    return client.get_data(f"/login?uid={client.get_username()}&pw={client.get_password()}")