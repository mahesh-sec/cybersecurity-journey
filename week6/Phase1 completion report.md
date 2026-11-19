# Phase 1 Completion Report (Weeks 1–6)

**Author:** Patimini Mahesh · **Goal:** SOC Analyst / Penetration Tester
**Program:** Self-directed 24-week cybersecurity roadmap (free resources only) · **Lab:** Kali Linux + Metasploitable2 (VirtualBox, Host-Only network)

Phase 1 built the foundation: networking, Linux, scripting, web application security, and the threat-intelligence language (MITRE ATT&CK) that SOC teams use every day. This report is my baseline going into Phase 2.

---

## 1. Tools I can use

| Tool | What I can do with it |
|---|---|
| **Nmap / NSE** | Host discovery, port and service scanning, NSE scripts; used against Metasploitable2 |
| **Wireshark** | Live captures, PCAP forensics, following TCP streams, spotting ARP/DNS/DHCP attacks and TLS handshakes |
| **Bash** | Wrote 3 security scripts: subnet scanner, auth-log parser, system report; cron, process and log monitoring |
| **Python** | Functions, file handling, dictionaries, threading, argparse, datetime, regex for log analysis |
| **Regex / grep / CLI tools** | Failed logins per user, non-existent user attempts, log filtering |
| **Burp Suite Community** | Proxy and scope, HTTP history, Repeater, Intruder (Sniper, Battering Ram, Pitchfork, Cluster Bomb), Decoder, Comparer |
| **enum4linux / smbmap** | SMB enumeration against Metasploitable2 |
| **FTP/SMB enumeration** | Anonymous access checks and share enumeration |
| **SSH (keygen, authorized_keys, journalctl)** | Key-based auth, auth-chain analysis through logs |
| **Git / GitHub** | Portfolio repo `mahesh-sec/cybersecurity-journey`, `weekN/dayN` structure |
| **MITRE ATT&CK Navigator/website** | Reading groups, techniques, sub-techniques; mapping attacks to IDs |
| **Anki** | ~20 cards/day across all weeks |

## 2. Concepts I understand

**Networking**
- OSI and TCP/IP models, DNS, HTTP/HTTPS, DHCP, ARP, TCP vs UDP
- TLS 1.2 vs 1.3 handshakes, ECDH key exchange
- IPv4, NAT, routing, firewalls, wireless encryption, subnetting/CIDR/VLSM
- VirtualBox network modes (Host-Only, NAT, NAT Network)
- Network attacks: ARP poisoning, DNS spoofing/tunneling/amplification, DHCP starvation

**Linux**
- Filesystem hierarchy, permissions, SUID/SGID, GTFOBins
- Users, groups and authentication internals, sudoers misconfigurations
- Logging, cron, systemd, process monitoring, package management
- Privilege escalation enumeration; cron privilege escalation patterns
- SSH internals: transport handshake, host authentication, public-key vs password auth, session ID as replay protection

**Web application security (OWASP Top 10)**
- SQL injection (Low/Medium/High), reflected, stored and DOM XSS, SSRF
- Authentication weaknesses, brute force and credential attacks, rate limiting and account lockout
- CSRF token validation, plaintext credentials in intercepted traffic
- Why Intruder results alone overstate risk without checking real defenses

**Threat intelligence and MITRE ATT&CK**
- Four intel levels: strategic, operational, tactical, technical, and who consumes each
- ATT&CK matrix: tactics (why), techniques (how), sub-techniques, ID format (T1566.001)
- Indicators of Compromise (hashes, IPs, domains, artifacts) and David Bianco's Pyramid of Pain
- Threat actor profiling: APT29 (espionage), Lazarus (disruption/finance), FIN7 (profit), and how motivation shapes technique choice

## 3. Labs completed

| Platform | Lab / exercise |
|---|---|
| **Metasploitable2** | Nmap scanning, SMB/FTP enumeration, internal vs external service verification, nmap SUID exploit |
| **Linux privesc** | Sudoers misconfiguration analysis, GTFOBins triage, SUID deep-dive with compiled C binaries, cron privesc patterns |
| **DVWA** | SQL injection (Low/Medium/High), reflected XSS, brute force with Burp Intruder, password-change flow with Repeater, login interception |
| **PortSwigger Web Security Academy** | All Apprentice SQLi labs; 3 XSS labs (reflected, stored, DOM); first 2 SSRF labs |
| **Wireshark** | Live captures and PCAP forensics |
| **Bandit (OverTheWire)** | Wargame progress (levels per my notes) |
| **SSH lab** | Kali to Metasploitable2 authentication chain via journalctl |
| **Burp Suite** | Full Proxy → Repeater → Intruder → Decoder → Comparer workflow on DVWA |
| **Threat intel** | IOC extraction from a public malware report; kill-chain tables for APT29, Lazarus, FIN7 |

## 4. Checkpoints

- Week 2 checkpoint: ~87%
- Weeks 3–6 checkpoints completed

## 5. Known gaps / going into Phase 2

- Security+ exam objectives
- SOC tooling and SIEM (log ingestion, detection rules, alert triage)
- Active Directory attacks and defense
- Cloud security (Azure for Students account already set up)
- Deeper pentest methodology and reporting
