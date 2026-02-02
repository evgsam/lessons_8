import requests
from config import AppConfig
from auth import authorization
from payloads import get_payloads
from http_client import HttpClient
from exploit_test import exploit_test


def main():
    session = requests.Session()
    credentials = AppConfig().get_conf_credentials()
    client = HttpClient(credentials,session)
    response = authorization(client)
    payloads = get_payloads()
    exploit_test(client,payloads)

if __name__ == "__main__":
    main()

    

