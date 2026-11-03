# Week 5 — Web Application Security + OWASP Top 10

**Goal:** Understand the 10 most critical web vulnerabilities and get hands-on with Burp Suite.
**Environment:** DVWA (local), PortSwigger Web Security Academy, Burp Suite Community.

## What I covered
| Topic | Write-up |
|---|---|
| OWASP Top 10 comparison table | [owasp-top10-notes.md](owasp-top10-notes.md) |
| SQL Injection (DVWA + PortSwigger labs) | [sqli-findings.md](sqli-findings.md) |
| Cross-Site Scripting (DVWA + PortSwigger labs) | [xss-writeup.md](xss-writeup.md) |
| Authentication, sessions & IDOR | [auth-idor-notes.md](auth-idor-notes.md) |
| Burp Suite setup + Proxy/Repeater/Intruder/Decoder/Comparer | [burp-setup.md](burp-setup.md) |
| SSRF + security misconfiguration | [ssrf-misconfig-notes.md](ssrf-misconfig-notes.md) |

## Key takeaways
1. Most web vulnerabilities come from **trusting user input** (injection, XSS, SSRF) or **trusting the client** (IDOR, broken access control).
2. Over plain HTTP, credentials travel in clear text. I confirmed this by intercepting the DVWA login in Burp. TLS is the baseline fix.
3. Burp's Repeater and Intruder turn "I think this is vulnerable" into evidence you can reproduce.
4. Every finding in this repo follows the same format: **what / how / evidence / impact / fix**.

## Tools used
Burp Suite Community, DVWA, PortSwigger Web Security Academy, browser dev tools.

## Next week
Week 6: Burp Suite mastery + MITRE ATT&CK + threat intel.

> All testing was done on intentionally vulnerable local/lab targets. No real systems were tested.
