# SQL Injection Findings

## DVWA
### Low
- **Input point:** TODO (User ID field)
- **Payload(s):** `TODO`
- **Result:** TODO (what the app returned)
- **Why it worked:** input concatenated directly into the SQL query.

### Medium
- **What changed vs Low:** TODO (e.g. dropdown / `mysqli_real_escape_string`, POST instead of GET)
- **Filter bypass logic:** TODO (how you got around it, e.g. tampering the request in Burp/Repeater)
- **Payload(s):** `TODO`

### High (if done)
- TODO

## PortSwigger labs — Apprentice (completed)
| # | Lab name | Technique | Typical payload | Notes |
|---|---|---|---|---|
| 1 | SQL injection vulnerability in WHERE clause allowing retrieval of hidden data | Comment out the rest of the query to make the WHERE clause always true | `' OR 1=1-- ` in the category filter | Returned every product, including hidden/unreleased ones |
| 2 | SQL injection vulnerability allowing login bypass | Comment out the password check | `administrator'-- ` in the username field | Logged in as administrator with no valid password |

**Note:** PortSwigger's SQLi Apprentice track only has these two labs — the other labs on the roadmap's "6 labs" target (UNION attacks, blind SQLi, error-based) are **Practitioner** level. If you only did the two above, you've completed Apprentice but not the full target; flag this in your README so it's an honest log, and pick up 2–4 Practitioner labs (e.g. "SQL injection UNION attack, determining the number of columns" and "Blind SQL injection with conditional responses") if you want to hit 6.

## Impact
Attacker can read, modify or delete database data, and sometimes bypass authentication entirely.

## Fix
Parameterized queries / prepared statements, least-privilege DB accounts, input validation, generic error messages.
