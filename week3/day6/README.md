# Week 3 — Day 6: Linux Privilege Escalation (SUID, Sudo, Cron)

## Overview

Day 6 focused on identifying and validating Linux privilege escalation vectors on Metasploitable2, using sudo misconfiguration analysis, SUID/SGID binary triage against GTFOBins, and a controlled deep-dive into SUID mechanics on a Kali host with a dedicated low-privilege test account (`testuser1`).

Three blocks, documented separately:

- [`sudo-misconfiguration.md`](./sudo-misconfiguration.md) — Lab block: sudo `ALL` escalation, cron/SUID write-permission audit
- [`gtfobins-practice.md`](./gtfobins-practice.md) — Practice block: SUID binary triage, `at` exploit attempt (negative result), `su` analysis, nmap cross-reference
- [`suid-deep-dive.md`](./suid-deep-dive.md) — Deep dive: hands-on SUID mechanics using a compiled C binary on `testuser1`

## Key takeaways

1. **Sudo `ALL` is a direct root grant, not a stepping stone.** On Metasploitable2, `msfadmin` has passwordless `sudo ALL`, which is itself the privilege escalation — no need to chain through cron or SUID artifacts.
2. **Write access is the precondition for cron/SUID abuse by a non-privileged user.** Without write permission to a script, cron entry, or SUID binary, execution alone doesn't grant control over what the privileged process does.
3. **SUID escalation is conditional on three factors simultaneously:** the file must be executable, there must be a privilege gap between file owner and executing user, and the file must contain code that meaningfully uses the elevated effective UID (e.g., spawning a shell).
4. **Not all SUID binaries are exploitable.** `su`, `passwd`, `mount`, etc. are SUID by design and require a password or a separate misconfiguration layered on top to be useful for escalation.
5. **Whether SUID privilege "survives" to your shell depends on the execution chain.** `nmap --interactive` spawns a shell directly from the SUID process, so root's effective UID carries through. `at` queues a job to a separate daemon (`atd`) that independently re-checks and drops privileges to the job's real owner before executing — so the SUID bit on `/usr/bin/at` does not translate into root execution.
6. **Real UID vs. effective UID** is the underlying mechanism: executing a SUID binary doesn't change who you are (real UID), but temporarily grants the file owner's privileges to that process for permission-checking purposes (effective UID) — unless something in the chain (e.g., a shell without `-p`) deliberately drops back to the real UID.

## Lab environment

- Kali host: `mpati` (attacker)
- Metasploitable2 target: `192.168.56.101`
- Networking: VirtualBox Host-Only
