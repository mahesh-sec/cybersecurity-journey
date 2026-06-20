# Service Enumeration & CVE Findings — Metasploitable2

**Date:** Week 2, Day 4
**Target:** 192.168.56.101 (Metasploitable2)
**Method:** Full port/service scan → manual CVE verification on cve.mitre.org/NVD → exploit availability check on exploit-db.com

---

## 1. Objective

Identify five open services on Metasploitable2, determine the exact CVE(s) associated with each running version, verify those CVEs actually apply to the specific software version in use, and check whether a public exploit exists. This mirrors what a penetration tester delivers as a findings table in a client report.

**Important methodology note:** An earlier draft of this table contained two mismatched CVEs (a Telnet CVE for unrelated, modern software, and an SMTP CVE for an unrelated platform) and one overstated severity rating. Every entry below was re-verified against primary sources before inclusion. This is intentional — citing an unverified CVE in a real report is a credibility failure, and double-checking version/vendor match against the CVE description is a mandatory step, not an optional one.

---

## 2. Findings Table

| Port | Service | Version | CVE | CVSS / Severity | Exploit-DB | Risk Level |
|---|---|---|---|---|---|---|
| 21 | FTP | vsftpd 2.3.4 | CVE-2011-2523 | 8.1 (High/Critical) | Yes — EDB-ID 49757, Metasploit `exploit/unix/ftp/vsftpd_234_backdoor` | **Critical** |
| 22 | SSH | OpenSSH 4.7p1 Debian 8ubuntu1 (protocol 2.0) | CVE-2008-5161 | 4.3 (Medium/Low) | No (detection-only finding, no PoC exploit code) | **Low** |
| 23 | Telnet | Linux telnetd | — (no applicable CVE) | — | — | **Medium (structural — cleartext protocol, no specific CVE)** |
| 25 | SMTP | Postfix (Ubuntu) — version string not exposed in banner | — (re-verification pending exact version) | — | — | **Informational** |
| 53 | DNS | ISC BIND 9.4.2 (confirmed via `dig version.bind`) | **CVE-2008-1447** | High (the "Kaminsky bug") | Yes — EDB-ID 6130 (kaminsky-attack.c), Metasploit `auxiliary/spoof/dns/bailiwicked_domain` | **High** |
| 3306 | MySQL | 5.0.51a-3ubuntu5 (confirmed via netcat banner grab) | — (no single matching CVE; finding is config-based) | — | — | **Critical (misconfiguration: root account has no password set)** |

---

## 3. Detailed Findings

### Port 21 — FTP — vsftpd 2.3.4 — CVE-2011-2523 ✅ Verified

**Description:** A malicious backdoor was inserted into the vsftpd 2.3.4 source archive between June 30 and July 3, 2011. Any username ending in a smiley face (`:)`) triggers the backdoor, opening a root shell on TCP port 6200.

**Why this is critical:** No authentication is required to trigger it, no user interaction beyond sending the crafted username is needed, and successful exploitation yields a root shell — complete loss of confidentiality, integrity, and availability.

**Exploit availability:** Confirmed on exploit-db.com (EDB-ID 49757, Python PoC) and built into Metasploit as `exploit/unix/ftp/vsftpd_234_backdoor`.

**Detection:** `nmap --script ftp-vsftpd-backdoor -p 21 <target>` will flag this directly.

---

### Port 22 — SSH — OpenSSH 4.7p1 — CVE-2008-5161 ✅ Verified, severity corrected

**Description:** OpenSSH (and several SSH Tectia products), when using a block cipher in CBC mode, allow a remote attacker to recover small amounts of plaintext data from an arbitrary block of ciphertext within an SSH session.

**Correction from initial draft:** This was originally logged as "Important" severity. The actual CVSS base score is **4.3 (Medium-Low)**. This is an information-disclosure weakness affecting CBC-mode ciphers specifically — not a remote code execution or authentication-bypass vulnerability. The practical attack is also difficult to execute and yields only limited plaintext recovery (a low probability per attempt), which is why later OpenSSH releases mitigated it without a full architectural fix being strictly required.

**Exploit availability:** No proof-of-concept exploit on exploit-db.com — this is a scanner/Nessus-style detection finding rather than something with working exploit code. Mitigation is to prefer CTR or GCM cipher modes over CBC.

**Risk Level:** Low — worth noting in a report for completeness/hardening recommendations, but not an urgent finding.

---

### Port 23 — Telnet — Linux telnetd — CVE removed pending correction ⚠️

**Original draft error:** The initial table cited CVE-2026-28372. This CVE is real, but it applies to **GNU inetutils telnetd through version 2.7**, exploited via systemd service credential handling introduced in util-linux 2.40 — released in 2026. Metasploitable2 is a 2010-era image with no systemd and an ancient util-linux version; this CVE's prerequisites do not exist on the target. **This CVE has been removed from the findings table as a mismatch.**

**What the actual finding is:** Telnet itself is the vulnerability here, independent of any specific CVE. Telnet transmits all data — including login credentials — in cleartext. Anyone capturing traffic on the network segment (confirmed achievable with Wireshark, per your earlier captures) can recover credentials directly from the packet stream with no cracking required.

**Recommendation for the report:** List this as a **configuration/protocol-level finding** rather than a CVE-based one: "Telnet service exposed; cleartext credential transmission confirmed via packet capture." This is actually how real reports often present legacy-protocol findings — not every risk maps to a CVE number.

---

### Port 25 — SMTP — Postfix smtpd — CVE pending re-verification ⚠️

**Original draft error:** CVE-2004-0925 was cited, but this CVE specifically concerns **Postfix on Mac OS X 10.3.x–10.3.5** with SMTPD AUTH enabled — an authentication-username-collision DoS bug unrelated to Metasploitable2's Debian/Linux Postfix installation. **This CVE has been removed pending correct identification.**

**Next step:** The exact Postfix version string running on Metasploitable2 needs to be captured (via `nmap -sV -p 25` banner grab, or `nc 192.168.56.101 25`) before a correctly matched CVE can be cited. Common, well-known SMTP findings on this box include **VRFY/EXPN command enabled for username enumeration** — worth checking with `nmap --script smtp-enum-users`.

---

### Port 53 — DNS — ISC BIND 9.4.2 — CVE-2008-1447 ✅ Verified

**Version confirmed via:** `dig @192.168.56.101 version.bind chaos txt` — returned `9.4.2` directly from the server's own diagnostic response.

**Description:** Known as the "Kaminsky bug" — a fundamental weakness in the DNS protocol's use of a 16-bit Query ID for matching responses to queries, combined with predictable source ports, allows an attacker to spoof DNS responses via a birthday attack and poison the resolver's cache. Affects BIND 8 and 9 before versions 9.5.0-P1, 9.4.2-P1, and 9.3.5-P1 — the target's plain **9.4.2** (no `-P1` patch suffix) falls directly within the vulnerable range.

**Severity:** Rated High severity and remotely exploitable by ISC.

**Exploit availability:** Confirmed on exploit-db.com (EDB-ID 6130, `kaminsky-attack.c`) and implemented as a Metasploit auxiliary module (`auxiliary/spoof/dns/bailiwicked_domain`).

**Impact:** Successful cache poisoning can redirect victims to attacker-controlled servers for any domain the poisoned resolver serves — enabling traffic interception, credential theft via fake login pages, or malware distribution under a trusted domain name.

---

### Port 3306 — MySQL — 5.0.51a-3ubuntu5 — Misconfiguration, not a CVE ✅ Verified

**Version confirmed via:** Manual netcat banner grab (`nc 192.168.56.101 3306`) — returned `5.0.51a-3ubuntu5` directly in the initial handshake.

**Why no single CVE is cited:** This exact build string doesn't map to one specific named CVE in available vulnerability databases. More importantly, the actual, well-documented risk on Metasploitable2 isn't a software bug at all — **the MySQL root account has no password configured**, allowing any network client to authenticate as root with zero credentials and gain full database access (and, depending on configuration, read local files via `LOAD DATA LOCAL INFILE`).

**Risk Level:** Critical, despite the absence of a CVE number — this is a textbook example of why enumeration findings shouldn't be limited to "does a CVE exist." A misconfiguration can be more severe than many CVEs and must be reported on its own merits.

---

## 4. Process Notes for Future Enumeration

1. **Always confirm the exact version string** via a banner grab or `nmap -sV` before searching for CVEs — version ranges in CVE descriptions are precise and a near-miss version is not a match.
2. **Read the full CVE description**, not just the CVE number paired with software name from a secondary source — vendor, OS, and version constraints are often narrower than they first appear (as seen with the SMTP and Telnet entries above).
3. **Cross-check CVSS score against severity label** — vendor labels like "Important" (Red Hat) or "High" (vendor-assigned) don't always align with the actual NVD CVSS base score; cite the CVSS number directly.
4. **Check exploit-db.com separately from the CVE lookup** — a CVE existing doesn't guarantee public exploit code exists; this distinction matters for realistic risk prioritization in a report.

---

## 5. Outstanding Items

- [x] Confirm BIND 9.4.2 version and CVE — **resolved**: `dig version.bind` confirmed 9.4.2, correct CVE is CVE-2008-1447
- [x] Confirm MySQL version via banner grab — **resolved**: 5.0.51a-3ubuntu5 confirmed via netcat; root account with no password is the actual finding
- [ ] Confirm exact Postfix version (banner does not expose it — try `EHLO` response or local package inspection) to identify a matching SMTP CVE
- [ ] Run `nmap --script smtp-enum-users` against port 25
- [ ] Run `nmap --script ftp-vsftpd-backdoor -p 21` to formally confirm Finding #1 via tool output
- [ ] Run `nmap --script dns-cache-snoop` or attempt the Kaminsky PoC in a controlled way to formally validate CVE-2008-1447 against this target (optional — version match alone is sufficient evidence for the report)
