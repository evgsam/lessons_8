#Тут реализую калсс, в котором будут хранится данные
import os
from dotenv import load_dotenv

this_base_url = f"https://google-gruyere.appspot.com/" 

class AppConfig:
    def __init__(self, env_file: str = ".env"):
        load_dotenv(env_file)
        self._username = os.getenv("USERNAME")
        self._password = os.getenv("PSWRD")
        self._id = os.getenv("MY_ID")

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
    
    def id(self) -> str:
        """Возвращает ID"""
        if not self._id:
            raise ValueError("ID не найден в .env файле")
        return self._id

    def get_conf_credentials(self) -> dict:
        """Возвращает учетные данные в виде словаря"""
        return {
            "username": self.username,
            "password": self.password,
            "id": self.id
        }
    
    def is_valid(self) -> bool:
        """Проверяет, есть ли все необходимые данные"""
        return bool(self._username and self._password and self._id)




