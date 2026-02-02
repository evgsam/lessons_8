import requests
from config import AppConfig
from auth import authorization
from get_data import get_data_
from payloads import get_payloads
from http_client import HttpClient

def handle_status(code):
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


def main():
    session = requests.Session()
    credentials = AppConfig().get_conf_credentials()
    client = HttpClient(credentials,session)
    response = authorization(client)
    payloads = get_payloads()
    response = get_data_(client,f"/newsnippet2?snippet={payloads[1]}")


if __name__ == "__main__":
    main()

    

