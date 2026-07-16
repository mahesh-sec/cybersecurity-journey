"""
Day 1 Lab: socket library basics
Tests whether a given port is open or closed on a target host using
socket.connect_ex(), which returns 0 on success instead of raising an
exception (useful for scanning many ports without try/except everywhere).
"""

import socket

def check_port(host, port, timeout=2):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)

    result = sock.connect_ex((host, port))
    sock.close()

    return result == 0


if __name__ == "__main__":
    target = "192.168.56.101"  # Metasploitable

    for port in [21, 22, 80, 9999]:
        if check_port(target, port):
            print(f"Port {port} is open")
        else:
            print(f"Port {port} is closed")
