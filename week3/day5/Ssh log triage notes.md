# SSH Log Triage — Annotated Capture

## Objective
Simulate a failed then successful SSH login against own Kali VM and identify the corresponding entries via `journalctl -u ssh`, understanding each field's meaning for later blue-team / brute-force detection work.

## Command
```bash
journalctl -u ssh --since "10 minutes ago"
```

## Captured Output (annotated)

```
Jul 10 06:23:16 kali systemd[1]: Starting ssh.service - OpenBSD Secure Shell server...
Jul 10 06:23:16 kali sshd[93722]: Server listening on 0.0.0.0 port 22.
Jul 10 06:23:16 kali sshd[93722]: Server listening on :: port 22.
Jul 10 06:23:16 kali systemd[1]: Started ssh.service - OpenBSD Secure Shell server.
```
→ systemd starting the SSH service.

```
Jul 10 06:23:34 kali unix_chkpwd[93886]: password check failed for user (kali)
```
→ `unix_chkpwd` is a privileged helper binary whose job is checking a submitted password against `/etc/shadow` (relevant to Day 3 — yescrypt `$y$` hashes). It runs separately since regular processes can't read `/etc/shadow` directly.

```
Jul 10 06:23:34 kali sshd-session[93790]: pam_unix(sshd:auth): authentication failure; logname= uid=0 euid=0 tty=ssh ruser= rhost=127.0.0.1  user=kali
```
→ PAM logging the failure at the authentication-framework layer, above `unix_chkpwd`.
**Key field: `rhost=127.0.0.1`** — the source IP of the login attempt. In a real investigation, this is the field to check for the attacker's origin.

```
Jul 10 06:23:36 kali sshd-session[93790]: Failed password for kali from 127.0.0.1 port 43086 ssh2
Jul 10 06:23:41 kali sshd-session[93790]: Failed password for kali from 127.0.0.1 port 43086 ssh2
```
→ Two deliberate wrong-password attempts. Same port (43086) on both lines confirms these are retries on the **same connection**, not separate connection attempts.
**This is the exact line to `grep` for brute-force hunting:**
```bash
grep "Failed password" /var/log/auth.log
journalctl -u ssh | grep "Failed password"
```

```
Jul 10 06:23:44 kali sshd-session[93790]: Accepted password for kali from 127.0.0.1 port 43086 ssh2
```
→ Successful login, same port — third attempt on the same connection succeeded.

```
Jul 10 06:23:44 kali sshd-session[93790]: pam_unix(sshd:session): session opened for user kali(uid=1000) by kali(uid=0)
```
→ Session creation. `for user kali(uid=1000)` is the target account. `by kali(uid=0)` indicates the session was opened **by a process running with root privileges** (the sshd daemon itself) — not a second privileged account named kali. This is normal: creating a login session (PTY setup, utmp updates) requires root-level operations under the hood even for a non-root user's login.

## Detection Takeaway
The signature pattern for a brute-force attack: multiple `Failed password` lines from the same (often unfamiliar) `rhost`, followed by an eventual `Accepted password`. Many fails → one success, especially from an unrecognized source IP, is the red flag to escalate on in real triage.

## Related: `last` command
For reviewing login history at a higher level (not full per-attempt detail like journalctl), the `last` command's third field specifies the **host of origin**:
- `127.0.0.1` → localhost
- an external IP → remote network login
- `:0` → local console/X11 login, not SSH
- blank → local login with no tracked origin

An unfamiliar external IP in this field on a system that shouldn't have external SSH access would warrant investigation.
