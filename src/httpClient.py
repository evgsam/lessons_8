import requests

class HttpClient:
   def __init__(self, auth_data: dict, session: requests.Session):
        self._base_url = auth_data['url']
        self._id = auth_data['id']
        self._username = auth_data['username']    
        self._password = auth_data['password']
        self.session = session
       
   def handle_status(self, code):
    if code == 200:
        print("Успешно!")
        return
    #ошибки
    errors = {
        404: "Ресурс не найден. Проверьте URL.",
        429: "Слишком много запросов. Подождите.",
        403: "Доступ запрещен.",
        401: "Требуется авторизация.",
    }
    
    if code in errors:
        raise Exception(f"{code}: {errors[code]}")
    elif code >= 500:
        raise Exception(f"{code}: Ошибка сервера.")
    else:
        raise Exception(f"{code}: Ошибка запроса.")
    
   def get_url(self) -> str:
        return self._base_url
   def get_id(self) -> str:
        return self._id
   def get_username(self) -> str:
        return self._username
   def get_password(self) -> str:
        return self._password

   def get_data(self, data:str) -> requests.Response:
        base_url = self.get_url()
        id = self.get_id()
        session = self.session
        response = session.get(f"{base_url}{id}{data}")
        #print(response.status_code)
        self.handle_status(response.status_code)
        return response

