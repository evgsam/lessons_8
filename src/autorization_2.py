import os
from dotenv import load_dotenv
import requests

# Загружаем переменные окружения
load_dotenv()
my_id = os.getenv("MY_ID")
username = os.getenv("USERNAME")
password = os.getenv("PSWRD")
base_url = f"http://google-gruyere.appspot.com/"

session = requests.Session()

def handle_status(code, url=""):
    if code == 200:
        return
    errors = {
        404: f"Ресурс не найден: {url}",
        429: "Слишком много запросов. Подождите.",
        403: "Доступ запрещен.",
        401: "Требуется авторизация.",
        302: "Перенаправление (возможно успешная авторизация)",
    }
    
    if code in errors:
        print(f"Статус {code}: {errors[code]}")
    elif code >= 500:
        print(f"Статус {code}: Ошибка сервера.")
    else:
        print(f"Статус {code}: Неожиданный статус.")

def post_req(url, data=None):
    try:
        response = session.post(url, data=data)
        print(f"POST {url} -> {response.status_code}")
        handle_status(response.status_code, url)
        return response
    except Exception as e:
        print(f"Ошибка при отправке POST на {url}: {e}")
        raise

def get_req(url, params=None):
    try:
        response = session.get(url, params=params)
        print(f"GET {url} -> {response.status_code}")
        handle_status(response.status_code, url)
        return response
    except Exception as e:
        print(f"Ошибка при отправке GET на {url}: {e}")
        raise

def login():
    """Авторизация на сайте"""
    login_url = f"{base_url}{my_id}/login"
    
    print(f"Пытаюсь авторизоваться на {login_url}")
    
    # Сначала получаем страницу логина (может понадобиться для CSRF)
    #response = get_req(login_url)
    #https://google-gruyere.appspot.com/671230628526485053983130881449723357254/login?uid=user&pw=user
    # Отправляем данные для авторизации
    response = post_req(f"{login_url}?uid={username}&pw={password}")
    
    # Проверяем, успешна ли авторизация
    if "Sign in" not in response.text and "login" not in response.text.lower():
        print("✓ Авторизация успешна!")
    else:
        print("✗ Авторизация не удалась!")
        print(f"Ответ: {response.text[:500]}")
    
    return response

def check_login():
    """Проверяем, авторизованы ли мы"""
    test_url = f"{base_url}{my_id}/"
    response = get_req(test_url)
    
    if "Sign in" not in response.text and username in response.text:
        print("✓ Проверка авторизации: вы вошли в систему")
        return True
    else:
        print("✗ Проверка авторизации: вы НЕ авторизованы")
        return False

def send_snippet():
    """Отправка сниппета"""
    snippet_url = f"{base_url}{my_id}/newsnippet2"
    
    # Подготовка данных - важно передавать словарь, а не строку!
    snippet_data = {
        'snippet': "Тестовый сниппет через Python. <b>Жирный текст</b>"
    }
    
    print(f"Отправляю сниппет на {snippet_url}")
    print(f"Данные: {snippet_data}")
    
    # Отправляем POST запрос с данными
    response = post_req(snippet_url, snippet_data)
    
    # Проверяем ответ
    print(f"Ответ от сервера ({len(response.text)} символов):")
    print("-" * 50)
    
    # Проверяем успешность по ключевым словам в ответе
    if "snippet" in response.text.lower() or "submitted" in response.text.lower():
        print("✓ Сервер подтвердил создание сниппета")
    else:
        print("✗ Возможно, сниппет не был создан")
    
    # Сохраняем ответ для отладки
    with open('snippet_response.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    print("✓ Ответ сохранен в snippet_response.html")
    
    return response

def check_snippets():
    """Проверяем список сниппетов"""
    snippets_url = f"{base_url}{my_id}/snippets.gtl"
    
    print(f"\nПроверяю список сниппетов на {snippets_url}")
    response = get_req(snippets_url)
    
    # Ищем наш текст в списке сниппетов
    search_text = "Тестовый сниппет через Python"
    if search_text in response.text:
        print(f"✓ Наш сниппет найден в списке!")
        
        # Найдем и покажем контекст
        idx = response.text.find(search_text)
        start = max(0, idx - 100)
        end = min(len(response.text), idx + 100)
        print(f"Контекст: ...{response.text[start:end]}...")
    else:
        print(f"✗ Наш сниппет НЕ найден в списке")
        
        # Сохраняем список сниппетов для анализа
        with open('snippets_list.html', 'w', encoding='utf-8') as f:
            f.write(response.text)
        print("✓ Список сниппетов сохранен в snippets_list.html")
        
        # Проверим, есть ли вообще какие-то сниппеты
        if "No snippets" in response.text or "нет сниппетов" in response.text.lower():
            print("На странице указано, что сниппетов нет")
        else:
            print("На странице есть другие сниппеты, но не наш")
    
    return response

def debug_form():
    """Анализируем форму создания сниппета"""
    form_url = f"{base_url}{my_id}/newsnippet2"
    
    print(f"\nАнализирую форму на {form_url}")
    response = get_req(form_url)
    
    # Сохраняем исходный код формы
    with open('form_page.html', 'w', encoding='utf-8') as f:
        f.write(response.text)
    print("✓ Страница с формой сохранена в form_page.html")
    
    # Простой анализ формы
    if '<form' in response.text:
        # Находим форму
        form_start = response.text.find('<form')
        form_end = response.text.find('</form>', form_start)
        
        if form_start != -1 and form_end != -1:
            form_html = response.text[form_start:form_end+7]
            
            # Ищем метод
            if 'method="post"' in form_html.lower():
                print("✓ Форма использует метод: POST")
            elif 'method="get"' in form_html.lower():
                print("✓ Форма использует метод: GET")
                print("⚠ ВНИМАНИЕ! Форма использует GET, попробуйте GET запрос!")
            
            # Ищем имя поля для сниппета
            if 'name="snippet"' in form_html:
                print("✓ Поле для сниппета найдено: name='snippet'")
            
            # Ищем скрытые поля
            hidden_fields = form_html.count('type="hidden"')
            if hidden_fields > 0:
                print(f"✓ Найдено скрытых полей: {hidden_fields}")
                
                # Покажем скрытые поля
                lines = form_html.split('\n')
                for line in lines:
                    if 'type="hidden"' in line:
                        print(f"  Скрытое поле: {line.strip()}")
    
    return response

def main():
    try:
        print("=" * 60)
        print("Google Gruyere: Отправка сниппета")
        print("=" * 60)
        
        # Шаг 1: Авторизация
        login()
        
        # Шаг 2: Проверяем авторизацию
        if not check_login():
            print("Не удалось авторизоваться. Завершаю работу.")
            return
        
        # Шаг 3: Анализируем форму
        debug_form()
        
        # Шаг 4: Отправляем сниппет
        send_snippet()
        
        # Шаг 5: Проверяем, появился ли сниппет
        check_snippets()
        
        print("\n" + "=" * 60)
        print("Завершено!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()