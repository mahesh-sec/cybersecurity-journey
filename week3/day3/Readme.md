# Week 3 — Day 3: Users, Groups + Authentication Files

## Focus
Linux user/group management, authentication file internals (`/etc/passwd`, `/etc/shadow`, `/etc/group`), sudoers configuration, and a hands-on sudo misconfiguration privilege escalation using GTFOBins.

## What was covered

- **Theory:** `/etc/passwd` and `/etc/shadow` structure, `/etc/group`, UID 0 = root, `sudo` vs `su`, the sudoers file and `visudo`
- **Lab:** Created two test users (`testuser1`, `testuser2`), assigned `testuser1` to the `sudo` group, granted `testuser2` a narrow scoped sudo rule via `/etc/sudoers.d/`, and compared file access as root vs. as a normal user
- **Practice:** Used `sudo -l` to enumerate `testuser2`'s allowed commands, then escalated to root using a GTFOBins technique against `find`
- **Deep Dive:** OverTheWire Bandit Levels 8–10 (text filtering, encoding)
- **Tools:** Process and session inspection — `whoami`, `id`, `w`, `last`, `ps aux`, `ps -ef --forest`

## Sub-documents

- [`users-and-auth.md`](./users-and-auth.md) — `/etc/passwd`, `/etc/shadow`, `/etc/group` structure, sudoers basics
- [`sudo-privesc-find.md`](./sudo-privesc-find.md) — full sudo misconfiguration → root walkthrough
- [`bandit-8-10.md`](./bandit-8-10.md) — Bandit Level 8–10 write-ups

## Key takeaway

Login-tracking tools (`w`, `last`) and live process tools (`ps`) are all point-in-time snapshots — none of them recorded the `su` session switch or the `find`/`sh` processes from the privilege escalation once those processes exited. This is exactly why persistent logging (e.g. `/var/log/auth.log`) matters for real detection, which ties directly into Day 5 (Logging, Cron + Process Monitoring).
