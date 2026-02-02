import os
from dotenv import load_dotenv
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#не свечу свои данные в коде
load_dotenv()
my_id = os.getenv("MY_ID")
username = os.getenv("USERNAME")
password = os.getenv("PSWRD")
base_url = f"http://google-gruyere.appspot.com/" 

#код для вывода статусов ответа
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

#функция отправки post
def post_req(url, data = None, auth = None, timeout = None):
    response = requests.post(
        url,
        data=data,
        auth=auth,
        timeout=timeout
    )
    handle_status(response.status_code)
    return response 

print(f"Логинимся на сайте {base_url}")
post_req(
    base_url + my_id + "/login",
    auth=(username, password)
)



