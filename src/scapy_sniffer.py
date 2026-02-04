from scapy.all import *
from scapy.layers.http import HTTPRequest
import threading
from queue import Queue
from typing import Callable, Optional
import re

class HttpSniffer:
    def __init__(self, iface="eth0", target_host: Optional[str] = None):
        self.iface = iface
        self.target_host = target_host
        self.sniffer = None
        self.packet_queue = Queue()
        self.running = False
        self.callbacks = []

    def process_packet(self, packet):
        if self.target_host and not re.search(self.target_host, str(packet)):
            return
            
        if packet.haslayer(TCP) and packet[TCP].dport == 80:
            print(f"[SNIFFER] TCP->target:80 {packet[IP].src}:{packet[TCP].sport} -> {packet[IP].dst}:{packet[TCP].dport}")
            
        if packet.haslayer(HTTPRequest):
            host = packet[HTTPRequest].Host.decode() if packet[HTTPRequest].Host else "?"
            path = packet[HTTPRequest].Path.decode() if packet[HTTPRequest].Path else "/"
            method = packet[HTTPRequest].Method.decode() if packet[HTTPRequest].Method else "?"
            
            print(f"[SNIFFER] HTTP {method} {host}{path}")
            
            if packet.haslayer(Raw):
                payload = packet[Raw].load.decode('utf-8', errors='ignore')
                print(f"[SNIFFER] PAYLOAD: {payload[:200]}...")
        
        # Логируем в очередь для основного потока
        self.packet_queue.put(packet.summary())

    def start(self):
        self.running = True
        filter_str = "tcp and port 80"  # HTTP трафик
        if self.target_host:
            filter_str += f" and host {self.target_host}"
            
        self.sniffer = AsyncSniffer(
            iface=self.iface,
            filter=filter_str,
            prn=self.process_packet,
            store=False
        )
        self.sniffer.start()
        print(f"[SNIFFER] Запущен на {self.iface}, фильтр: {filter_str}")

    def stop(self):
        self.running = False
        if self.sniffer:
            self.sniffer.stop()
            self.sniffer.join()
        print("[SNIFFER] Остановлен")

    def add_callback(self, callback: Callable):
        self.callbacks.append(callback)
