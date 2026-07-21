import socket
import threading
from queue import Queue

print_lock = threading.Lock()

def sock_scan(ip_addr, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    result = sock.connect_ex((ip_addr, port))
    with print_lock:
        if result == 0:
            print(f"port {port} is open")
        else:
            print(f"port {port} is closed")
    sock.close()

def worker(ip_addr, q):
    while True:
        port = q.get()
        sock_scan(ip_addr, port)
        q.task_done()

if __name__ == "__main__":
    ip_addr = "127.0.0.1"
    ports = range(1, 1025)
    q = Queue()

    for i in range(50):
        t = threading.Thread(target=worker, args=(ip_addr, q))
        t.daemon = True
        t.start()

    for port in ports:
        q.put(port)

    q.join()
