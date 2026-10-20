# DVWA SQL Injection: Security Levels (Day 1)

| Level | What the app does | Protection | Does it work? |
|-------|-------------------|------------|---------------|
| Low | Input concatenated straight into the query | None | No, fully injectable |
| Medium | Dropdown + quote escaping | Client-side restriction | No, request can be tampered with |
| High | Separate input window, LIMIT 1 | Output hiding | No, still injectable |
| Impossible | Prepared statements + numeric check + CSRF token | Parameterized queries | Yes |

**Key takeaway:** UI restrictions and output hiding don't fix injection. Parameterized queries do, because the query structure and user input are kept separate.

## Lab notes
- Low: `1` returns one user, `1' OR '1'='1` returns all users.
- Medium: dropdown can be bypassed by editing the request (Burp, Day 2+).
- High / Impossible: read source to see why results are limited and why the fix works.
