# OSI Layer — Protocols & Attacks Table

> Protocols marked ★ were directly observed in the Day 1 live capture.

| Layer | Name | Protocol 1 | Protocol 2 | Protocol 3 | Attack |
|-------|------|-----------|-----------|-----------|--------|
| 7 | Application | ★ HTTP | ★ DNS | ★ LLMNR | **LLMNR Poisoning** — attacker responds to multicast name queries to steal NTLMv2 hashes (Responder tool) |
| 6 | Presentation | ★ TLS 1.3 | SSL (deprecated) | MIME | **SSL Stripping** — downgrade HTTPS → HTTP so traffic is cleartext (Bettercap) |
| 5 | Session | NetBIOS | RPC | PPTP | **Session Hijacking** — steal valid session token to impersonate authenticated user |
| 4 | Transport | ★ TCP | ★ UDP | ★ QUIC | **SYN Flood** — flood SYN packets without completing handshake, exhausting server connections |
| 3 | Network | ★ ICMP | ★ IGMP | OSPF | **IP Spoofing** — forge source IP to bypass IP-based authentication |
| 2 | Data Link | ★ ARP | Ethernet II | PPP | **ARP Spoofing** — send fake ARP replies to link attacker MAC with legitimate IP (MitM) |
| 1 | Physical | Ethernet | Wi-Fi 802.11 | Bluetooth | **Wiretapping / RF Jamming** — physically tap cable or jam wireless signals |

---

## Why LLMNR Matters
LLMNR (UDP 5355) is a Windows fallback when DNS fails. It broadcasts on the local subnet:
*"Who is [hostname]?"*
An attacker running **Responder** answers — capturing the NTLMv2 hash of whoever asked.
That hash can be cracked offline or relayed for authentication.
This was observed live on Day 1 before even studying attacks.

## Why QUIC is Interesting
QUIC combines transport + encryption over UDP port 443.
It merges the TCP handshake and TLS handshake into one round trip — reducing latency.
Modern Chrome uses QUIC heavily, which is why it appeared without visiting anything unusual.

## Layer 5 Absence Explained
The OSI Session layer was designed for mainframe-era protocols like X.25.
In modern networking, session management lives inside TLS (L6) or the application itself (L7).
An empty L5 in a real capture is completely accurate and expected.
