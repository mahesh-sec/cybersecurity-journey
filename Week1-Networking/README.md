# Week 1 — What I Learned

**Duration:** 7 days | **Hours logged:** ~63 hrs (9 hrs/day)
**Phase:** Foundation (Weeks 1–6) | **Status:** ✅ Complete

---

## 🧠 Concepts Studied

### OSI & TCP/IP Models
- All 7 OSI layers and their roles — Physical through Application
- PDU names at each layer: bits → frames → packets → segments → data
- How TCP/IP collapses the 7-layer model into 4 layers, and why that matters in practice
- Encapsulation going down the stack; de-encapsulation going up
- When engineers reference OSI vs TCP/IP and why both models still matter

### TCP — Deep Dive
- 3-way handshake: SYN → SYN-ACK → ACK, with actual Seq/Ack number arithmetic
- 4-way termination: FIN → ACK → FIN → ACK, and why it's asymmetric
- All 6 TCP flags and what each triggers: SYN, ACK, FIN, RST, PSH, URG
- Sequence and Acknowledgment math — counting bytes transmitted, not packets
- PDU reassembly: how Wireshark reconstructs a full HTTP body from fragmented TCP segments
- RTT measurement from Seq/Ack pairs in a live capture

### DNS
- Full resolution chain: stub resolver → recursive resolver → root nameserver → TLD → authoritative
- Record types: A, AAAA, CNAME, MX, NS, TXT, PTR — when each is used
- CNAME chaining — how `www.example.com` can chain through multiple aliases to an A record
- TTL and caching at every hop; why stale cache causes hard-to-debug failures
- Why DNS defaults to UDP/53 but falls back to TCP for zone transfers and large responses
- Privacy-preserving DNS: DoH (DNS over HTTPS) and DoT (DNS over TLS)

### HTTP & HTTPS
- HTTP/1.1 request/response structure: method, headers, status line, body
- Status code families and key codes: 200, 301, 302, 400, 401, 403, 404, 500, 503
- How HTTPS = HTTP inside a TLS tunnel — port 443 vs 80, nothing else changes at the HTTP layer
- HTTP/1.1 vs HTTP/2 (multiplexing, header compression via HPACK) vs HTTP/3 (QUIC-based)
- Why HTTP/3 traffic appears as "QUIC" in Wireshark with fully encrypted payloads

### TLS 1.3 — Handshake Internals
- Full handshake packet-by-packet:
  `ClientHello` → `ServerHello` → `{EncryptedExtensions, Certificate, CertificateVerify, Finished}` → `[client Finished]`
- Cipher suites in TLS 1.3: `TLS_AES_128_GCM_SHA256`, `TLS_AES_256_GCM_SHA384`, `TLS_CHACHA20_POLY1305_SHA256`
- ECDH key exchange — how both sides derive an identical shared secret without ever transmitting it
- Key schedule: `(EC)DHE` input → HKDF-Extract → HKDF-Expand → handshake traffic keys → application traffic keys
- Why TLS 1.3 killed RSA key exchange (no forward secrecy) and deprecated CBC, RC4, SHA-1
- What `Change Cipher Spec` means in TLS 1.3 — a legacy compatibility record, not a functional signal
- PSK session resumption and 0-RTT data — performance win, replay attack risk

### Cookies & Session Security
- Cookie attributes and what each does: `HttpOnly`, `Secure`, `SameSite` (Strict/Lax/None), `Path`, `Domain`, `Expires`
- How `HttpOnly` blocks JavaScript `document.cookie` access — preventing direct theft
- XSS-based session hijacking: injected script → exfiltrate session cookie → attacker replays it
- Why `HttpOnly` doesn't fully stop XSS — attacker can still make authenticated requests via JS without reading the cookie
- `SameSite=Strict` as a CSRF mitigation layer
- Cookie interception when `Secure` flag is absent over HTTP

### Defense in Depth (DiD)
- 7-layer DiD model: Policies → Physical → Perimeter → Network → Endpoint → Application → Data
- Control placement: firewalls at perimeter/network, EDR at endpoint, WAF at application, encryption at data
- Lateral movement — why perimeter breach alone doesn't mean full compromise with proper DiD
- VLANs as network segmentation — containing blast radius
- Security policy hierarchy: Policy → Standard → Procedure → Guideline

### Additional Protocols (from live captures)
- **ARP** — IP-to-MAC resolution; broadcast request, unicast reply; gratuitous ARP and spoofing potential
- **IGMP** — multicast group join/leave; seen in home network captures from streaming devices
- **SSDP** — UPnP device discovery over UDP/1900; why it's an attack surface on local networks
- **ICMPv6 / NDP** — Neighbour Discovery Protocol replacing ARP in IPv6; Router Solicitation/Advertisement
- **QUIC** — UDP-based, multiplexed streams, built-in TLS 1.3; the transport under HTTP/3

---

## 🛠️ Tools Used

| Tool | How I Used It |
|------|---------------|
| **Wireshark** | Live captures on active interface; loaded pcap/pcapng files; wrote display filters (`tls`, `dns`, `http`, `tcp`, `arp`, `quic`); followed TCP streams; inspected TLS 1.3 ClientHello cipher suites; measured RTT via Seq/Ack arithmetic; identified QUIC/HTTP3 traffic |
| **Kali Linux (VirtualBox)** | Primary environment for all captures and tooling |
| **Nmap** | Basic host discovery, port scanning, service version detection |
| **Browser DevTools** | Inspected live HTTP request/response headers; verified cookie attributes (`HttpOnly`, `Secure`, `SameSite`) on real sites |
| **PicoCTF** | Platform setup; initial challenge exploration |

---

## 📖 Resources Used

| Resource | Purpose |
|----------|---------|
| NetworkChuck (YouTube) | OSI model, DNS resolution, HTTP/HTTPS visual walkthroughs |
| Professor Messer (YouTube) | Defense in Depth, security controls, policy hierarchy |
| IppSec (YouTube) | CTF methodology, practical tool usage |
| PortSwigger Web Academy | Cookie security, XSS session hijacking (reading + theory) |
| RFC 8446 | TLS 1.3 specification — cross-referenced against Wireshark captures |
| Wireshark Documentation | Display filter syntax, protocol dissector references |

---

## 🧪 Labs & Hands-On Work

- [x] Live Wireshark capture — identified and filtered DNS, TLS, ARP, IGMP, SSDP, ICMPv6, QUIC traffic on a real interface
- [x] Analysed a full TLS 1.3 handshake packet-by-packet in Wireshark — matched each record to the key schedule
- [x] Traced a complete DNS resolution chain in a live capture — CNAME chain → A record
- [x] Followed a TCP stream in Wireshark — reconstructed a full HTTP response from multiple segments
- [x] Manually worked through Seq/Ack arithmetic across a multi-packet TCP exchange
- [x] Identified HTTP/3 (QUIC) traffic and confirmed encrypted payload structure
- [x] Verified cookie security attributes (`HttpOnly`, `Secure`, `SameSite`) in browser DevTools on live production sites
- [x] PicoCTF platform setup and initial challenge exploration

---

## 💡 Key Takeaways

> **TLS 1.3 encrypts most of its own handshake.** By the time you see a `Certificate` record in Wireshark, it's already inside an encrypted wrapper. The server's identity is hidden from passive observers — something TLS 1.2 never achieved.

> **DNS is the phonebook — and a major attack surface.** DNS hijacking, cache poisoning, data exfiltration over DNS queries — all of it flows from this one protocol that most traffic depends on but almost nobody filters properly.

> **`HttpOnly` is not a silver bullet against XSS.** It blocks `document.cookie` reads, but an attacker with script execution can still make authenticated requests on the victim's behalf. Real session security needs `HttpOnly` + `Secure` + `SameSite` + a strong CSP, layered together.

> **Wireshark doesn't lie.** When my understanding of ARP conflicted with what I actually saw in a capture, the capture was right. Reading specs is good. Reading packets is better.

---

## ⏭️ Coming Up — Week 2

- Linux filesystem, permissions, and user management
- Bash scripting for security automation
- File analysis tools: `strings`, `file`, `xxd`, `grep`
- Log analysis fundamentals
- Cron jobs and persistence mechanisms (attacker perspective)
