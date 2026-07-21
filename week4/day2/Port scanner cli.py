import socket
import threading
from queue import Queue
import argparse

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

def workers(ip_addr, q):
    while True:
        port = q.get()
        sock_scan(ip_addr, port)
        q.task_done()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Multithreaded TCP port scanner")
    parser.add_argument("-t", "--target", required=True, help="Target IP address")
    parser.add_argument("-p", "--port", default="1-1024", help="Port range, e.g. 1-1024")
    parser.add_argument("-T", "--threads", default="50", type=int, help="Number of worker threads")
    args = parser.parse_args()

    start, end = args.port.split("-")
    ports = range(int(start), int(end) + 1)

    q = Queue()

    for i in range(args.threads):
        t = threading.Thread(target=workers, args=(args.target, q))
        t.daemon = True
        t.start()

    for port in ports:
        q.put(port)

    q.join()
