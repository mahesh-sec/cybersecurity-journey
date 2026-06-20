# Week 2 — Day 4: Service Enumeration (FTP, SMB, Netcat, CVE Mapping)

**Target:** 192.168.56.101 (Metasploitable2)
**Focus:** Anonymous/unauthenticated access enumeration, manual banner grabbing, and verified CVE mapping across multiple services

## Summary

Today's work covered enumeration of multiple services on Metasploitable2 — FTP, SMB, and a netcat-based manual banner-grab sweep — followed by a full CVE verification pass to build an accurate findings table.

| Service | Port | Version (confirmed) | Key finding |
|---|---|---|---|
| FTP | 21 | vsftpd 2.3.4 | Anonymous login allowed; backdoor CVE-2011-2523 (Critical) |
| SSH | 22 | OpenSSH 4.7p1 | CVE-2008-5161, low-severity info disclosure |
| Telnet | 23 | Linux telnetd | Cleartext protocol risk — no applicable CVE |
| SMTP | 25 | Postfix (Ubuntu) | Version not exposed in banner — open item |
| SMB | 139/445 | Samba 3.0.20-Debian | Anonymous read/write on `tmp`; 2 users enumerated; CVE-2007-2447 |
| DNS | 53 | BIND 9.4.2 | CVE-2008-1447 — the Kaminsky cache-poisoning bug (High) |
| MySQL | 3306 | 5.0.51a-3ubuntu5 | Root account has no password — Critical misconfiguration |

Full detail in:
- [`ftp-anonymous-enumeration.md`](./ftp-anonymous-enumeration.md)
- [`smb-enumeration.md`](./smb-enumeration.md)
- [`netcat-basics.md`](./netcat-basics.md)
- [`service-cve-findings.md`](./service-cve-findings.md)
- [`concepts-reference.md`](./concepts-reference.md)

## Key takeaway

A draft CVE table built without direct verification contained two wrong CVE matches (Telnet, SMTP) and one mis-stated severity (SSH). Every entry was re-checked against primary sources (NVD, ISC's own vulnerability matrix, exploit-db) before being finalized. Manual netcat banner grabs also surfaced two version strings (MySQL, BIND) that closed out previously open items in the findings table — BIND's version was confirmed precisely using a `dig version.bind` CHAOS-class query, leading to the correct CVE-2008-1447 citation.

## Concepts reinforced this session

- The difference between a share list (what's exposed) and a host's actual filesystem (what exists)
- Service accounts vs. human accounts on Linux, and the principle of least privilege
- "Account disabled" refers to interactive login only — it has no bearing on whether the underlying service is running
- Netcat as a raw TCP tool — manual protocol interaction without a client wrapper, and why it's called "the Swiss army knife of networking"
- Why some services (FTP, SSH, SMTP) send a banner immediately, while others (HTTP, DNS) wait for a properly formed request first
- **CVE verification discipline:** always confirm exact version/vendor match against the CVE's stated affected range before citing it; a misconfiguration (e.g., MySQL with no root password) can be a valid, severe finding even without an associated CVE number
- Port binding is exclusive — only one process can hold a given port at a time, demonstrated directly via an "Address already in use" conflict between `sshd` and netcat
