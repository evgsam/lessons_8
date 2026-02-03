import socketserver
import socket
import threading
import urllib.parse
from typing import Optional
from urllib.parse import urlparse


class ProxyHTTPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # Читаем запрос от клиента (requests.Session)
        data = b""
        while True:
            chunk = self.request.recv(4096)
            if not chunk:
                break
            data += chunk
            if b"\r\n\r\n" in data:
                break
        
        if not data:
            return
            
        request_str = data.decode('utf-8', errors='ignore')
        lines = request_str.split('\n')
        first_line = lines[0]
        
        print(f"[PROXY] Получен запрос: {first_line.strip()}")
        
        # Парсим первую строку: GET http://target/ HTTP/1.1
        try:
            method, url, version = first_line.split()
            parsed_url = urlparse(url)
            target_host = parsed_url.hostname
            target_port = parsed_url.port or 80
            target_path = parsed_url.path or "/"
            if parsed_url.query:
                target_path += "?" + parsed_url.query
                
            # Формируем запрос к target
            target_request = f"{method} {target_path} {version}\n"
            target_request += "Host: " + target_host + "\n"
            target_request += request_str.split('\n', 2)[2]  # Остальные заголовки
            
            print(f"[PROXY] Пересылаем на {target_host}:{target_port}")
            
            # Отправляем на target
            target_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            target_sock.connect((target_host, target_port))
            target_sock.send(target_request.encode())
            
            # Получаем ответ и пересылаем назад
            while True:
                response_chunk = target_sock.recv(4096)
                if not response_chunk:
                    break
                self.request.sendall(response_chunk)
            
            target_sock.close()
            
        except Exception as e:
            print(f"[PROXY] Ошибка: {e}")


class ProxyServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server = socketserver.TCPServer((host, port), ProxyHTTPRequestHandler)
        self.server_thread = None
        self.running = False
