#Тут реализую калсс, в котором будут хранится данные
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
import psutil
import socket

def select_interface():
    """Выводит все сетевые интерфейсы и предлагает выбрать один."""
    stats = psutil.net_if_stats()
    addrs = psutil.net_if_addrs()
    
    interfaces = []
    for iface, stat in stats.items():
        status = "UP" if stat.isup else "DOWN"
        info = f"{iface}: {status}, MTU={stat.mtu}"
        
        if iface in addrs:
            ipv4 = next((a.address for a in addrs[iface] if a.family.name == 'AF_INET'), 'no IP')
            info += f", IP={ipv4}"
        
        interfaces.append((iface, info))
    
    print("Выберите сетевой интерфейс для снифинга:")
    for i, (name, info) in enumerate(interfaces, 1):
        print(f"{i}. {info}")
    
    while True:
        try:
            choice = int(input(f"Выберите номер (1-{len(interfaces)}): ")) - 1
            if 0 <= choice < len(interfaces):
                selected = interfaces[choice][0]
                print(f"Выбран: {selected}")
                return selected
            print("Неверный номер!")
        except ValueError:
            print("Введите число!")


class AppConfig:
    def __init__(self):
        load_dotenv()
        self._url = f"http://google-gruyere.appspot.com/" 
        self._host_ip = socket.gethostbyname(urlparse(self._url).netloc)
        self._id = os.getenv("MY_ID")
        self._iface = select_interface()
        self._username = os.getenv("USERNAME")
        self._password = os.getenv("PSWRD")
        self._proxy_ip = "127.0.0.1"
        self._proxy_port = "8080"
    
    def url(self) -> str:
        """Возвращает URL"""
        if not self._url:
            raise ValueError("URL не найден")
        return self._url
    
    def host_ip(self) -> str:
        """Возвращает IP хоста"""
        if not self._host_ip:
            raise ValueError("URL не найден")
        return self._host_ip
    
    def iface(self) -> str:
        """Возвращает Интерфейс для прослушки"""
        if not self._iface:
            raise ValueError("Интерфейс не найден")
        return self._iface
    
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
    
    def proxy_ip(self) -> str:
        """Возвращает IP прокси"""
        if not self._proxy_ip:
            raise ValueError("IP для прокси не найден")
        return self._proxy_ip
    
    def proxy_port(self) -> str:
        """Возвращает порт для прокси"""
        if not self._proxy_port:
            raise ValueError("Порт для прокси не найден")
        return self._proxy_port


    def get_conf_credentials(self) -> dict:
        """Возвращает учетные данные в виде словаря"""
        return {
            "url": self.url(),
            "host_ip": self.host_ip(),
            "iface": self.iface(),
            "id": self.id(),
            "username": self.username(),
            "password": self.password(),
            "proxy_ip": self.proxy_ip(),
            "proxy_port": self.proxy_port(),
        }
    
    def is_valid(self) -> bool:
        """Проверяет, есть ли все необходимые данные"""
        return bool(self._username and self._url and self._id and self._password ) 




