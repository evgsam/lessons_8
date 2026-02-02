import requests
from bs4 import BeautifulSoup
import urllib.parse

import os
from dotenv import load_dotenv


def analyze_site(base_url):
    """Анализирует все ссылки и формы на сайте"""
    visited = set()
    to_visit = [base_url]
    
    while to_visit:
        url = to_visit.pop(0)
        if url in visited:
            continue
            
        print(f"\n Анализирую: {url}")
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Находим ВСЕ формы
            forms = soup.find_all('form')
            for form in forms:
                print(f"\n Форма найденa на {url}")
                print(f"   Action: {form.get('action', 'Текущая страница')}")
                print(f"   Method: {form.get('method', 'GET').upper()}")
                
                # Все поля формы
                inputs = form.find_all(['input', 'textarea', 'select'])
                for inp in inputs:
                    name = inp.get('name', 'Без имени')
                    type_attr = inp.get('type', inp.name)
                    print(f"   Поле: {name} ({type_attr})")
            
            # Находим ВСЕ ссылки
            links = soup.find_all('a', href=True)
            for link in links:
                href = link['href']
                # Преобразуем относительные ссылки в абсолютные
                full_url = urllib.parse.urljoin(url, href)
                if base_url in full_url and full_url not in visited:
                    to_visit.append(full_url)
                    print(f"   🔗 Найдена ссылка: {link.text.strip()} -> {href}")
            
            visited.add(url)
            
        except Exception as e:
            print(f" Ошибка при анализе {url}: {e}")
    
    print(f"\n Проанализировано {len(visited)} страниц")

# Использование
load_dotenv()
my_id = os.getenv("MY_ID")
url = f"https://google-gruyere.appspot.com/{my_id}/"
analyze_site(url)
