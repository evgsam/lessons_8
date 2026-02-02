#Модуль авторизации
import requests

def auth(auth_data: dict, session: requests.Session) -> requests.Response:
    base_url = auth_data['url']
    id = auth_data['id']
    username = auth_data['username']
    password = auth_data['password']
   
    print(f"попытка авторизации на {base_url}")
    response = session.get(f"{base_url}{id}/login?uid={username}&pw={password}")
    return response