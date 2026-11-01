# Week 5, Day 5 — Broken Authentication, Session Management & IDOR

**Date:** November 1, 2026
**Tools used:** Burp Suite Community (Kali), DVWA, browser dev tools

## 1. Authentication Labs (PortSwigger)

### Lab 1: Username Enumeration via Different Responses
- **Goal:** find a valid username/password pair by exploiting a login form that responds differently depending on whether the username exists.
- **Method:**
  1. Captured a failed `POST /login` request in Burp Proxy > HTTP history.
  2. Sent the request to Intruder, marked the username field as the payload position, and loaded the candidate username wordlist from the lab.
  3. Ran the attack and sorted results by response length — the outlier response revealed the valid username.
  4. Repeated the same process on the password field using the valid username, this time looking for a different status code (302 vs 200) to identify the correct password.
  5. Logged in with the discovered credentials to solve the lab.
- **Root cause:** the application returned subtly different error messages/response lengths for "invalid username" vs "invalid password," letting an attacker enumerate valid accounts.
- **Fix:** return identical, generic error messages (e.g. "Invalid username or password") regardless of which field was wrong, and apply rate limiting / account lockout to slow brute-force attempts.

### Lab 2: 2FA Simple Bypass
- **Goal:** bypass two-factor authentication without the victim's code.
- **Method:**
  1. Logged in as the victim using the credentials provided by the lab, reaching the 2FA code prompt.
  2. Without entering a code, navigated directly to `/my-account`.
  3. The server did not verify that the 2FA step had been completed, granting full access to the victim's account.
- **Root cause:** the server trusted the client to reach the 2FA page honestly instead of enforcing step completion on the backend.
- **Fix:** enforce 2FA state server-side on every request to a protected page (e.g. a session flag that is only set after successful code verification), not just via the UI flow.

## 2. Access Control / IDOR Labs (PortSwigger)

### Lab: User ID Controlled by Request Parameter
- **Goal:** access another user's data by modifying an ID in the request.
- **Method:** changed the `id` (or equivalent) parameter in the request to another user's value and confirmed the server returned that user's data without an ownership check.
- **Root cause:** the server trusted a client-supplied ID instead of checking that the logged-in user actually owns that resource.
- **Fix:** always verify server-side that the requested resource belongs to the authenticated user before returning it; avoid exposing sequential/predictable IDs where possible.

### Lab: Insecure Direct Object References (static files)
- **Goal:** access another user's data via a predictable static file reference (e.g. saved chat transcripts).
- **Method:** identified the predictable file naming pattern and requested another user's file directly.
- **Root cause:** files were stored with guessable names/paths and no access check was performed when serving them.
- **Fix:** use unpredictable, non-enumerable identifiers for stored resources, and enforce authorization checks before serving any file.

## 3. Session Cookie Analysis — DVWA

Inspected the `PHPSESSID` cookie via browser dev tools (Application > Cookies) after logging into DVWA:

| Flag | Value | Meaning |
|------|-------|---------|
| HttpOnly | `true` | JavaScript cannot read the cookie — protects against theft via XSS. |
| Secure | `false` | Cookie is sent over both HTTP and HTTPS — a weakness, since it could be intercepted on plain HTTP. |
| HostOnly | `true` | Cookie is scoped to the exact host only (no `Domain` attribute set), not shared with subdomains. |
| SameSite | `Strict` | Cookie is never sent on cross-site requests (even top-level link clicks), giving strong CSRF protection. |

**Summary:** DVWA's session cookie is well protected against XSS-based theft (`HttpOnly`) and CSRF (`SameSite: Strict`), but the missing `Secure` flag means it would still be transmitted over an unencrypted connection if one were ever used — a gap that matters in production even though it's expected in this local/HTTP test setup.

## 4. Key Takeaways

- Authentication flaws (enumeration, weak 2FA enforcement) and access control flaws (IDOR) both stem from the same root issue: **trusting client input or client-side flow instead of verifying authorization server-side.**
- Cookie flags are a quick, high-value check: `HttpOnly`, `Secure`, and `SameSite` each defend against a different attack (XSS theft, network interception, CSRF respectively).
- Burp Intruder is effective even in Community Edition for short wordlists; Repeater is sufficient for manually testing flow-bypass issues like the 2FA lab.

## 5. Real-World Reference

*(Add after completing the 18:30 evening block: a short write-up found on an IDOR or broken-authentication bug bounty report, with one paragraph on root cause and fix.)*
