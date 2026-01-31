from scapy.all import *
import re

def extract_http_payload(pkt):
    """
    Извлекает HTTP-полезную нагрузку из пакета
    """
    if pkt.haslayer(TCP) and pkt.haslayer(Raw):
        try:
            payload = pkt[Raw].load.decode('utf-8', errors='ignore')
            return payload
        except:
            return None
    return None

def detect_xss(payload):
    """
    Обнаружение признаков XSS в тексте
    """
    xss_patterns = [
        r'<script[^>]*>.*?</script>',  # тег script
        r'javascript:',  # протокол javascript
        r'onerror\s*=',  # обработчик ошибок
        r'onload\s*=',   # обработчик загрузки
        r'onclick\s*=',  # обработчик клика
        r'alert\(',      # функция alert
        r'document\.cookie',  # доступ к кукам
        r'<img[^>]*onerror=', # XSS через img
        r'<svg[^>]*onload=',  # XSS через SVG
        r'eval\s*\(',         # функция eval
        r'<iframe[^>]*>',     # iframe инъекция
    ]
    
    detected = []
    for pattern in xss_patterns:
        matches = re.findall(pattern, payload, re.IGNORECASE | re.DOTALL)
        if matches:
            detected.append((pattern, matches[:3]))  # сохраняем первые 3 совпадения
    
    return detected

def analyze_pcap(pcap_file):
    """
    Анализ PCAP файла на наличие XSS
    """
    print(f"[*] Анализ файла: {pcap_file}")
    print("[*] Загрузка пакетов...")
    
    try:
        packets = rdpcap(pcap_file)
    except Exception as e:
        print(f"[!] Ошибка загрузки файла: {e}")
        return
    
    xss_count = 0
    total_packets = len(packets)
    
    print(f"[*] Проанализировано пакетов: {total_packets}")
    print("[*] Поиск признаков XSS...\n")
    
    for i, pkt in enumerate(packets):
        payload = extract_http_payload(pkt)
        if payload:
            xss_signatures = detect_xss(payload)
            
            if xss_signatures:
                xss_count += 1
                print(f"\n[!] Обнаружен XSS в пакете #{i}")
                print(f"    Время: {pkt.time}")
                
                # Определяем направление трафика
                if pkt.haslayer(IP):
                    src = pkt[IP].src
                    dst = pkt[IP].dst
                    print(f"    От: {src}:{pkt[TCP].sport} -> Кому: {dst}:{pkt[TCP].dport}")
                
                # Выводим найденные сигнатуры
                for pattern, matches in xss_signatures:
                    print(f"    Паттерн: {pattern}")
                    for match in matches:
                        print(f"        - {match[:100]}..." if len(match) > 100 else f"        - {match}")
                
                # Выводим фрагмент полезной нагрузки
                print(f"    Фрагмент полезной нагрузки:")
                print(f"    {payload[:300]}..." if len(payload) > 300 else f"    {payload}")
                print("-" * 80)
    
    # Статистика
    print(f"\n[*] Анализ завершен")
    print(f"[*] Всего пакетов: {total_packets}")
    print(f"[*] Пакетов с признаками XSS: {xss_count}")
    print(f"[*] Процент зараженных пакетов: {(xss_count/total_packets*100):.2f}%")

def analyze_live_traffic(interface="eth0", count=100):
    """
    Анализ живого трафика на наличие XSS
    """
    print(f"[*] Начинаю захват трафика с интерфейса {interface}")
    print("[*] Для остановки нажмите Ctrl+C\n")
    
    def packet_handler(pkt):
        payload = extract_http_payload(pkt)
        if payload:
            xss_signatures = detect_xss(payload)
            if xss_signatures:
                print(f"\n[!] Обнаружен XSS в реальном времени!")
                print(f"    Время: {pkt.time}")
                
                if pkt.haslayer(IP):
                    src = pkt[IP].src
                    dst = pkt[IP].dst
                    print(f"    От: {src} -> Кому: {dst}")
                
                for pattern, matches in xss_signatures:
                    print(f"    Паттерн: {pattern}")
                
                # Краткий фрагмент
                print(f"    Образец: {payload[:200]}...")
                print("-" * 60)
    
    # Захват пакетов
    sniff(iface=interface, filter="tcp port 80 or tcp port 8080", 
          prn=packet_handler, store=0, count=count)

def save_xss_packets(pcap_file, output_file="xss_packets.pcap"):
    """
    Сохраняет пакеты с XSS в отдельный файл
    """
    print(f"[*] Фильтрация XSS пакетов из {pcap_file}")
    
    packets = rdpcap(pcap_file)
    xss_packets = []
    
    for pkt in packets:
        payload = extract_http_payload(pkt)
        if payload and detect_xss(payload):
            xss_packets.append(pkt)
    
    if xss_packets:
        wrpcap(output_file, xss_packets)
        print(f"[*] Сохранено {len(xss_packets)} пакетов в {output_file}")
    else:
        print("[*] XSS пакеты не обнаружены")

def main():
    """
    Главное меню программы
    """
    print("=" * 60)
    print("           SCAPY XSS TRAFFIC ANALYZER")
    print("=" * 60)
    
    while True:
        print("\nВыберите действие:")
        print("1. Анализ PCAP файла")
        print("2. Анализ живого трафика")
        print("3. Сохранить XSS пакеты в отдельный файл")
        print("4. Выход")
        
        choice = input("\nВаш выбор (1-4): ").strip()
        
        if choice == "1":
            pcap_file = input("Введите путь к PCAP файлу: ").strip()
            if os.path.exists(pcap_file):
                analyze_pcap(pcap_file)
            else:
                print(f"[!] Файл {pcap_file} не найден")
        
        elif choice == "2":
            interface = input("Введите интерфейс (по умолчанию eth0): ").strip() or "eth0"
            count = input("Сколько пакетов захватить (по умолчанию 100): ").strip()
            count = int(count) if count.isdigit() else 100
            analyze_live_traffic(interface, count)
        
        elif choice == "3":
            pcap_file = input("Введите путь к PCAP файлу: ").strip()
            if os.path.exists(pcap_file):
                output_file = input("Имя выходного файла (по умолчанию xss_packets.pcap): ").strip()
                output_file = output_file if output_file else "xss_packets.pcap"
                save_xss_packets(pcap_file, output_file)
            else:
                print(f"[!] Файл {pcap_file} не найден")
        
        elif choice == "4":
            print("[*] Выход из программы")
            break
        
        else:
            print("[!] Неверный выбор")

if __name__ == "__main__":
    # Проверка прав доступа
    import os
    if os.geteuid() != 0:
        print("[!] Для захвата живого трафика требуются права администратора")
        print("[*] Анализ PCAP файлов доступен без прав root")
    
    main()