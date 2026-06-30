# Week 3 — Day 2: File Permissions + Ownership Model

## Topics Covered
- rwx permission model for files and directories
- Octal and symbolic permission notation
- chmod, chown, umask
- SUID, SGID, and sticky bit
- SUID binary hunting on Metasploitable2
- OverTheWire Bandit Levels 4–7

## Files
- [permissions-cheatsheet.md](./permissions-cheatsheet.md) — full reference for rwx, octal, symbolic, special bits
- [suid-findings.md](./suid-findings.md) — SUID binary findings on Metasploitable2 with GTFOBins notes
- [bandit-solutions.md](./bandit-solutions.md) — Bandit Level 4–7 solutions and reasoning

## Key Takeaways
- Write permission on a file controls contents, not deletion — deletion needs `w` on the parent directory
- Ownership (not write permission) controls who can `chmod` a file
- SUID binaries run as the file's owner — if owned by root, attacker gets root execution context
- `nmap --interactive` + `!sh` on Metasploitable2 escalates to root via SUID abuse
- Root bypasses all permission checks — getting root = game over in pentesting
