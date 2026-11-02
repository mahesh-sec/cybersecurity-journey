# SSRF Lab & Security Misconfiguration Notes

## SSRF Lab (PortSwigger)

**Lab:** Basic SSRF against the local server
**Target:** `0acc006d0413700c872cedeb00b00060.web-security-academy.net`

### Concept
Server-Side Request Forgery (SSRF) occurs when an attacker can make the
server issue HTTP requests to a destination of their choosing — including
internal-only endpoints the attacker couldn't reach directly (e.g. cloud
metadata endpoints, internal admin panels).

### Exploitation Steps
1. Intercepted the `POST /product/stock` request in Burp.
2. Found the `stockApi` parameter pointing to an internal URL:
   ```
   stockApi=http://192.168.0.1:8080/admin/delete?username=carlos
   ```
3. Sent the request to Intruder.
4. Set the attack type to **Sniper** (single payload position — Cluster
   bomb requires 2+ positions and isn't appropriate here).
5. Marked the last IP octet as the payload position:
   ```
   stockApi=http://192.168.0.§1§:8080/admin/delete?username=carlos
   ```
6. Payload type: Numbers, range 1–255, step 1 — swept the internal subnet
   to find which host responds on port 8080 with the admin interface.
7. Identified the responding host and confirmed the SSRF successfully
   reached an internal-only admin endpoint, deleting the `carlos` user
   as proof of impact.

### Root Cause
The application trusted a user-supplied URL for a server-side request
with no validation or allow-listing of destination hosts.

### Defense
- Allow-list permitted destination hosts/IPs for server-side requests.
- Disable unnecessary URL schemas and block requests to internal/
  loopback/link-local ranges.
- Avoid returning raw response data from the fetched URL to the client.

---

## Security Misconfiguration Sweep (DVWA / Metasploitable)

Checked the local DVWA/Metasploitable setup against the standard
misconfiguration checklist, using Burp's intercepted traffic plus a
manual walkthrough.

| Check | Finding |
|---|---|
| Default credentials | DVWA ships with `admin/password` by default — confirmed login succeeds with default creds. |
| Verbose error pages | Triggering invalid input (e.g. malformed SQL in the SQLi module) returned raw DB error output revealing query structure. |
| Exposed admin panels | DVWA's admin/config pages accessible without additional auth beyond the default login. |
| Unnecessary open ports | Ran a quick port check against the Metasploitable host; several services open beyond what's needed for the lab (ftp, telnet, unauthenticated services). |
| Security level setting | DVWA's security level was set to Low/Medium during testing — confirmed this directly affects how much misconfiguration-style exposure is present (expected, lab-intentional). |

### Root Cause
Default/insecure configuration left in place without hardening —
common in real-world deployments where defaults are never reviewed
post-install.

### Defense
- Change default credentials immediately on deployment.
- Disable verbose error/debug output in production.
- Restrict admin interfaces to internal networks or require strong auth.
- Regularly audit open ports/services and disable anything unused.
