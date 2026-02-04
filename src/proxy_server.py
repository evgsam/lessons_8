# proxy_server.py
import socket
import socketserver
import threading
from urllib.parse import urlsplit

HOP_BY_HOP = {
    "proxy-connection", "connection", "keep-alive", "te",
    "trailers", "transfer-encoding", "upgrade"
}
#чтение из сокета потока байт
def _recv_until(sock: socket.socket, marker: bytes, limit: int = 1024 * 1024) -> bytes:
    data = b""
    while marker not in data:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk
        if len(data) > limit:
            raise ValueError("Header too large")
    return data
#чтение байт
def _read_exact(sock: socket.socket, n: int) -> bytes:
    out = b""
    while len(out) < n:
        chunk = sock.recv(n - len(out))
        if not chunk:
            break
        out += chunk
    return out
#класс прокси
class ProxyHandler(socketserver.BaseRequestHandler):
    def handle(self):
        client = self.request
        client.settimeout(10)

        head = _recv_until(client, b"\r\n\r\n")
        if not head:
            return

        header_part, rest = head.split(b"\r\n\r\n", 1)
        lines = header_part.split(b"\r\n")
        try:
            method, raw_target, version = lines[0].decode("iso-8859-1").split(" ", 2)
        except ValueError:
            return

        # Парсим заголовки
        headers = {}
        for ln in lines[1:]:
            if b":" not in ln:
                continue
            k, v = ln.split(b":", 1)
            headers[k.decode("iso-8859-1").strip().lower()] = v.decode("iso-8859-1").strip()

        # Определяем host/port/path
        # Для proxy обычно приходит absolute-form: GET http://host:port/path HTTP/1.1
        # Но иногда может прийти origin-form + Host:
        if raw_target.startswith("http://") or raw_target.startswith("https://"):
            u = urlsplit(raw_target)
            host = u.hostname
            port = u.port or 80
            path = (u.path or "/") + (("?" + u.query) if u.query else "")
        else:
            host_hdr = headers.get("host")
            if not host_hdr:
                return
            if ":" in host_hdr:
                host, p = host_hdr.rsplit(":", 1)
                port = int(p)
            else:
                host, port = host_hdr, 80
            path = raw_target

        # Дочитываем body если есть Content-Length
        body = rest
        cl = headers.get("content-length")
        if cl is not None:
            need = int(cl) - len(body)
            if need > 0:
                body += _read_exact(client, need)

        # Чистим hop-by-hop
        out_headers = []
        for k, v in headers.items():
            if k in HOP_BY_HOP:
                continue
            if k == "host":
                continue
            out_headers.append((k, v))

        # Собираем запрос к target (origin-form) и корректные CRLF
        req = []
        req.append(f"{method} {path} {version}\r\n")
        req.append(f"Host: {host}\r\n")
        for k, v in out_headers:
            req.append(f"{k}: {v}\r\n")
        req.append("Connection: close\r\n")
        req.append("\r\n")
        req_bytes = "".join(req).encode("iso-8859-1") + body

        # Подключаемся к target и форвардим
        upstream = socket.create_connection((host, port), timeout=10)
        try:
            upstream.sendall(req_bytes)

            # Пересылаем ответ обратно (как есть)
            while True:
                chunk = upstream.recv(4096)
                if not chunk:
                    break
                client.sendall(chunk)
        finally:
            upstream.close()

class ProxyServer:
    def __init__(self, proxy_ip: str, proxy_port: int):
        self.host = proxy_ip
        self.port = proxy_port
        self.server = socketserver.ThreadingTCPServer((proxy_ip, proxy_port), ProxyHandler)
        self.server.daemon_threads = True
        self.thread = None

    def start(self):
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        print(f"[PROXY] Запущен на {self.host}:{self.port}")

    def stop(self):
        self.server.shutdown()
        self.server.server_close()
        if self.thread:
            self.thread.join()
        print("[PROXY] Остановлен")
