# Week 4 Day 4 — Theory Notes

## Log parsing fundamentals

### auth.log / journalctl structure
Modern Kali uses journald instead of a flat /var/log/auth.log. Access SSH logs via:
    journalctl -u ssh --since "1 month ago" -o short-iso --no-pager

Log line anatomy:
    2026-07-23T06:49:06-04:00 kali sshd-session[146196]: Failed password for invalid user shiva from 127.0.0.1 port 44440 ssh2
    <timestamp>               <host> <process>[<pid>]:   <message>

Two message shapes:
- `Failed password for invalid user <name> from <ip> port <port> ssh2` — nonexistent user
- `Failed password for <name> from <ip> port <port> ssh2` — real user, wrong password
- `Accepted password for <name> from <ip> port <port> ssh2` — success

### Python `re` module
- `re.search()` — find first match in a string; returns Match object or None
- `re.findall()` — find all matches
- Capturing groups `(...)` vs non-capturing `(?:...)` — non-capturing groups
  bundle a pattern without assigning it a group number, keeping group indices
  stable across optional branches
- `?` after a group makes the whole group optional (zero or one occurrence)
- `\w+` (word chars incl. digits) vs `[a-z]+` (letters only) — usernames can
  contain digits, so `\w+` is safer

### Brute-force vs credential stuffing
- Brute-force: many failed attempts, same username, short time window
- Credential stuffing: many usernames tried, few attempts each, from one IP

### Python truthiness
`if x:` checks truthy/falsy, not literal equality to True. Falsy values:
None, False, 0, "", [], {}, (). A regex Match object is always truthy;
None (no match) is falsy — this is why `if log:` correctly skips non-matching lines.
