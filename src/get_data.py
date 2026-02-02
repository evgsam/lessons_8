#Модуль авторизации
import requests

def get_data(auth_data: dict, session: requests.Session, data:str) -> requests.Response:
    base_url = auth_data['url']
    id = auth_data['id']
    username = auth_data['username']
    password = auth_data['password']
   
    print(f"отправка на {base_url}")
    response = session.get(f"{base_url}{id}{data}")
    return response