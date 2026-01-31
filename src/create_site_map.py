import requests
from bs4 import BeautifulSoup
import json
import re  # Добавляем импорт re
import os
from dotenv import load_dotenv
from urllib.parse import urljoin  # Добавляем для правильного объединения URL

load_dotenv()
my_id = os.getenv("MY_ID")

def filter_id(text):
    """Заменяет my_id на [FILTERED] в тексте"""
    if not text or not my_id:
        return text
    return text.replace(my_id, '[FILTERED]')

def filter_url(url):
    """Фильтрует ID в URL"""
    if not url or not my_id:
        return url
    # Простая замена my_id, а не паттерн для любых длинных чисел
    return url.replace(my_id, '[FILTERED]')

def filter_id_in_sitemap(data, my_id):
    """
    Рекурсивно заменяет my_id на [FILTERED] во всей структуре site_map
    """
    if not my_id:  # если my_id пустой, нечего заменять
        return data
    
    if isinstance(data, dict):
        filtered_dict = {}
        for key, value in data.items():
            # Фильтруем ключи (если они строки)
            filtered_key = filter_id(key) if isinstance(key, str) else key
            filtered_value = filter_id_in_sitemap(value, my_id)
            filtered_dict[filtered_key] = filtered_value
        return filtered_dict
    
    elif isinstance(data, list):
        return [filter_id_in_sitemap(item, my_id) for item in data]
    
    elif isinstance(data, str):
        return filter_id(data)
    
    else:  # числа, булевы значения, None
        return data

def create_site_map(base_url):
    """Создает карту сайта со всеми формами и полями"""

    site_map = {
        "base_url": filter_url(base_url),  # Фильтруем сразу
        "pages": {}
    }
    
    visited = set()  # Для отслеживания уже посещенных страниц
    
    def crawl(url, depth=0, max_depth=3):
        if depth > max_depth or url in visited:
            return
        
        # Выводим оригинальный URL в логах
        print(f"{'  ' * depth}📄 {url}")
        visited.add(url)
        
        try:
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text, 'html.parser')
            
            page_info = {
                "forms": [],
                "links": [],
                "url_params": []
            }
            
            # Формы - фильтруем данные при сборе
            for form in soup.find_all('form'):
                form_info = {
                    "action": filter_id(form.get('action')),
                    "method": filter_id(form.get('method', 'GET')),
                    "inputs": []
                }
                
                for inp in form.find_all(['input', 'textarea', 'select']):
                    form_info["inputs"].append({
                        "name": filter_id(inp.get('name')),
                        "type": filter_id(inp.get('type', inp.name)),
                        "id": filter_id(inp.get('id'))
                    })
                
                page_info["forms"].append(form_info)
            
            # Ссылки - фильтруем данные при сборе
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith('/') or base_url in href:
                    page_info["links"].append({
                        "text": filter_id(link.text.strip()[:50]),
                        "href": filter_id(href)
                    })
            
            # URL параметры - фильтруем значения параметров
            if '?' in url:
                params = url.split('?')[1].split('&')
                filtered_params = []
                for param in params:
                    if '=' in param:
                        key, value = param.split('=', 1)
                        filtered_params.append(f"{key}={filter_id(value)}")
                    else:
                        filtered_params.append(filter_id(param))
                page_info["url_params"] = filtered_params
            
            # Сохраняем под отфильтрованным URL ключом
            filtered_url_key = filter_url(url)
            site_map["pages"][filtered_url_key] = page_info
            
            # Рекурсивно обходим ссылки
            for link in page_info["links"][:10]:  # Ограничиваем глубину
                next_url = urljoin(url, link["href"])  # Используем urljoin для корректного объединения
                if base_url in next_url:
                    crawl(next_url, depth + 1, max_depth)
                    
        except Exception as e:
            print(f"{'  ' * depth}❌ Ошибка: {e}")
    
    crawl(base_url)

    # Дополнительная фильтрация всего site_map (на всякий случай)
    filtered_site_map = filter_id_in_sitemap(site_map, my_id)
    
    # Сохраняем в JSON
    with open('gruyere_sitemap.json', 'w', encoding='utf-8') as f:
        json.dump(filtered_site_map, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Карта сайта сохранена в gruyere_sitemap.json")
    print(f"🔒 MY_ID '{my_id}' заменен на '[FILTERED]' во всех местах")
    
    return filtered_site_map 

# Запуск
load_dotenv()
my_id = os.getenv("MY_ID")
url = f"https://google-gruyere.appspot.com/{my_id}/"
create_site_map(url)