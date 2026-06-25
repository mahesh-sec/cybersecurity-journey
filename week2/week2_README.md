# Week 2 — Network Protocol Attacks, PCAP Analysis & Service Enumeration

Summary of everything covered across Days 1–6 of Week 2, with links to the detailed write-up for each day.

## Day-by-Day Breakdown

### [Day 1 — HTTP Deep Dive + PCAP Analysis](./day1/README.md)
Cold analysis of `http.cap` (Wireshark sample capture): TCP handshake, HTTP GET/response cycle, TCP segmentation/reassembly of a large response body, a parallel ad-server connection, and a DNS lookup mid-capture. Verified findings using `tcp.flags.syn==1`, `http.request`, `http.response`, `dns`, and `tcp.flags.fin==1` filters. Corrected an early mix-up between request-only and response-only headers.

### [Day 2 — Protocol Attack Theory + DHCP/Nmap Labs](./day2/)
Built the core **Protocol Attack Table** (`protocols attacks.md`) covering ARP poisoning, DHCP starvation, HTTP request smuggling, and DNS spoofing. Supplemented with deeper theory on [DNS tunneling and DNS amplification DDoS](./day2/Dns%20tunneling%20amplification.md) — covering exfiltration/C2 via subdomain encoding, and open-resolver-based amplification attacks. Hands-on labs: captured a full DHCP DORA exchange (`dhcp-dora-lab.md`) and ran a full Nmap scan against Metasploitable2 (`nmap-metasploitable-scan.md`).

### [Day 3 — TLS 1.2 vs 1.3 + Backdoor PCAP Analysis](./day3/README.md)
**Theory:** Full TLS 1.2 RSA handshake breakdown (ClientHello → ServerHello → Certificate → CertificateVerify → key exchange → Finished), with the signature/encryption distinction worked through explicitly. TLS 1.3 changes: ECDHE-only key exchange, 1 round trip, forward secrecy, and encrypted certificates. Documented why HTTPS still leaks metadata regardless of TLS version: SNI sent in plaintext (no ECH in practice), IP addresses always visible, and traffic-pattern analysis remains possible even when content is encrypted.

**Practical:** [Full incident report](./day3/pcap-analysis-report.md) on `dns-remoteshell.pcap` — a backdoor command shell found bound to three separate ports (53, 23, 80) on a compromised Windows XP host, used to evade port-based firewall filtering by hiding behind the normally-allowed DNS port. Reconstructed the full timeline from TCP stream payloads, fingerprinted the backend OS via a failed Unix command, and flagged a likely-duplicate-capture artifact (dual-interface merge) rather than misreading it as real retransmission.

### [Day 4 — Service Enumeration: FTP, SMB, Netcat, CVE Mapping](./day4/README.md)
Enumerated FTP, SMB, and ran a netcat-based manual banner-grab sweep across Metasploitable2, then built a verified CVE findings table.

- [`ftp-anonymous-enumeration.md`](./day4/ftp-anonymous-enumeration.md) — confirmed anonymous FTP login succeeds (vsFTPd 2.3.4) but write access is correctly restricted (`553 Could not create file`)
- [`smb-enumeration.md`](./day4/smb-enumeration.md) — anonymous SMB session enumerated shares (`tmp` with anonymous READ/WRITE), pulled live artifacts out of `/tmp` (Java service PID, active X11 session), and enumerated user accounts via `smb-enum-users` (2 live human accounts: `msfadmin`, `user`)
- [`netcat-basics.md`](./day4/netcat-basics.md) — manual banner grabs across FTP/SSH/Telnet/SMTP/MySQL, `dig`-based BIND version extraction via CHAOS-class query, and a demonstrated port-binding conflict between `sshd` and a netcat listener on port 22
- [`service-cve-findings.md`](./day4/service-cve-findings.md) — verified CVE table; caught and corrected two mismatched CVE citations (Telnet, SMTP) and one overstated severity rating (SSH) from an earlier draft before finalizing
- [`concepts-reference.md`](./day4/concepts-reference.md) — reusable concept notes: enumeration vs. vulnerability analysis, share lists vs. actual filesystem, service accounts vs. human accounts, and CVE-verification discipline

### [Day 5 — SOC Analyst Mindset & PCAP Anomaly Detection](./day5/README.md)
Shifted from learning individual attacks to baseline-vs-anomaly thinking across DNS, HTTP, ARP, and SMB.

- [`pcap-analysis.md`](./day5/pcap-analysis.md) — cold analysis of a RARP request/reply pair (correctly reinterpreted after an initial false-positive read) and an ARP storm capture (622 requests/29s, 0 replies, 9 gateway identities sweeping 303 targets — parsed via scapy)
- [`protocol-self-test.md`](./day5/protocol-self-test.md) — wrote out DNS resolution, TCP handshake, DHCP DORA, ARP poisoning, and TLS handshake from memory, then checked against ground truth (DNS: missing OS/hosts-cache layer; TLS: signing-vs-encryption and RSA-vs-ECDHE mixups caught and corrected; DHCP and ARP poisoning: fully correct)
- [`detection-rules.md`](./day5/detection-rules.md) — recognition-level detection flags for ARP poisoning, DHCP starvation, HTTP smuggling, DNS tunneling, and DNS spoofing, plus a reference table mapping each to Wireshark filter logic and MITRE ATT&CK/CAPEC/CWE identifiers
- [`wireshark-cheatsheet.md`](./day5/wireshark-cheatsheet.md) — filters practiced live against the ARP storm capture, including why `ip.addr` silently fails on ARP traffic and why a zero-result filter can itself be meaningful evidence rather than a mistake

### Day 6 — Consolidation: SQL Injection, NSE Scripting, Internal Verification
Reviewed Week 2 theory aloud, then three hands-on blocks against Metasploitable2/DVWA:

- **DVWA SQL injection** across Low/Medium/High security — demonstrated the classic `' OR '1'='1` tautology bypass at Low (full table dump), an error-based leak at Medium (blind character-escaping produces a broken-but-revealing SQL syntax error), and a clean block at High (parameterized queries bind input as pure data, never entering query structure)
- **Nmap NSE scripting** — `http-title` confirmed the DVWA page title cleanly; `smb-vuln-ms17-010` returned no result, correctly traced to the target running **Samba 3.0.20-Debian** rather than Windows SMB, since MS17-010/EternalBlue is Windows-specific
- **Internal vs. external verification** — SSH'd into Metasploitable2 and compared `ps aux` / `netstat -tulnp` against the morning's external Nmap results: confirmed exact binaries behind every open port (e.g. 445 = `smbd`, 8180 = Tomcat via `jsvc`), and surfaced services not obvious from the port scan alone (an externally-reachable Ruby DRb timeserver running as root on 8787, `distccd` listening with no IP allow-list on 3632, and NFS/portmapper fully exposed)

## Tools Used

- **Wireshark** / **tshark** — protocol dissection, filter-based analysis, verbose packet inspection
- **scapy** — programmatic PCAP statistics (ARP storm packet-count/ratio analysis)
- **Kali Linux** — attack-side VM for all hands-on labs
- **Metasploitable2** (`192.168.56.101`) — intentionally vulnerable target VM
- **nmap** — port/service/version scanning, NSE scripting (`ftp-anon`, `smb-enum-shares`, `smb-enum-users`, `smb-vuln-*`, `http-title`, `smb-vuln-ms17-010`)
- **netcat** — manual banner grabbing, listener mode, port-binding conflict demonstration
- **dig** — DNS version disclosure via CHAOS-class TXT query
- **ftp** client — manual anonymous login and write-access testing
- **smbclient** — anonymous SMB share listing and file-level inspection
- **DVWA** — SQL injection practice across all three security levels
- **SSH** — remote access to Metasploitable2 for internal verification
- **ps aux** / **netstat -tulnp** — internal process and listening-socket inspection
- **VirtualBox** — Host-Only networking lab environment

## PCAPs Analyzed

| File | Day | Focus |
|---|---|---|
| `http.cap` | 1 | HTTP GET/response cycle, TCP segmentation, parallel ad-server connection |
| (DHCP DORA capture) | 2 | Full Discover/Offer/Request/Ack exchange |
| `dns-remoteshell.pcap` | 3 | Backdoor command shell disguised as DNS traffic, confirmed on 3 ports |
| `rarp_req_reply.pcapng` | 5 | RARP request/reply — legacy IP-assignment protocol, reinterpreted after an initial false-positive |
| `220703_arp-storm.pcapng` | 5 | High-volume zero-reply ARP sweep across 9 gateway identities |
| `PRIV_bootp-both_overload_empty-no_end.pcap` | 6 | Malformed DHCP Discover — sname/file option overload, 3 distinct missing-End-option errors |
| `tcp-ethereal-file1.trace` | 6 | Plaintext HTTP POST — 152,372-byte file upload reassembled across 132 TCP segments |

## Concepts Mastered

**Protocol attack theory:** ARP poisoning (reactive + gratuitous variants), DHCP starvation and option-overload malformation, DNS spoofing, DNS tunneling (exfiltration/C2 via subdomain encoding), DNS amplification DDoS (open-resolver abuse), HTTP request smuggling (CL.TE/TE.CL header conflict), SQL injection (tautology bypass vs. escaping vs. parameterized queries)

**Protocol internals:** TCP three-way handshake/teardown/segmentation, full DHCP DORA sequence, TLS 1.2 vs. 1.3 (RSA vs. ECDHE key exchange, forward secrecy, certificate plaintext-vs-encrypted, CertificateVerify signing vs. encryption, SNI metadata leakage), DNS resolution chain (including OS/hosts-file cache layer), SMB enumeration (shares, null sessions, user/RID enumeration) vs. targeted vulnerability checks

**Reconnaissance & scripting:** Full nmap port/service scans, NSE script categories and targeted scripts, manual protocol interaction via netcat, banner-grab-based version fingerprinting, DNS version disclosure via CHAOS queries

**CVE verification discipline:** Confirming exact vendor/version match against a CVE's stated affected range before citing it; treating misconfigurations (e.g. passwordless MySQL root) as valid critical findings independent of any CVE number; cross-checking CVSS scores against vendor severity labels

**SOC analyst mindset:** Baseline-vs-anomaly reasoning across DNS/HTTP/ARP/SMB; separating mechanism (what a device is doing) from anomaly (what's statistically abnormal about how it's doing it); separating confirmed evidence from hypothesis when escalating; recognizing that a zero-result filter can itself be meaningful evidence

**Linux system verification:** `/etc/passwd` structure (UID ranges, shell field as login-capability indicator), service accounts vs. human accounts and the principle of least privilege, `ps aux` vs. `netstat -tulnp` (all running processes vs. only listening sockets), matching externally-scanned ports to confirmed internal binaries and privilege levels
