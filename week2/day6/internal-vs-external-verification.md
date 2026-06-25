# Internal vs. External Verification — Metasploitable2

**Date:** Week 2, Day 6
**Target:** Metasploitable2 (`192.168.56.101`)
**Method:** SSH into the target and compare `ps aux` / `netstat -tulnp` against the morning's external Nmap scan

---

## 1. Objective

Confirm that services Nmap identified externally (by guessed name) match real running processes when viewed from inside the box, and identify anything visible internally that an external port scan alone didn't fully surface.

---

## 2. `/etc/passwd` — Reading User Accounts

Format: `username:password-placeholder:UID:GID:comment:home_directory:shell`

| Field | Example (`msfadmin`) | Meaning |
|---|---|---|
| Username | `msfadmin` | Login name |
| Password | `x` | Placeholder — real hash lives in `/etc/shadow` |
| UID | `1000` | Numeric user ID |
| GID | `1000` | Primary group ID |
| Comment | `msfadmin,,,` | Free-text (often blank) |
| Home dir | `/home/msfadmin` | Login destination |
| Shell | `/bin/bash` | Login program — the field that determines if interactive login is even possible |

**Reading patterns used:**
- **Shell field:** `/bin/bash` or `/bin/sh` = real interactive login possible. `/bin/false` or `/usr/sbin/nologin` = login blocked even with a valid password — these are service accounts that exist only so a daemon can run as a non-root user.
- **UID ranges:** UID 0 = root always. UID < 1000 = system/service accounts (auto-created by installed packages). UID 1000+ = human-created accounts.

**Result:** 32 accounts total. Three real interactive human accounts: `msfadmin` (1000), `user` (1001), `service` (1002). Everything else is a system/service account, matched to the services already identified externally (e.g. `sshd`, `mysql`, `postgres`, `bind`, `www-data`, `proftpd`, `telnetd`, `distccd`).

---

## 3. `ps aux` vs `netstat -tulnp` — The Core Distinction

| | `ps aux` | `netstat -tulnp` |
|---|---|---|
| Shows | Every running process, system-wide | Only processes with a socket in the LISTEN state |
| Includes non-networked processes (`cron`, `fluxbox`, `xterm`) | Yes | No |
| Tells you which port a process owns | No (not directly) | Yes — PID/program column |

**Flags:**
- `ps aux` — `a` = all users' processes, `u` = user-oriented output format, `x` = include processes with no controlling terminal
- `netstat -tulnp` — `t`/`u` = TCP/UDP, `l` = listening sockets only, `n` = numeric addresses (skip DNS lookups), `p` = show owning process/PID (requires `sudo`)

**One-sentence summary:** `ps aux` shows everything running regardless of network use; `netstat -tulnp` shows only the subset of processes with an open listening socket, because of the `-l` flag specifically — dropping `-l` would also surface active/established connections, not just listeners.

---

## 4. Matching External Scan Results to Internal Processes

| Port (external) | Confirmed binary (internal) |
|---|---|
| 21 ftp | `proftpd` (separate from the `vsftpd` instance also present, fronted via `xinetd` on the standard port) |
| 22 ssh | `/usr/sbin/sshd` |
| 23 telnet | No standing process — spawned on demand by `xinetd` |
| 25 smtp | `/usr/lib/postfix/master` |
| 53 domain | `/usr/sbin/named -u bind` |
| 80 http | `/usr/sbin/apache2 -k start` |
| 139/445 smb | `/usr/sbin/nmbd -D` / `/usr/sbin/smbd -D` |
| 3306 mysql | `/usr/sbin/mysqld` |
| 5432 postgresql | `/usr/lib/postgresql/8.3/bin/postgres` |
| 5900 vnc | `Xtightvnc :0 ... -rfbport 5900` |
| 6667 irc | `/usr/bin/unrealircd` |
| 8009/8180 tomcat | `jsvc -user tomcat55 ...` |
| 1099 rmiregistry | `/usr/bin/rmiregistry` |

**Privilege observation:** `smbd`, `nmbd`, `named`, and `sshd`'s privileged listener all run as **root**. Web/database services (`apache2` worker processes, `mysqld`, `postgres`) run under their own dedicated low-privilege accounts. Any compromise of the root-run services gets root immediately, with no privilege escalation step needed.

---

## 5. Findings Visible Internally That Weren't Obvious From the External Scan Alone

- **`distccd` on port 3632** — running with `--allow 0.0.0.0/0` (no IP restriction at all). Confirmed listening via `netstat` (`tcp6 :::3632 LISTEN 4529/distccd`).
- **A Ruby DRb timeserver (`druby_timeserver.rb`) on port 8787** — running as **root**, bound to `0.0.0.0` (externally reachable, not just local).
- **NFS / portmapper / `rpc.mountd` / `rpc.statd`** — fully exposed (`2049`, `111`, plus dynamically assigned RPC ports).
- **Two separate FTP services** — `vsftpd` on the standard port 21 (via `xinetd`) and an independent `proftpd` instance on port 2121.
- **BIND's `rndc` control channel (port 953)** — correctly bound to `127.0.0.1` only, the one clearly hardened detail found; almost everything else binds to `0.0.0.0`.

---

## 6. Summary

External Nmap scanning identified open ports and guessed service names. Internal `ps aux`/`netstat -tulnp` inspection confirmed the exact binary and PID behind every one of them, and additionally surfaced several services that either fell outside the original scan's port range or were only fully understandable with privilege/process-owner context that an external scan can't provide — most notably an unrestricted `distccd` listener and a root-owned, externally-reachable Ruby DRb service.

---

## 7. Key Commands Reference

| Command | Purpose |
|---|---|
| `ssh msfadmin@<IP>` | Remote login to the target for internal inspection |
| `cat /etc/passwd` | Lists all system/user accounts and their login capability |
| `ps aux` | Lists all running processes system-wide |
| `sudo netstat -tulnp` | Lists listening sockets with owning process name/PID |
| `nmap -p <port> <IP>` | Targeted re-scan to confirm a specific port's external visibility |
