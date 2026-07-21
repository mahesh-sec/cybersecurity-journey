# Python Port Scanner

A multithreaded TCP port scanner written in Python using sockets, threading, and a queue for concurrent scanning, with a command-line interface via argparse.

## What it does

Scans a target IP across a range of ports and reports whether each port is open or closed, using TCP connect scanning (a full three-way handshake via `socket.connect_ex()`).

## How it works

- Ports to scan are loaded into a `Queue`.
- A configurable pool of worker threads (default 50) pull ports from the queue concurrently and scan them, dramatically speeding up scanning versus a single-threaded loop (since scanning is I/O-bound — most time is spent waiting on the network, not computing).
- A `threading.Lock` prevents overlapping thread output when printing results.
- Target, port range, and thread count are all configurable via command-line flags.

## Usage

```bash
python3 port-scanner.py -t <target_ip> [-p <port_range>] [-T <thread_count>]
```

**Flags:**
- `-t`, `--target` (required) — target IP address to scan
- `-p`, `--port` (optional, default `1-1024`) — port range to scan, e.g. `1-1024`
- `-T`, `--threads` (optional, default `50`) — number of worker threads

**Example:**

```bash
python3 port-scanner.py -t 192.168.56.101 -p 1-1024 -T 100
```

## Example output

```
port 22 is open
port 80 is open
port 135 is closed
...
```

## Security concept

This tool demonstrates a **TCP connect scan** — the same technique as `nmap -sT`. It completes the full TCP handshake (SYN → SYN-ACK → ACK) for each port, which is simple to implement but more detectable than a **SYN scan** (`nmap -sS`), which never completes the handshake and requires raw socket privileges.

Verified against Metasploitable (192.168.56.101): this script and both `nmap -sT` and `nmap -sS` identified the same 12 open ports, confirming the script's correctness. Unlike Nmap, this script only identifies whether a port is open — it doesn't perform service/version detection (e.g. identifying "port 80 → Apache httpd"), since that requires actively probing and parsing service banners, which Nmap does via its service-fingerprint database and which this tool doesn't yet attempt.

## Limitations / next steps

- No service/version identification (planned for Day 5's banner grabber tool)
- No output-to-file option yet
