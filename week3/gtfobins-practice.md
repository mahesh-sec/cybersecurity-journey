# Practice Block — SUID Binary Triage Against GTFOBins

**Target:** Metasploitable2 (`192.168.56.101`)
**User context:** `msfadmin`

## 1. Full SUID candidate list

```bash
find / -perm -4000 2>/dev/null
```

```
/bin/umount
/bin/fusermount
/bin/su
/bin/mount
/bin/ping
/bin/ping6
/sbin/mount.nfs
/lib/dhcp3-client/call-dhclient-script
/usr/bin/sudoedit
/usr/bin/X
/usr/bin/netkit-rsh
/usr/bin/gpasswd
/usr/bin/traceroute6.iputils
/usr/bin/sudo
/usr/bin/netkit-rlogin
/usr/bin/arping
/usr/bin/at
/usr/bin/newgrp
/usr/bin/chfn
/usr/bin/nmap
/usr/bin/chsh
/usr/bin/netkit-rcp
/usr/bin/passwd
/usr/bin/mtr
/usr/sbin/uuidd
/usr/sbin/pppd
/usr/lib/telnetlogin
/usr/lib/apache2/suexec
/usr/lib/eject/dmcrypt-get-device
/usr/lib/openssh/ssh-keysign
/usr/lib/pt_chown
```

## 2. Triage: expected/benign vs. worth testing

**Expected/benign — SUID by design, not exploitable without an additional misconfiguration:**
`su`, `passwd`, `chsh`, `chfn`, `newgrp`, `gpasswd`, `sudo`, `sudoedit`, `mount`, `umount`, `ping`, `ping6`, `fusermount`, `mount.nfs`, `dhcp3-client` script, `traceroute6`, `arping`, `mtr`, `uuidd`, `netkit-rsh`/`rlogin`/`rcp` (legacy trusted-host tools), `apache2/suexec` (narrow designed purpose), `dmcrypt-get-device`, `ssh-keysign`, `pt_chown`, `telnetlogin`.

**Candidates tested this block:** `su`, `at`, `nmap` (cross-reference)
**Candidate flagged, out of scope:** `pppd`
**Candidate not tested (stretch goal, deferred):** `X`

## 3. `su` — analysis (not an exploit)

```bash
find / -perm -4000 2>/dev/null | grep su$
```

GTFOBins lists `su -c /bin/sh` as a technique, but this is **not a vulnerability on its own**. `su` is SUID root by design — that's the only mechanism by which an unprivileged user can ever authenticate to become root through it. Using it successfully still requires the target account's password (or already being root).

**Conclusion:** `su` appearing in the SUID list is expected, not a finding. It would only be a genuine escalation vector if it were separately reachable via a `sudo -l` entry with `NOPASSWD` restricted to `su`, bypassing normal authentication. Not applicable here since `msfadmin` already has unrestricted `sudo ALL`.

## 4. `at` — GTFOBins attempt (negative result)

**Hypothesis:** SUID on `/usr/bin/at` allows queuing a job that spawns a root shell.

**Attempt 1 — direct shell spawn:**
```bash
echo "/bin/sh -p" | at now -M
```
Job queued successfully but ran detached with no attached terminal; process had exited by the time it was checked (`ps aux | grep "sh -p"` returned no match).

**Attempt 2 — output redirected to file for proof:**
```bash
echo "id > /tmp/at_proof 2>&1; whoami >> /tmp/at_proof" | at now
sleep 65
cat /tmp/at_proof
```

**Result:**
```
uid=1000(msfadmin) gid=1000(msfadmin) groups=4(adm),20(dialout),24(cdrom),25(floppy),29(audio),30(dip),44(video),46(plugdev),107(fuse),111(lpadmin),112(admin),119(sambashare),1000(msfadmin)
msfadmin
```

**Conclusion: Not exploitable.** The job executed as `msfadmin` (real UID), not root.

**Root cause:** The SUID bit on `/usr/bin/at` exists so an unprivileged user can write into `/var/spool/cron/atjobs/` (normally root-only writable) to *queue* a job — not to execute it with elevated privileges. Execution is handled by a separate daemon, `atd`, which runs as root but independently tracks per-job ownership and deliberately drops its own privileges down to the job's real owner before running it. The elevated context used to queue the job does not carry through to execution.

**Contrast with `nmap --interactive` (Week 3 finding, re-confirmed below):** no intermediary daemon is involved — the SUID `nmap` process itself spawns the shell directly, so the shell inherits the process's effective UID (root) with no re-check in between. This is the mechanism-level reason one SUID binary escalates and the other doesn't.

## 5. `nmap` — cross-reference (Week 3)

```bash
nmap --interactive
!sh
id
```

Confirmed root shell via `nmap --interactive` (full exploit already documented in `week3/day2/`). Re-listed here only because it reappeared in this Day 6 SUID survey.

## 6. `pppd` — flagged, out of scope

`pppd` requires a known CVE (buffer overflow in the version shipped with Metasploitable2), not GTFOBins-style built-in-functionality abuse. This is a binary exploitation technique, not a SUID/GTFOBins technique — deferred to a later phase of the roadmap.

## 7. `X` — deferred

Not attempted this block. GTFOBins lists a file-read technique (`-fp` option abuse) for SUID `X`, but it is more version-dependent and involved than the other candidates. Marked as a stretch goal for a future session.

## Key lesson

SUID doesn't guarantee escalation on its own. Whether the elevated effective UID actually reaches a usable shell depends on whether execution happens **directly** within the SUID process (`nmap`) or is handed off to a **separate privilege-aware daemon** that re-checks ownership (`at`/`atd`).
