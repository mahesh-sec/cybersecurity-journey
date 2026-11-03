# SSRF Labs + Security Misconfiguration Findings

## SSRF — PortSwigger labs (2 of 7, Apprentice)
### Lab 1: Basic SSRF against the local server
- **Vulnerable feature:** stock-check feature that fetches a URL supplied by the client
- **Payload:** `stockApi=http://localhost/admin/delete?username=carlos`
- **Result:** deleted the user `carlos` via the internal admin interface, which trusts requests coming from localhost
- **Why it works:** the server makes the request on the attacker's behalf, and the admin panel only checks the *source* of the request (localhost), not who is really asking.

### Lab 2: Basic SSRF against another back-end system
- **Vulnerable feature:** same stock-check feature, but the back-end is a private, non-routable system (e.g. `192.168.0.x`) rather than localhost
- **Payload:** `stockApi=http://192.168.0.X:8080/admin` (discover the live internal host/port, e.g. by trying a small IP/port range)
- **Result:** reached an internal admin interface not directly exposed to the internet
- **Why it works:** internal back-end systems are reachable from the app server even though they're invisible to normal users, and they're often protected by network location rather than real authentication.

**Remaining SSRF labs (not yet done):** SSRF with blacklist-based filter, SSRF with whitelist-based filter, SSRF with filter bypass via open redirection, blind SSRF with out-of-band detection. Worth a look in a later week if SSRF comes up again.

## Fix for SSRF
Allow-list destinations (not block-list), block requests to internal/loopback/link-local ranges, don't return the raw back-end response to the client, require authentication on internal services too (don't rely on network location as the only control).

## Security misconfiguration findings
| Finding | Where seen | Risk | Fix |
|---|---|---|---|
| TODO (e.g. verbose error / stack trace) | TODO | Information disclosure | Disable debug output in production |
| DVWA login over plain HTTP | DVWA login page | Credentials sniffable by anyone on the network path | Enforce TLS/HTTPS, HSTS |
| TODO (e.g. default credentials `admin/password`) | TODO | Easy account takeover | Change defaults |
| TODO (e.g. missing security headers) | TODO | TODO | TODO |
