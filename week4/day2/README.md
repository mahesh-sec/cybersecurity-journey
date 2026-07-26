# Multithreaded TCP Port Scanner

## What It Does
Scans a range of TCP ports on a target host and reports which ones are open or closed. Uses a thread pool (via `threading` + `queue.Queue`) to check multiple ports concurrently instead of one at a time, so a full 1–1024 sweep finishes in seconds rather than minutes.

## How It Works
- A `Queue` is loaded with every port number in the requested range.
- A configurable number of worker threads pull ports off the queue and attempt a TCP connection (`connect_ex`) with a 3-second timeout.
- A `threading.Lock` guards `print()` so output from concurrent threads doesn't interleave and get garbled.

## Usage
```bash
python port_scanner.py -t <target_ip> [-p <port_range>] [-T <threads>]
```

| Flag | Description | Default |
|---|---|---|
| `-t`, `--target` | Target IP address (required) | — |
| `-p`, `--port` | Port range, e.g. `1-1024` | `1-1024` |
| `-T`, `--threads` | Number of worker threads | `50` |

**Example:**
```bash
python port_scanner.py -t 192.168.56.101 -p 1-1024 -T 100
```

## Example Output
```
port 21 is open
port 22 is open
port 80 is open
port 23 is closed
port 139 is open
port 445 is open
port 3306 is closed
```
*(Output order will vary between runs since threads complete out of sequence — this is expected with concurrent scanning.)*

## Security Concept
This tool implements **TCP connect scanning**, the reconnaissance technique behind tools like Nmap's `-sT` scan. Identifying open ports is the first step of the enumeration phase in a penetration test or SOC investigation — it maps a host's attack surface before any service/version fingerprinting (banner grabbing) or vulnerability research happens. The threading design also demonstrates why real scanners are fast: sequential, single-socket scanning of 1,024 ports at a 3-second timeout would take much longer than a concurrent sweep.

## Possible Improvements
- Add a `try/except` around `connect_ex` to handle unreachable hosts gracefully instead of hanging per-thread.
- Support scanning a list/CIDR of hosts, not just a single IP.
