# Users, Groups & Authentication Files

## `/etc/passwd`

World-readable file listing every account on the system. One line per user:

```
username:x:UID:GID:comment:home:shell
```

| Field | Meaning |
|---|---|
| `username` | login name |
| `x` | placeholder — the real password hash lives in `/etc/shadow`, not here |
| `UID` | user ID number (0 = root) |
| `GID` | primary group ID |
| `comment` | GECOS field — free-text info (full name, etc.) |
| `home` | home directory path |
| `shell` | login shell (`/bin/bash`, `/bin/zsh`, or `/usr/sbin/nologin`/`/bin/false` for service accounts that shouldn't log in interactively) |

**Why the `x` placeholder exists:** decades ago, password hashes were stored directly in `/etc/passwd`. Since that file has to be world-readable (many tools need to resolve UID → username), storing hashes there meant every user on the system could copy them offline and crack them. `/etc/shadow` was introduced specifically to move hashes into a file only root can read.

## `/etc/shadow`

Root-only file (`-rw-r-----`, owned by `root:shadow`) holding the actual password data:

```
username:hash:lastchange:min:max:warn:inactive:expire:
```

- **Hash field format:** `$id$salt$hash`
  - `$1$` = MD5 (legacy, weak)
  - `$5$` = SHA-256
  - `$6$` = SHA-512 (common textbook default)
  - `$y$` = yescrypt — the current default on modern Debian/Kali. Deliberately slow and memory-hard, which makes GPU-based brute-force cracking significantly harder than SHA-512.
- **Aging fields:** last password change, minimum days between changes, maximum days before expiry, warning period, inactivity period, account expiration date.
- Service/system accounts (e.g. `daemon`, `sshd`, `mysql`) show `!` or `!*` in the hash field — this means password-based login is disabled entirely for that account, by design.

## `/etc/group`

Same pattern as `/etc/passwd`, but for groups:

```
groupname:x:GID:member-list
```

Shows secondary/supplementary group membership — i.e. which groups a user belongs to *beyond* their primary GID. This is how group-based privilege grants (like adding a user to `sudo`) actually show up on disk.

## UID 0 = root

Linux privilege checks are based on the **UID number**, not the username. Any account with UID 0 has full root privileges regardless of what it's named. This is why a classic privilege escalation technique is inserting a second `UID 0` entry into a writable `/etc/passwd` — the system will treat that account as root.

## `sudo` vs `su`

| | `su` | `sudo` |
|---|---|---|
| Switches to | another user's full shell | runs a single command as another user |
| Requires | **target user's** password | **your own** password (by default) |
| Governed by | target account's password | policy defined in `/etc/sudoers` |

This distinction matters for enumeration: `sudo -l` reveals what a user can run as root **without ever knowing root's password** — access is policy-based, not password-based.

## The sudoers file

`/etc/sudoers` defines who can run what, as whom. It should never be edited directly with a plain text editor — always use:

```bash
sudo visudo
```

`visudo` opens the file in your default editor but validates syntax before saving, preventing a typo from corrupting the file and potentially breaking `sudo` system-wide.

Individual, scoped permission grants are better placed in **`/etc/sudoers.d/`** as separate files rather than crammed into the main file:

```bash
sudo visudo -f /etc/sudoers.d/<name>
```

**Rule syntax breakdown:**
```
user  host = (runas_user)  command
```

Example:
```
testuser2 ALL=(ALL) NOPASSWD: /usr/bin/find
```

- `testuser2` — the user the rule applies to
- `ALL` (host field) — which machines this rule applies on (relevant in multi-server environments where one sudoers config is shared; effectively meaningless on a single VM but always required by syntax)
- `(ALL)` (runas_user field) — which user(s) this account may run the command *as*. This is what caps the "ceiling" of any exploit built on the rule — `(ALL)` includes root; `(www-data)` would not.
- `NOPASSWD:` — no password prompt required for this specific command
- `/usr/bin/find` — the only command this rule authorizes

**Why `/etc/sudoers.d/` over editing the main file:**
1. **Isolation** — each grant lives in its own file, easy to audit or remove
2. **Safety** — a bad edit in one file doesn't risk corrupting the sudoers config for everyone
3. **Real-world practice** — configuration management tools (Ansible, Puppet, etc.) drop scoped sudoers snippets into `sudoers.d/` for exactly this reason
