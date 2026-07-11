# Lab Block — Sudo Misconfiguration & Cron/SUID Write-Permission Audit

**Target:** Metasploitable2 (`192.168.56.101`)
**User context:** `msfadmin`

## 1. Sudo privilege check

```bash
sudo -l
```

**Result:** `(ALL : ALL) ALL` — `msfadmin` can run any command as any user, without a password prompt.

**Conclusion:** This is a direct, standalone privilege escalation path. `msfadmin` does not need to chain through cron or SUID artifacts to reach root — a single command is sufficient:

```bash
sudo su -
```

or

```bash
sudo bash -i
```

This is one of Metasploitable2's well-known intentional misconfigurations (passwordless sudo for the `msfadmin` account).

## 2. SUID/SGID binary survey

```bash
find / -perm -4000 2>/dev/null   # SUID
find / -perm -2000 2>/dev/null   # SGID
```

**Result:** Multiple SUID/SGID binaries found across `/usr/bin`, `/usr/sbin`, `/bin`, `/sbin`, `/usr/lib`.

**Permission check on discovered binaries:**

```bash
ls -la <binary>
```

None of the identified SUID/SGID binaries had world-write (`o+w`) permissions set.

**Conclusion:** A low-privilege user without sudo access cannot directly modify these binaries. They can only execute them as they already exist — meaning exploitation (for a non-sudo user) would have to come from a binary's *built-in* functionality (GTFOBins-style abuse), not from tampering with the file itself.

## 3. Cron write-permission audit

```bash
cat /etc/crontab
ls -la /etc/cron.d/
```

**Result:**
- `/etc/crontab` contains 4 time-based entries (hourly, daily, weekly, monthly)
- No entries or referenced scripts have world-write permissions
- `/etc/cron.d/` files also have no world-write permissions

**Conclusion:** Same logic as SUID — a non-sudo user cannot hijack cron-executed scripts to run arbitrary commands as root, since they lack write access to the crontab, the cron.d files, or the scripts those entries call.

## Corrected reasoning (see conversation notes)

Initial working theory considered using `msfadmin`'s sudo access to modify cron/SUID artifacts as a path to escalation. This was a misframing — `sudo ALL` **is** the escalation, not a prerequisite for a further escalation. Modifying cron jobs or SUID binaries as a sudo-privileged user is a lateral-movement/persistence technique (affecting other users), not a privilege-escalation technique for oneself.

The cron/SUID write-permission analysis is the correct exercise for a **different, unprivileged foothold scenario** (e.g., landing a shell as `www-data` via a web app exploit, with no sudo rights) — a scenario to revisit in a later block.

## Summary table

| Vector | Write-accessible to unprivileged user? | Exploitable without sudo? |
|---|---|---|
| Sudo (`ALL:ALL`) | N/A — direct grant | N/A — already root-equivalent |
| Cron (`/etc/crontab`, `/etc/cron.d/`) | No | No (for non-sudo user) |
| SUID/SGID binaries | No | Only via built-in binary functionality (GTFOBins), not file tampering |
