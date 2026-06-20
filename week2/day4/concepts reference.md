# Concepts Reference — Enumeration, Service Accounts, Netcat

**Date:** Week 2, Day 4
**Purpose:** Plain-language reference notes on core concepts clarified during today's enumeration work. Captured separately from the technical findings files since these are reusable concepts, not target-specific results.

---

## 1. What is enumeration?

Enumeration is **information-gathering about a target** — discovering what exists (shares, users, services, versions, configuration) without yet judging whether any of it is exploitable.

It is distinct from **vulnerability analysis**, which is the separate, later step of asking "is what I found dangerous?"

| Step | Question asked | Example tools |
|---|---|---|
| Enumeration | "What's here?" | `smbclient -L`, `nc`, `nmap --script *-enum-*` |
| Vulnerability analysis | "Is what's here dangerous?" | `nmap --script *-vuln-*`, manual CVE lookup |

**Port/host-level enumeration** (e.g., a full `nmap` port scan) answers "what services exist and on which ports?" — this is the broadest, usually first, enumeration step.

**Service-level enumeration** (e.g., `smbclient`, `nc <IP> 21`, `nmap --script ftp-anon`) goes deeper into one specific service once you already know it's running.

Both levels are still pure fact-finding — neither makes a judgment call about risk on its own.

---

## 2. Share lists vs. the actual filesystem

A share list (e.g., from `smbclient -L`) shows only what a service has been **deliberately configured to expose** over the network — not the target's full filesystem.

```
Actual filesystem (everything that exists):
/etc, /home, /root, /var, /usr, /bin ... and /tmp, /opt

What SMB chooses to expose (the share list):
tmp, opt, print$, IPC$, ADMIN$
```

Administrators control this via the Samba config file (`/etc/samba/smb.conf`), which sets, per share: the share name, the real path it maps to, whether it's browseable (visible in the list), whether guest/anonymous access is allowed, and whether it's read-only or read/write.

---

## 3. Service accounts vs. human accounts

On Linux, every service typically runs under its own dedicated system account — this is the **principle of least privilege**.

- **Service accounts** (e.g., `mysql`, `postgres`, `www-data`, `ftp`) are not tied to one person. Every connection to that service goes through the same shared account at the OS level — nobody "logs in as mysql" individually; the service just runs in the background under that identity.
- **Human accounts** (e.g., `msfadmin`, `user` on Metasploitable2) are for actual interactive login by a person.

Services often layer their **own internal user/permission system** on top of this — e.g., MySQL has its own internal user table, separate from the Linux account (`mysql`) that owns the running process. The Linux account owns the process; the internal user system governs what that connection is allowed to do once inside the service.

### "Account disabled" — a common point of confusion

**"Account disabled" only means the account cannot be used for interactive login** (e.g., via SSH). It does **not** mean the associated service is stopped.

```
mysql account disabled  →  MySQL still runs fine on port 3306
ftp account disabled    →  FTP still runs fine on port 21
```

Service accounts are disabled for login *by design* — disabling login has no bearing on whether the service process itself is running and reachable on its port. The only reliable way to check if a service is actually stopped is to check the port directly (`nmap -p <port> <IP>`) or query the service manager on the host itself (`service <name> status` / `systemctl status <name>`).

### Why this sandboxing matters for security

If a service account is compromised (e.g., via SQL injection against MySQL), the attacker initially only has the privileges of that one account — not the whole system:

```
mysql user CAN access:        mysql user CANNOT access:
├── /var/lib/mysql ✓          ├── /home/msfadmin ✗
├── /etc/mysql ✓              ├── /etc/ssh ✗
└── mysql databases ✓         └── other users' files ✗
```

A SOC analyst seeing a service account doing anything outside its normal job (e.g., `mysql` reading `/etc/passwd`, or making outbound connections) should treat that as a strong indicator of compromise — the account itself becomes the detection signal.

---

## 4. Netcat as a raw protocol tool

Tools like `ftp` and `ssh` are effectively netcat plus a protocol-aware translator built on top, automating what the protocol expects. Netcat strips that translation away, letting you see and send raw bytes directly over a TCP/UDP connection.

This is why netcat is nicknamed **"the Swiss army knife of networking"** — the same tool, with different flags, performs port scanning, banner grabbing, file transfer, raw protocol interaction, and listener/reverse-shell setup. See `netcat-basics.md` for the full hands-on breakdown.

---

## 5. CVE verification discipline

Citing a CVE number without confirming it actually matches the target's exact vendor, product, and version range is a credibility failure in a real report. Today's exercise caught two outright mismatched CVEs (Telnet, SMTP) and one overstated severity (SSH) in an initial draft table — all corrected only by reading the full CVE description and cross-checking against the exact version string confirmed on the target. See `service-cve-findings.md` for the full corrected table and methodology notes.

A misconfiguration (e.g., MySQL's root account having no password) can be a valid, severe finding even with **no CVE number attached at all** — not every risk maps to a CVE.
