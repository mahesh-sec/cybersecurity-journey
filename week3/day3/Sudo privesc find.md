# Sudo Misconfiguration Privilege Escalation — `find` (GTFOBins)

## Scenario

Two test users were created to demonstrate the contrast between broad and narrow sudo access:

- **`testuser1`** — added to the `sudo` group (`usermod -aG sudo testuser1`), granting full, unrestricted sudo access.
- **`testuser2`** — granted a single, narrow sudo permission via `/etc/sudoers.d/testuser2`:

```
testuser2 ALL=(ALL) NOPASSWD: /usr/bin/find
```

On the surface, this looks safe — `testuser2` can only run `find`, nothing else. In practice, `find` is a documented sudo privilege escalation vector.

## Step 1 — Enumeration

As `testuser2`, the first move (and the real-world first move any attacker/pentester makes on landing a shell) is to check current sudo rights:

```bash
sudo -l
```

Confirmed output shows `/usr/bin/find` permitted with `NOPASSWD`.

**Verification of the restriction:**
```bash
$ sudo whoami
Sorry, user testuser2 is not allowed to execute '/usr/bin/whoami' as root on kali.

$ sudo find --version
find (GNU findutils) 4.10.0
```
`whoami` is correctly denied; `find` runs instantly with no password prompt, confirming the scoped `NOPASSWD` rule is active.

## Step 2 — GTFOBins lookup

[gtfobins.github.io](https://gtfobins.github.io) → search `find` → **Sudo** column gives the escalation payload:

```bash
sudo find . -exec /bin/sh \; -quit
```

## Step 3 — Command breakdown

| Part | Purpose |
|---|---|
| `sudo find` | runs `find` as root, per the sudoers rule |
| `.` | required starting path for `find` to search from — functionally irrelevant here, just needed for valid syntax |
| `-exec /bin/sh \;` | for the first matched item, execute `/bin/sh`. The `\;` (escaped semicolon) terminates the `-exec` clause so `find` knows where the command ends |
| `-quit` | stop `find` immediately after the first execution, instead of repeating for every match |

## Step 4 — Why it works (real UID vs. effective UID)

`sudo` doesn't make `testuser2` become root permanently — it spawns a **new process** (`find`) whose real UID is 0 for that execution only. Because `find`'s `-exec` flag spawns a **child process**, and child processes inherit the privilege level of their parent, the `/bin/sh` launched by `find` also runs with UID 0. That shell is a genuine root shell, not a simulated one.

```bash
sudo find . -exec /bin/sh \; -quit
whoami
# root
```

This is the same underlying pattern as the Day 2 nmap SUID exploit: a binary with elevated execution rights spawning a shell, and that shell inheriting the elevation.

## Takeaway

**Any binary with an `-exec`, "run a command," or similar arbitrary-execution feature is a sudo/SUID privilege escalation risk** if it appears in a `sudo -l` listing or has the SUID bit set — regardless of how narrow or "safe" the command grant appears at first glance. Scoped sudo access is not automatically safe access; the specific binary's capabilities matter.
