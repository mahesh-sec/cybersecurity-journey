# Week 4 — Python for Security & Log/Service Enumeration

Week 4 shifted focus from Linux internals (Week 3) to Python scripting for security tooling, plus continued OverTheWire Bandit practice and deeper service enumeration.

## Python Tools

| Tool | Description |
|---|---|
| [Multithreaded Port Scanner](day2/README.md) | Scans a TCP port range on a target host concurrently using a thread pool, reporting open/closed status per port. |
| [File Hash Generator](day3/README.md) | Computes a cryptographic hash (default SHA-256) for every file in a directory — for integrity checks and forensic baselining. |
| [SSH Auth Log Parser & Brute-Force Detector](day4/README.md) | Parses SSH auth logs, extracts login attempts by user/IP, and alerts when failed attempts cross a threshold. |
| [Service Banner Grabber](day5/README.md) | Connects to target ports and grabs service banners to identify running software and versions. |

## Bandit (OverTheWire)

- **Levels solved this week:** [13 → 22](bandit-writeups.md)
- **Continuing next week:** 22 → 33
- Techniques covered across this range included SSL/TLS-based password submission (`openssl s_client`, distinguishing real listeners from decoy echo services), `env`/setuid helper binaries (`bandit20-do`), and client/listener password relay via `nc` + `suconnect`.

## SMB Enumeration

- [SMB Deep Enumeration Write-Up](day6/smb-deep-enum.md) — deep-dive enumeration of SMB shares/services on the lab target, building on the Nmap/NSE and FTP/SMB enumeration work from Week 2.
