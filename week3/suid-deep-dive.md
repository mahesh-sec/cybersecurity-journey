# Deep Dive Block — SUID Mechanics (Controlled Demo)

**Host:** Kali (`mpati`)
**Accounts:** `kali` (attacker/builder), `testuser1` (unprivileged test account)

## Purpose

The lab and practice blocks demonstrated SUID escalation outcomes on pre-existing Metasploitable2 binaries, but the underlying *conditions* for why SUID escalation succeeds or fails aren't fully controllable on a system you didn't build. This block isolates those conditions on a self-built test case where every variable (ownership, permissions, file content) is known.

**Hypothesis under test:** SUID escalation requires all three of the following simultaneously:
1. The file must be executable
2. There must be a privilege gap between file owner and executing user
3. The file must contain code that meaningfully uses the elevated effective UID

## 1. Initial setup

Created two empty test files as `testuser1`:

```bash
touch testfile1 testfile2
sudo chown root:root testfile1 testfile2
```

## 2. Finding #1 — capital `S` vs lowercase `s`

```bash
sudo chmod u+s testfile1 testfile2
ls -l
```

**Result:**
```
-rwSrw-r-- 1 root root 0 Jul 11 03:34 testfile1
-rwSrw-r-- 1 root root 0 Jul 11 03:34 testfile2
```

Capital `S` in the owner-execute position means: **SUID is set, but the owner-execute bit is missing.** The setuid bit only has an effect when combined with execute permission.

**Fix:**
```bash
sudo chmod -v u+x testfile1 testfile2
```
```
mode of 'testfile1' changed from 4644 (rw-r--r--) to 4744 (rwsr--r--)
mode of 'testfile2' changed from 4644 (rw-r--r--) to 4744 (rwsr--r--)
```

Lowercase `s` confirmed — SUID + execute now both correctly set.

**Note:** an earlier attempt using `sudo chmod u+s` repeatedly only toggled the SUID bit and never added execute, which is why the permission string appeared "stuck" on capital `S` across multiple retries — the command being run wasn't actually setting the execute bit at all.

## 3. Finding #2 — SUID bit alone is not enough; content matters

Even with permissions correct (`rwsr--r--`), both files were 0 bytes. Attempting to run one produced nothing meaningful — no executable content exists for the OS to run with the elevated effective UID.

**Conclusion:** correct permissions are necessary but not sufficient. The file needs actual code that does something as the elevated user.

## 4. Building a real SUID demo binary

Note: SUID is ignored on shell scripts by the Linux kernel as a built-in security protection, so a `#!/bin/bash` script would not demonstrate real escalation. A compiled binary is required.

**Source (`/tmp/testfile1.c`):**
```c
#include <unistd.h>
int main() {
    setuid(0);
    system("/bin/sh -p");
    return 0;
}
```

- `setuid(0)` — explicitly sets effective UID to 0 (root). Technically redundant once SUID root is set on the compiled binary (the kernel applies it automatically on execution), but included for an unambiguous, GTFOBins-style PoC.
- `system("/bin/sh -p")` — spawns a shell. The `-p` flag keeps the shell in privileged mode, preventing it from silently dropping back to the real UID when real and effective UID differ (a safety behavior in bash that would otherwise make a working exploit look like a failed one).

**Build and configure:**
```bash
gcc /tmp/testfile1.c -o testfile1
sudo chown root:root testfile1
sudo chmod u+sx testfile1
ls -la testfile1
```

Compiling resets permissions to a default (no SUID), so `chown`/`chmod` must be reapplied after every rebuild.

**Expected result:** `-rwsr-xr-x 1 root root ... testfile1`

## 5. Execution as unprivileged user

```bash
sudo passwd testuser1     # if not already set
su - testuser1
./testfile1
id
```

**Expected result inside the spawned shell:** `uid=0(root) ...` — confirming the process executed with root's effective UID despite being launched by `testuser1`.

## 6. Core mechanism confirmed

Running a file with execute + SUID set does **not** change who you are — `testuser1`'s real UID, home directory, and login session remain unchanged. What changes is the **effective UID** of the specific process spawned by that execution: it temporarily runs with the file owner's (root's) privileges for permission-checking purposes.

This real-UID vs. effective-UID distinction is the same mechanism behind every SUID finding across this Day 6 session:
- `nmap --interactive` — effective UID (root) carries directly into the spawned shell → escalation succeeds
- `at` — `atd` re-checks and drops the effective UID back to the job's real owner before execution → escalation fails
- `su` — requires authentication to switch identity; SUID here only allows the *mechanism* of switching, not a bypass of the password check

## Summary

| Condition | Present in initial test files? | Present after fix? |
|---|---|---|
| Executable | No (capital `S`, no `+x`) | Yes |
| Privilege gap (owner ≠ executor) | Yes (root vs. testuser1) | Yes |
| Meaningful content using elevated UID | No (0 bytes) | Yes (compiled C binary) |
