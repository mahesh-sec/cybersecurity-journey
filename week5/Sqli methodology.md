# SQL Injection Methodology — Week 5, Day 3

## 1. Retrieving Hidden Data (Apprentice)
**Lab:** SQL injection vulnerability in WHERE clause allowing retrieval of hidden data

**Diagnosis:** Injected a single `'` into the `category` parameter to check whether
the input was passed into the query unsanitized. The app's altered response
confirmed the injection point.

**Construction:** Since the query was of the form
`... WHERE category = 'Gifts' AND released = 1`, I used:
```
' or '1'='1
```
This makes the `WHERE` clause evaluate to true for every row, so hidden
(unreleased) products are returned alongside the Gifts category.

---

## 2. Login Bypass (Apprentice)
**Lab:** SQL injection vulnerability allowing login bypass

**Diagnosis:** Entered a `'` in the username field. The app returned an
internal server error, confirming the input wasn't sanitized and was
breaking the underlying SQL syntax.

**Construction:** Reasoned that the query likely looked like:
```sql
SELECT * FROM users WHERE username = '<input>' AND password = '<input>'
```
Used:
```
administrator'--
```
in the username field. The `'` closes the string early, and `--` comments
out the rest of the query (including the password check), so the query
effectively becomes a lookup for the `administrator` row with no password
required.

---

## 3. UNION Attack — Retrieving Database Version (Practitioner)
**Lab:** SQL injection UNION attack, querying the database type and version (Oracle)

**Diagnosis:**
1. Determined the number of columns using `ORDER BY`, incrementing until
   an error was thrown:
   ```
   ' ORDER BY 1--
   ' ORDER BY 2--
   ' ORDER BY 3--   → error
   ```
   Confirmed the query returns 2 columns.
2. Checked which column(s) accept string data:
   ```
   ' UNION SELECT 'a','a' FROM dual--
   ```
   No error returned, confirming both columns accept strings.

**Construction:** Built the final payload to retrieve the Oracle version
banner, using `v$version` (Oracle requires a `FROM` clause on every `SELECT`):
```
' UNION SELECT banner, NULL FROM v$version--
```
The `banner` column holds the version string; `NULL` pads the second
column to match the required count.

---

## Key takeaway
All three labs follow the same pattern: **diagnose the injection point and
query shape first** (via error behavior, `ORDER BY`, or type probing),
**then construct the payload deliberately** rather than guessing. This
matters more in the UNION lab, where mismatched column count or type
throws an error before you even get to see useful data.
