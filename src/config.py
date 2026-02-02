#Тут реализую калсс, в котором будут хранится данные
import os
from dotenv import load_dotenv

this_base_url = f"https://google-gruyere.appspot.com/" 

class AppConfig:
    def __init__(self):
        load_dotenv()
        self._url = f"https://google-gruyere.appspot.com/" 
        self._id = os.getenv("MY_ID")
        self._username = os.getenv("USERNAME")
        self._password = os.getenv("PSWRD")
    
    def url(self) -> str:
        """Возвращает URL"""
        if not self._url:
            raise ValueError("URL не найден")
        return self._url
    
    def id(self) -> str:
        """Возвращает ID"""
        if not self._id:
            raise ValueError("ID не найден в .env файле")
        return self._id
    
    def username(self) -> str:
        """Возвращает имя пользователя"""
        if not self._username:
            raise ValueError("Имя пользователя не найдено в .env файле")
        return self._username
    
    def password(self) -> str:
        """Возвращает пароль"""
        if not self._password:
            raise ValueError("Пароль не найден в .env файле")
        return self._password
    


    def get_conf_credentials(self) -> dict:
        """Возвращает учетные данные в виде словаря"""
        return {
            "url": self.url(),
            "id": self.id(),
            "username": self.username(),
            "password": self.password(),
        }
    
    def is_valid(self) -> bool:
        """Проверяет, есть ли все необходимые данные"""
        return bool(self._username and self._url and self._id and self._password ) 




