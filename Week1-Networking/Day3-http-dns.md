# Day 3 — DNS Deep Dive + HTTP/HTTPS + Wireshark Analysis

**Date:** [fill in your date]  
**Phase:** Foundation (Week 1)  
**Focus:** DNS resolution, HTTP/HTTPS basics, live packet analysis  
**PCAP file:** `capthttp.pcapng` — 5,716 packets captured  

---

## What I Studied Today

### 1. DNS — How It Actually Works

DNS is the internet's phonebook. When you type a domain name, DNS translates it to an IP address before any connection is made.

**Resolution process (recursive):**
1. Browser checks its own cache
2. OS checks its local cache
3. Query goes to your configured DNS resolver (usually your router or ISP)
4. Resolver checks its cache — if miss, contacts root nameserver
5. Root nameserver returns the address of the TLD nameserver (e.g. `.com`)
6. TLD nameserver returns the authoritative nameserver for that domain
7. Authoritative nameserver returns the actual IP (A or AAAA record)
8. Resolver caches the result for TTL seconds and returns it to you

**Recursive vs Iterative:**
- **Recursive:** your resolver does all the legwork — you ask once, you get the final answer
- **Iterative:** the resolver gives you a referral ("ask this server next") and you chase it yourself

**DNS Record Types:**

| Record | Purpose | Example |
|--------|---------|---------|
| A | Maps domain → IPv4 | `github.com → 140.82.112.21` |
| AAAA | Maps domain → IPv6 | `github.com → 2606:50c0:8000::215` |
| CNAME | Alias one domain to another | `www.example.com → example.com` |
| MX | Mail server for domain | `example.com → mail.example.com` |
| TXT | Arbitrary text (used for SPF, DKIM) | `v=spf1 include:...` |
| PTR | Reverse lookup — IP → domain | `140.82.112.21 → github.com` |

**DNS Caching (TTL):**
Every DNS response comes with a TTL (Time To Live) in seconds. The resolver keeps the answer cached for that duration. This is why DNS changes take time to propagate — old answers stay cached until TTL expires.

**How DNS is Abused:**
- **DNS Spoofing / Cache Poisoning:** Attacker injects a fake record into a resolver's cache — next person who asks gets the attacker's IP instead of the real one. Redirects users to malicious sites silently.
- **DNS Tunneling:** Data is encoded inside DNS query/response packets to exfiltrate information out of a network through firewalls that allow DNS but block other traffic.

---

### 2. HTTP/HTTPS Basics

**HTTP Methods:**
- `GET` — retrieve a resource; parameters visible in URL (`?q=search`); idempotent (same result every time)
- `POST` — send data to server in the request body; used for forms, logins, file uploads; not idempotent

**Common Status Codes:**

| Code | Meaning | When You See It |
|------|---------|----------------|
| 200 | OK | Successful request |
| 301 | Moved Permanently | Site has a new URL — update bookmarks |
| 302 | Found (temp redirect) | Temporary redirect |
| 403 | Forbidden | You don't have permission |
| 404 | Not Found | Resource doesn't exist |
| 500 | Internal Server Error | Something broke on the server |

**Key HTTP Headers:**
- `Host` — which domain the request is for (important for virtual hosting)
- `User-Agent` — identifies the client (browser, OS, version)
- `Accept` — what content types the client can handle
- `Cookie` — session data sent with every request to that domain
- `Set-Cookie` — server telling the browser to store a cookie
- `Content-Type` — format of the request/response body

**Cookies vs Sessions:**
- A **cookie** is a small piece of data stored in the browser, sent automatically with every matching request
- A **session cookie** exists only while the browser is open
- A **persistent cookie** has an expiry date set by the server
- Security risk: cookies can be stolen via XSS (cross-site scripting) → session hijacking

**HTTP vs HTTPS:**
HTTP sends everything in plaintext. HTTPS wraps HTTP inside TLS — the content is encrypted and the server's identity is verified via certificate. In my PCAP, **every single web connection used HTTPS** — zero plaintext HTTP — which is the modern default.

---

### 3. Wireshark Lab — Live PCAP Analysis (`capthttp.pcapng`)

**Capture stats:**
- Total packets: **5,716**
- DNS queries: **98** (both A and AAAA types)
- TLS records: **746**
- QUIC frames: **3,345**
- ARP packets: **16**
- My machine IP (IPv4): `192.168.0.103`
- My machine IP (IPv6): `2406:b400:28:136c:b0b6:7512:eeab:8c70`
- Router (TP-Link): `192.168.0.1` — MAC `20:23:51:d4:22:80`

**Key Finding — No Plaintext HTTP:**
The `http` Wireshark filter returned zero packets. Every connection used HTTPS (TLS on port 443) or QUIC (HTTP/3 over UDP 443). This is expected in 2025 — almost all traffic is encrypted. To study raw HTTP headers you need to either visit an `http://` site or provide the browser's TLS session key log file (`SSLKEYLOGFILE`).

**DNS Observations:**
Every hostname had both an A and AAAA query sent simultaneously — this is modern dual-stack DNS. My machine queried both record types in parallel (e.g. frames 69 and 70 both queried `srtb.msn.com`).

DNS hosts resolved in this capture:
  github.com, api.github.com, alive.github.com, collector.github.com,

avatars.githubusercontent.com, user-images.githubusercontent.com,

github-cloud.s3.amazonaws.com, www.bing.com, r.bing.com, c.bing.com,

th.bing.com, c.msn.com, api.msn.com, assets.msn.com, srtb.msn.com,

ntp.msn.com, img-s-msn-com.akamaized.net, browser.events.data.msn.com,

sb.scorecardresearch.com, r.msftstatic.com, edge.microsoft.com,

functional.events.data.microsoft.com, nav-edge.smartscreen.microsoft.com,login.live.com


**Interesting: Tracking Domain Without Visiting It**
`sb.scorecardresearch.com` appeared in the DNS queries even though I never navigated there directly. The browser resolved it as background telemetry from one of the pages I visited. This is how trackers work — embedded in pages as scripts that your browser silently contacts.

**TLS Handshake Structure (visible even in encrypted traffic):**
Before encryption starts, the TLS Client Hello is sent in plaintext. It contains:
- SNI (Server Name Indication) — the domain being connected to, readable without decryption
- Cipher suites offered by the client
- TLS version being requested

Wireshark filter to find Client Hellos: `tls.handshake.type == 1`

**QUIC / HTTP3:**
A large portion of the capture (3,345 frames) was QUIC — a Google-designed transport protocol that runs HTTP/3 over UDP port 443 instead of TCP. The handshake was visible: `Initial` packets with DCID (Destination Connection ID), then `Handshake` packets, then `Protected Payload`. QUIC is faster than TCP+TLS because it combines the transport and crypto handshakes into one round trip.

**ARP Exchange (frames 6–7):**
  Router (192.168.0.1) → broadcast: "Who has 192.168.0.103?"

My machine (192.168.0.103) → "I'm at 2c:3b:70:fa:3b:7d"
This is normal ARP — the router resolving my MAC address to forward packets. Repeated 8 times throughout the capture (16 packets total: 8 requests, 8 replies).

**Wireshark Filters Used:**
  dns                          → all DNS traffic

dns.flags.response == 0      → queries only

tls.handshake.type == 1      → TLS Client Hello (shows SNI)

tcp.stream eq 0              → follow first TCP stream

arp                          → ARP requests and replies

quic                         → all QUIC/HTTP3 frames
---

### 4. Nmap Flag Reference

| Flag | Name | What It Does |
|------|------|-------------|
| `-sS` | SYN Scan (stealth) | Sends SYN, doesn't complete handshake — less noisy in logs |
| `-sV` | Version Detection | Probes open ports to identify service and version |
| `-sC` | Default Scripts | Runs Nmap's default NSE scripts for common info gathering |
| `-p` | Port Specification | e.g. `-p 80,443` or `-p 1-1000` or `-p-` (all ports) |
| `-A` | Aggressive | Enables `-sV`, `-sC`, OS detection, traceroute together |
| `-T4` | Timing Template 4 | Faster scan — good for reliable networks |
| `-O` | OS Detection | Tries to fingerprint the target OS from packet responses |

---

## Key Takeaways

- DNS happens before any HTTP connection — every website visit starts with a DNS query, and you can see it in Wireshark before the TLS handshake
- Modern web traffic is almost entirely encrypted — the `http` filter is nearly useless on current captures; use TLS SNI to identify sites instead
- QUIC (HTTP/3) is now dominant on many connections — it's UDP-based, faster, and harder to inspect than TCP+TLS
- Tracking domains resolve silently in background — `sb.scorecardresearch.com` appeared without me visiting it directly
- ARP is purely local — it maps IPs to MACs and only works within a single network segment

---

## Resources Used

- Computerphile — "How DNS Works"
- NetworkChuck — "HTTP Explained"
- Wireshark live capture: `capthttp.pcapng`
- picoCTF — Networking/Forensics beginner challenges

---

## Files in This Folder
