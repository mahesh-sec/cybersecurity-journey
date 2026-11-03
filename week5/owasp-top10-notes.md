# OWASP Top 10 — Comparison Table

Edition used: OWASP Top 10:2021 (check owasp.org/Top10 in case a newer edition is current).
Fill the **Lab evidence** column with a lab you actually performed.

| # | Category | Root cause | Example attack | Primary defense | Lab evidence |
|---|---|---|---|---|---|
| A01 | Broken Access Control | Server doesn't enforce who may do what | Change `id=5` to `id=6` to read another user's data (IDOR) | Server-side authorization on every request, deny by default | TODO (auth/IDOR labs) |
| A02 | Cryptographic Failures | Weak/missing encryption of data in transit or at rest | Sniffing credentials sent over HTTP | TLS everywhere, strong hashing (bcrypt/argon2), no sensitive data in URLs | DVWA login seen in plain text via Burp |
| A03 | Injection | Untrusted input is interpreted as code/query | `' OR 1=1 --` in a login or search field (SQLi), `<script>` (XSS) | Parameterized queries, input validation, output encoding | TODO (SQLi + XSS labs) |
| A04 | Insecure Design | Missing security thinking at design time | No rate limit or lockout on login, enabling brute force | Threat modeling, secure design patterns, rate limiting | TODO (Intruder run on login) |
| A05 | Security Misconfiguration | Insecure defaults, verbose errors, open admin pages | Default credentials, directory listing, stack traces | Hardened baselines, remove defaults, disable debug in production | TODO (misconfig findings) |
| A06 | Vulnerable & Outdated Components | Using libraries/software with known CVEs | Exploiting a known CVE in an old framework | Inventory dependencies, patch, SCA tools | TODO (or "reviewed only") |
| A07 | Identification & Authentication Failures | Weak passwords, poor session handling, no MFA | Credential stuffing, session fixation | MFA, strong password policy, secure session management, lockout | TODO (auth/session labs, Intruder) |
| A08 | Software & Data Integrity Failures | Trusting unverified updates, plugins or serialized data | Insecure deserialization, tampered CI/CD pipeline | Signed artifacts, integrity checks, safe deserialization | TODO (or "reviewed only") |
| A09 | Security Logging & Monitoring Failures | Attacks go unnoticed | Brute force that never triggers an alert | Centralized logs, alerting, incident response plan | TODO (or "reviewed only") |
| A10 | Server-Side Request Forgery (SSRF) | Server fetches attacker-supplied URLs | Make the server request `http://localhost/admin` or a cloud metadata URL | Allow-list destinations, block internal ranges, network segmentation | TODO (SSRF lab) |

## Notes
- Rows marked "reviewed only" are fine if you didn't do a lab. Be honest about that, since interviewers ask.
- Pick 2–3 rows and be ready to explain them out loud (attack, why it works, fix).
