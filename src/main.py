import requests
from config import AppConfig
from auth import auth 
from get_data import get_data

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
    response = auth(credentials, session)
    handle_status(response.status_code)
    response = get_data(credentials,session,"/newsnippet2?snippet=OGAF")
    handle_status(response.status_code)

if __name__ == "__main__":
    main()

    

