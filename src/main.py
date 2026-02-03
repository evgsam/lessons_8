import requests
from config import AppConfig
from auth import authorization
from payloads import get_payloads
from http_client import HttpClient
from exploit_test import exploit_test

from proxy_server import ProxyServer
import threading

def main():
    credentials = AppConfig().get_conf_credentials()
    proxy_ip = credentials["proxy_ip"]
    proxy_port = int(credentials["proxy_port"])
   
    proxy = ProxyServer(proxy_ip,proxy_port)
    target_host = credentials["host_ip"]
    try:
        proxy.start()
        threading.Event().wait(2)
        session = requests.Session()
        session.proxies = {"http": f"http://{proxy_ip}:{proxy_port}"}
        
        client = HttpClient(credentials, session)
        response = authorization(client)
        payloads = get_payloads()
        exploit_test(client, payloads)
    finally:
        proxy.stop()

if __name__ == "__main__":
    main()

    

