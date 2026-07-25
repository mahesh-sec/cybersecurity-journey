import socket


def sock_scanner(ip_addr, ports):
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((ip_addr, port))
        if result == 0:
            print(f"port {port} is open ")
        else:
            print(f"port {port} is closed")
        sock.close()


if __name__ == "__main__":
    sock_scanner("192.168.56.101", [445])
