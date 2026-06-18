# PCAP Analysis Report — Backdoor Shell Disguised as DNS Traffic

| | |
|---|---|
| **File analyzed** | `dns-remoteshell.pcap` |
| **Tool used** | Wireshark / tshark |
| **Analyst** | Mahesh |
| **Date** | Week 2, Day 3 — Cybersecurity Self-Study Roadmap |

---

## 1. Executive Summary

An internal host (`192.168.1.3`) used a pre-installed backdoor on a compromised Windows XP
machine (`192.168.1.2`) to obtain a remote command shell, connecting over TCP port 53 —
normally reserved for DNS — specifically to evade port-based firewall filtering. The same
backdoor shell was confirmed reachable on three separate ports (53, 23, 80), while a probe
of port 21 found nothing listening, indicating a multi-port backdoor rather than any of
these being legitimate DNS, Telnet, or HTTP services.

---

## 2. Findings Summary

| Finding | Detail |
|---|---|
| **Backdoor host** | `192.168.1.2` (Windows XP) |
| **Operator host** | `192.168.1.3` |
| **Malicious ports confirmed** | TCP/53, TCP/23, TCP/80 — all return identical shell |
| **Port probed, not backdoored** | TCP/21 (FTP) — closed, connection refused |
| **Evasion technique** | Backdoor bound to port 53 to blend in with allowed outbound DNS traffic |
| **OS fingerprint confirmed via** | `ls -la` (Unix command) rejected with Windows-style error |
| **Initial compromise vector** | Not visible in this capture — backdoor was already installed |
| **Capture artifact** | Duplicate frames due to dual-interface capture (not real retransmission) |

---

## 3. Timeline

| # | Frame(s) | Time (rel.) | Source → Destination | Event |
|---|----------|-------------|------------------------|-------|
| 1 | 1–10 | 0.00s–2.96s | `192.168.1.3` ↔ `192.168.1.1` | Background ARP resolution and legitimate DNS queries (gateway PTR lookup → `SpeedTouch.lan`; A-record lookups for `www.www.com`). Benign noise, not part of the incident. |
| 2 | 14 | 25.49s | `192.168.1.3:1396` → `192.168.1.2:53` | TCP SYN to port 53 (DNS port). |
| 3 | 17–20 | 25.50s | `192.168.1.2` ↔ `192.168.1.3` | Three-way handshake completes. No DNS query/response follows — payload is not DNS-formatted. |
| 4 | 21 | 25.56s | `192.168.1.2:53` → `192.168.1.3:1396` | 88-byte payload: Windows XP command-shell banner + `C:\>` prompt (confirmed via TCP stream reassembly). |
| 5 | 25 | 27.85s | `192.168.1.3` → `192.168.1.2:53` | 4-byte payload: `dir` command typed. |
| 6 | 27, 31 | 27.89s–28.02s | `192.168.1.2:53` → `192.168.1.3` | 201-byte and 1011-byte payloads: full `C:\` directory listing returned, including files of interest. |
| 7 | 35–38 | 30.78s–30.80s | `192.168.1.3` ↔ `192.168.1.2` | `exit` sent; both sides RST, session closes. |
| 8 | 39–46 | 48.48s–48.94s | `192.168.1.3:1399` → `192.168.1.2:21` | Two connection attempts to port 21 (FTP) — both SYNs immediately answered with RST; nothing listening. |
| 9 | 47–49, 66–75 | 48.95s–73.18s | various external hosts | Unrelated background traffic (TLS handshake to `205.227.136.203`, HTTP request to `83.170.75.178`). Not part of the incident. |
| 10 | 76 | 75.78s | `192.168.1.3:1403` → `192.168.1.2:23` | TCP SYN to port 23 (real Telnet port). |
| 11 | 83 | 75.85s | `192.168.1.2:23` → `192.168.1.3` | Identical 88-byte shell banner returned — same backdoor, now confirmed on Telnet port too. |
| 12 | 87–94 | 77.34s–77.50s | both directions | `dir` run again; identical directory listing returned. |
| 13 | 97–100 | 79.02s–79.09s | `192.168.1.3` → `192.168.1.2:23` | Attacker tries `ls -la` (Unix command). Shell responds with Windows' "'ls' is not recognized..." error — confirms backend OS is Windows. |
| 14 | 105–108 | 85.57s | both directions | `exit` sent; both sides RST, session closes. |
| 15 | 109 | 96.44s | `192.168.1.3:1404` → `192.168.1.2:80` | TCP SYN to port 80 (HTTP port). |
| 16 | 115–125 | 96.51s–98.22s | both directions | Same banner, same `dir` command, same listing — third confirmation of the same shell bound to a third port. |
| 17 | 128–131 | 99.71s–99.73s | both directions | `exit` sent; RST closes the final session. |

**Note on duplicate frames:** Many packets in this capture appear twice with different
source/destination MAC addresses (one Ethernet pair, one WLAN/LLC pair). This is because the
capture was merged from two interfaces observing the same physical traffic, causing
Wireshark to flag legitimate duplicates as `[TCP Retransmission]`, `[TCP Dup ACK]`, or
`[TCP Out-of-Order]`. This is a capture artifact, not evidence of real packet loss or
retransmission on the wire.

---

## 4. Captured Shell Session (Sample)

Reassembled TCP stream showing the backdoor banner and a `dir` command issued over port 53:

```
C:\>dir

 Volume in drive C has no label.
 Volume Serial Number is XXXX-XXXX

 Directory of C:\

[DATE]  [TIME]    <DIR>          quarantine
[DATE]  [TIME]                   s37g
[DATE]  [TIME]                   s3fs
[DATE]  [TIME]                   aierrorlog.txt
[DATE]  [TIME]                   installer-debug.txt
[DATE]  [TIME]                   systemscandata.txt
```

OS fingerprinting attempt on the Telnet session (port 23):

```
C:\>ls -la
'ls' is not recognized as an internal or external command,
operable program or batch file.
```

---

## 5. Indicators of Compromise (IOCs)

### Internal hosts involved

| IP Address | MAC Address | Role |
|---|---|---|
| `192.168.1.2` | `00:80:48:24:33:32` / `00:10:c6:30:6b:b3`* | Compromised host — Windows XP, running the backdoor shell |
| `192.168.1.3` | `00:0e:35:78:0c:02` | Internal host used to connect to and operate the backdoor |
| `192.168.1.1` | `00:90:d0:eb:46:e7` | Network gateway (`SpeedTouch.lan` ADSL router) — uninvolved in the incident |

*\*Two MAC addresses for the same IP confirm the dual-interface capture artifact noted above.*

### Ports

| Port | Expected Service | Observed Behavior |
|---|---|---|
| TCP/53 | DNS | **Backdoor command shell (malicious)** |
| TCP/21 | FTP | Closed — connection refused, not backdoored |
| TCP/23 | Telnet | **Backdoor command shell (malicious)** |
| TCP/80 | HTTP | **Backdoor command shell (malicious)** |

### Suspicious filenames (revealed via `dir` output)

| Filename | Notes |
|---|---|
| `quarantine\` | Directory — possibly AV-quarantined items |
| `s37g` | Non-standard filename, no extension |
| `s3fs` | Non-standard filename, no extension |
| `aierrorlog.txt` | Unclear origin |
| `installer-debug.txt` | Unclear origin |
| `systemscandata.txt` | Possibly tied to a prior AV/security scan |

### Unrelated background traffic (for completeness — not part of the incident)

- DNS query: `www.www.com` → resolved to `63.215.91.200`
- External hosts contacted by `192.168.1.2`: `140.112.253.189`, `205.227.136.203` (TLS),
  `83.170.75.178` (HTTP `GET /images/empty.gif`)

---

## 6. Conclusion

The attacker at `192.168.1.3` was operating an already-installed backdoor on
`192.168.1.2`, not exploiting a vulnerability live in this capture — the initial compromise
happened before the capture starts. The attacker's actions show systematic verification of
backdoor access: first connecting over TCP/53 (chosen because outbound DNS traffic is rarely
blocked by firewalls), then probing TCP/21 and finding it closed, then confirming the
identical shell was also reachable over the legitimate Telnet port (23) and HTTP port (80).

In every successful session the attacker ran the same `dir` command to confirm filesystem
access, and on the Telnet session specifically tested `ls -la`, which failed in a way that
confirmed the compromised host's OS. The presence of a `quarantine\` folder and oddly named
files (`s37g`, `s3fs`) in the directory listing are consistent with leftovers from a prior
malware infection or AV action, though this cannot be confirmed from network traffic alone.
No evidence in this capture shows how the backdoor was originally installed — only that it
existed and was actively used.

---

*Report generated as part of Week 2, Day 3 Wireshark/PCAP analysis training —
see [`README.md`](README.md) in this folder for the accompanying TLS theory notes.*
