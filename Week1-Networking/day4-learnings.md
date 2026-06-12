# Day 4 — DHCP + ARP + ICMP + First Nmap Scan
**Date:** 2026-06-12
**Phase:** Week 1 — Networking Foundations
**Focus:** Protocol Theory + Nmap Reconnaissance

---

## What I Learned Today

### DHCP — DORA Process
DHCP (Dynamic Host Configuration Protocol) automatically assigns IP addresses to devices on a network. It follows a 4-step process called DORA:

| Step | Message | What happens |
|---|---|---|
| Discover | Client → Broadcast | "I need an IP address" — sent to 255.255.255.255 |
| Offer | Server → Client | "Here is an available IP + lease time" |
| Request | Client → Broadcast | "I accept that IP offer" |
| Acknowledge | Server → Client | "Confirmed — IP is yours" |

**How attackers exploit DHCP:**
- **DHCP Starvation** — flood the server with fake MAC addresses, exhaust the IP pool
- **Rogue DHCP Server** — set up a fake server after starvation, assign attacker-controlled gateway → full MITM

---

### ARP — IP to MAC Mapping
ARP (Address Resolution Protocol) maps IP addresses to MAC addresses at Layer 2. When a device wants to communicate, it broadcasts "who has IP x.x.x.x?" and the owner replies with its MAC address. The result is stored in the ARP cache.

**Key weakness:** No authentication — any device can send a fake ARP reply and overwrite the cache.

**How attackers exploit ARP:**
- **ARP Spoofing / Poisoning** — send fake ARP replies linking attacker MAC to victim IP → traffic redirected through attacker → MITM, session hijack, or DoS

---

### ICMP — Error Reporting and Diagnostics
ICMP (Internet Control Message Protocol) is the feedback layer for IP. Since IP has no built-in error reporting, ICMP fills that gap. It operates at Layer 3 and has no port number.

| Type | Code | Meaning |
|---|---|---|
| 8 | 0 | Echo Request (ping sent) |
| 0 | 0 | Echo Reply (ping response) |
| 3 | 0-4 | Destination Unreachable (network/host/port/fragmentation) |
| 11 | 0 | Time Exceeded (used by traceroute) |

**How attackers exploit ICMP:**
- **Ping Flood** — overwhelm target with echo requests → DoS
- **Smurf Attack** — spoof victim IP, send broadcast ping → entire network replies to victim → amplified DoS
- **Ping of Death** — oversized ICMP packet causes buffer overflow (older systems)
- **ICMP Redirect** — fake "better route" message → silently redirect traffic through attacker

---

### TCP vs UDP
| Feature | TCP | UDP |
|---|---|---|
| Connection | 3-way handshake required | Connectionless |
| Reliability | Guaranteed delivery | No guarantee |
| Speed | Slower | Faster |
| Use cases | HTTP, HTTPS, SSH, FTP | DNS, DHCP, ICMP, NTP |

---

## Nmap Scans Performed

### Target: 192.168.0.1 (Home Router — TP-Link WAP)

#### Scan 1 — Version Detection
```
nmap -sV 192.168.0.1
```

**Output:**
```
Host is up (0.0050s latency)
Not shown: 998 filtered tcp ports (no-response)

PORT      STATE  SERVICE  VERSION
80/tcp    open   http     TP-LINK WAP http config
1900/tcp  open   upnp     Portable SDK for UPnP devices 1.6.19 (Linux 3.10.14; UPnP 1.0)

Service Info: OS: Linux; Device: WAP; CPE: cpe:/o:linux:linux_kernel:3.10.14
```

---

#### Scan 2 — Aggressive Scan
```
nmap -A 192.168.0.1
```

**Output:**
```
Host is up (0.0018s latency)
Not shown: 998 filtered tcp ports (no-response)

PORT      STATE  SERVICE  VERSION
80/tcp    open   http     TP-LINK WAP http config
|_http-title: Site doesn't have a title (text/html; charset=utf-8)
1900/tcp  open   upnp     Portable SDK for UPnP devices 1.6.19 (Linux 3.10.14; UPnP 1.0)

Warning: OSScan results may be unreliable
OS CPE: cpe:/o:linux:linux_kernel:3.10.14
Service Info: OS: Linux; Device: WAP

TRACEROUTE (using port 80/tcp)
HOP  RTT      ADDRESS
1    0.37ms   192.168.0.1

Nmap done: 1 IP address (1 host up) scanned in 20.96 seconds
```

---

## Port Analysis

### Port 80 — HTTP (TP-LINK Admin Panel)
- **What it is:** Router's admin web panel served over HTTP
- **How to access:** Open browser → type `192.168.0.1` → enter credentials
- **Security implication:** Admin panel served over unencrypted HTTP (not HTTPS). Login credentials travel as plaintext. Anyone on the network running Wireshark could capture the admin password.

### Port 1900 — UPnP
- **What it is:** Universal Plug and Play — allows devices to auto-discover each other and open ports without manual configuration
- **Version:** Portable SDK for UPnP 1.6.19 — known vulnerable version
- **Security implication:** UPnP has a long CVE history. Attackers can abuse UPnP to open arbitrary ports on the router, bypass firewall rules, and expose internal services to the internet.

---

## Nmap Scan Types Reference

| Flag | What it does |
|---|---|
| `-sS` | SYN/stealth scan — half-open, never completes handshake |
| `-sV` | Version detection of services on open ports |
| `-sC` | NSE script scan — auto-interacts with open services for extra info |
| `-O` | OS detection via TCP/IP fingerprinting |
| `-sU` | UDP scan — finds services running on UDP |
| `-A` | Aggressive — combines -sV, -sC, -O, traceroute |
| `-Pn` | Skip host discovery, assume host is up |
| `-p-` | Scan all 65535 ports |

---

## Port States Explained

| State | Meaning | Reply received |
|---|---|---|
| Open | Service is running and listening | SYN-ACK |
| Closed | Port reachable but nothing listening | RST |
| Filtered | Firewall silently dropping packets | No reply |

---

## Key Concepts

- **Nmap host discovery:** Sends ICMP echo request first to check if host is up, then begins port scan
- **`-A` does NOT include UDP** — must add `-sU` separately for UDP services
- **TCP scan misses UDP services** — DHCP (67/68), DNS (53), NTP (123) need `-sU`
- **998 filtered ports** = router firewall silently dropping all probes (drop policy, not reject)
- **1 hop traceroute** = Kali and router are directly on the same network segment

---

## Security Observations

1. Router admin panel running on HTTP (port 80) — not HTTPS — credentials exposed in plaintext
2. UPnP version 1.6.19 running — outdated, known vulnerabilities — should be disabled if not needed
3. Linux kernel 3.10.14 — very old (2013) — likely unpatched CVEs exist
4. 998 ports filtered — router has a strict drop firewall policy — good security hygiene
5. Default credentials risk — if admin/admin still works, full router compromise possible

---

## Resources Used Today
- Professor Messer — CompTIA Network+ DHCP videos (x2)
- Professor Messer — ARP/DNS Poisoning
- Professor Messer — ICMP (Other Useful Protocols N10-009)
- nmap.org — scan types reference
