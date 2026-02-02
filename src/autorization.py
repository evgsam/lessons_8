import os
from dotenv import load_dotenv
import requests

#не свечу свои данные в коде
load_dotenv()
my_id = os.getenv("MY_ID")
username = os.getenv("USERNAME")
password = os.getenv("PSWRD")
base_url = f"https://google-gruyere.appspot.com/" 

session = requests.Session()

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
    response = session.post(
        url,
        data=data,
        auth=auth,
        timeout=timeout
    )
    handle_status(response.status_code)
    return response 

 
def send_snippet():
    snippet_data = "test3"
    params = {
        'snippet': snippet_data
    }
    response = session.get(f"{base_url}{my_id}/newsnippet2&snippet={snippet_data}")
    #https://google-gruyere.appspot.com/671230628526485053983130881449723357254/login?uid=user&pw=user
    #https://google-gruyere.appspot.com/671230628526485053983130881449723357254/newsnippet2?snippet=%27hello3!%27

    #response = requests.get(f"{base_url}{my_id}/newsnippet2", params=params)
    #if response.status_code == 200:
    #    print("Сниппет успешно отправлен!")
    #    print(f"Ответ сервера: {response.text[:500]}...")  # Первые 500 символов ответа
    #else:
    #    print(f"Ошибка: {response.status_code}")
    #    print(response.text)

def main():
   # login_data = {
   #     'uid': username,
    #    'pw': password,
    #}

    #response = post_req(f"{base_url}{my_id}/login", login_data)
    shippet_data = "MY snippet1"

    response = session.get(f"{base_url}{my_id}/login?uid={username}&pw={password}")
    if "Sign in" not in response.text and "login" not in response.text.lower():
        print("✓ Авторизация успешна!")
    else:
        print("✗ Авторизация не удалась!")
        print(f"Ответ: {response.text[:500]}")

    response = session.get(f"{base_url}{my_id}/newsnippet2?snippet={shippet_data}")
    #https://google-gruyere.appspot.com/671230628526485053983130881449723357254/newsnippet2?snippet=%27hello!%27

    #send_snippet()


if __name__ == "__main__":
    main()


