# Linux Permissions Cheatsheet

## Permission Basics

Each file and directory has three permission sets:
- **Owner (u)** — the user who owns the file
- **Group (g)** — the group assigned to the file
- **Others (o)** — everyone else

Each set has three bits:

| Symbol | Octal | Meaning on File | Meaning on Directory |
|--------|-------|-----------------|----------------------|
| r | 4 | Read contents | List contents (ls) |
| w | 2 | Modify contents | Create/delete/rename files inside |
| x | 1 | Execute as program | Enter directory (cd) |

---

## Octal Notation

Permissions are represented as three digits — owner / group / others.

```
chmod 644 file
      ^^^
      |||__ others: 4 = r--
      ||___ group:  4 = r--
      |____ owner:  6 = rw-  (4+2)
```

### Common values
| Octal | Binary | Symbol | Meaning |
|-------|--------|--------|---------|
| 7 | 111 | rwx | read + write + execute |
| 6 | 110 | rw- | read + write |
| 5 | 101 | r-x | read + execute |
| 4 | 100 | r-- | read only |
| 0 | 000 | --- | no permissions |

### Baselines
- **Files: 644** — owner can read/write, group and others can only read
- **Directories: 755** — owner can read/write/enter, group and others can read/enter but not write

---

## Symbolic Notation

Symbolic mode uses operators instead of numbers:

| Operator | Meaning |
|----------|---------|
| `=` | Set exact permissions |
| `+` | Add permission without changing others |
| `-` | Remove permission without changing others |

```bash
chmod u=rw,g=rx,o=rx file    # set exact permissions
chmod u+x file                # add execute for owner only
chmod g-w file                # remove write from group
chmod o= file                 # remove all permissions from others
chmod a+x file                # add execute for all (owner, group, others)
```

---

## chmod and chown

```bash
# Change permissions
chmod 755 file
chmod u+x file

# Change owner
sudo chown root file
sudo chown mahesh:mahesh file   # change owner and group

# Change group only
sudo chgrp shadow file

# Recursive (apply to directory and all contents)
sudo chmod -R 755 /var/www
```

---

## umask

umask defines default permissions subtracted from new files/directories.

```bash
umask          # view current umask (typically 0022)
umask 0000     # set umask (everything allowed)
```

Default umask 0022:
- New files: 666 - 022 = **644**
- New directories: 777 - 022 = **755**

---

## Key Rules

1. **Deletion** needs `w` on the **parent directory**, not the file itself
2. **chmod** requires **ownership**, not write permission
3. **x on a directory** means traverse/enter — without it you can't `cd` in even with `r`
4. **w without x on a directory** is useless — you can't access the directory at all
5. **Root bypasses all permission checks** — UID 0 ignores rwx entirely

---

## Special Permission Bits

### SUID (Set User ID) — octal 4000

When set on an executable, it runs as the **file's owner** instead of the user who launched it.

```bash
ls -la /usr/bin/passwd
-rwsr-xr-x 1 root root ...
#   ^-- 's' in owner execute position = SUID set
```

- `passwd` is owned by root and has SUID → it runs as root so it can write to `/etc/shadow`
- Find all SUID binaries: `find / -perm -4000 2>/dev/null`

**Pentesting relevance:** Misconfigured SUID binaries are a primary Linux privilege escalation vector.

---

### SGID (Set Group ID) — octal 2000

Same as SUID but for group identity.

- On a **file** → runs as the file's group
- On a **directory** → new files created inside inherit the directory's group

```bash
ls -la /usr/bin/wall
-rwxr-sr-x 1 root tty ...
#      ^-- 's' in group execute position = SGID set
```

- Find all SGID binaries: `find / -perm -2000 2>/dev/null`

---

### Sticky Bit — octal 1000

Set on directories. Prevents users from deleting each other's files even if they have `w` on the directory.

```bash
ls -la /
drwxrwxrwt ... tmp
#         ^-- 't' at end = sticky bit set
```

- `/tmp` uses sticky bit — everyone can create files but only the owner (or root) can delete their own files
- Set it: `chmod +t /tmp` or `chmod 1777 /tmp`

---

## Special Bits Summary

| Bit | Octal | On Files | On Directories |
|-----|-------|----------|----------------|
| SUID | 4000 | Runs as file owner | Rarely used |
| SGID | 2000 | Runs as file group | New files inherit group |
| Sticky | 1000 | No effect | Only owner can delete their files |

---

## Useful Commands

```bash
ls -la                          # list with permissions
stat filename                   # full permission + metadata view
find / -perm -4000 2>/dev/null  # find all SUID binaries
find / -perm -2000 2>/dev/null  # find all SGID binaries
```
