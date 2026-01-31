import httpx
import asyncio
from urllib.parse import urljoin

async def check_endpoint(base_url, endpoint):
    """Проверяет доступность endpoint"""
    url = urljoin(base_url, endpoint)
    async with httpx.AsyncClient(timeout=3.0, follow_redirects=True) as client:
        try:
            start_time = asyncio.get_event_loop().time()
            response = await client.get(url)
            elapsed = asyncio.get_event_loop().time() - start_time
            
            return {
                "url": url,
                "status": response.status_code,
                "exists": response.status_code < 400,
                "time": f"{elapsed:.2f}s",
                "size": len(response.content) if response.content else 0
            }
        except httpx.TimeoutException:
            return {"url": url, "status": "timeout", "exists": False}
        except Exception as e:
            return {"url": url, "status": "error", "error": str(e), "exists": False}

async def scan_directories(base_url, directories):
    """Сканирует список директорий асинхронно"""
    print(f"Начинаю сканирование {len(directories)} директорий...")
    
    tasks = [check_endpoint(base_url, dir_path) for dir_path in directories]
    results = await asyncio.gather(*tasks)
    
    # Разделяем результаты на найденные и ненайденные
    found = [r for r in results if r.get("exists")]
    not_found = [r for r in results if not r.get("exists")]
    
    print(f"Сканирование завершено. Найдено: {len(found)}, Не найдено: {len(not_found)}")
    return found

async def main():
    """Основная асинхронная функция"""
    # Конфигурация
    base_url = "https://httpbin.org"
    common_dirs = [
        "/",  # корень
        "/admin",
        "/api",
        "/.git",
        "/backup",
        "/test",
        "/status",
        "/headers",
        "/ip",
        "/user-agent",
        "/get",
        "/post",
        "/put",
        "/delete"
    ]
    
    # Запуск сканирования
    found = await scan_directories(base_url, common_dirs)
    
    # Вывод результатов
    print("\n" + "="*60)
    print("НАЙДЕННЫЕ ДИРЕКТОРИИ:")
    print("="*60)
    
    if found:
        for item in found:
            print(f"[{item['status']:3}] {item['url']}")
            if 'time' in item and 'size' in item:
                print(f"      ⏱ {item['time']} | 📦 {item['size']} bytes")
    else:
        print("Доступные директории не найдены.")
    
    print("="*60)
    print(f"Итого: {len(found)} доступных endpoint")

# Запуск
if __name__ == "__main__":
    asyncio.run(main())