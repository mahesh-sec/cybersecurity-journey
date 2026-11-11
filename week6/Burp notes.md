# Week 6: Burp Suite Notes

## Day 1: Target scope, site map, passive capture

### Target scope
- Tells Burp which hosts and URLs I am testing.
- Lets me filter the site map and HTTP history to in-scope items only, and avoid touching hosts I don't have permission to test.
- Community Edition: scope settings are lost when Burp closes, so re-add the target each session.

### Setup used
- Target app: DVWA (local), `http://127.0.0.1:42001`
- Scope prefix added: `http://127.0.0.1:42001`
- Intercept: off (passive capture through Burp's browser)
- DVWA security level: started on `impossible` (default), changed to `low` for the vulnerability modules

### Cookie observations
| Cookie | HttpOnly | Secure | SameSite | Path | Expiry |
|---|---|---|---|---|---|
| PHPSESSID | confirm in Burp | no | Strict | / | observed about 1 day after creation (confirm which cookie) |
| security | no | no | (check) | / | (check) |

- PHPSESSID without `Secure` can travel over plain HTTP, so it could be sniffed on the network. Expected on local HTTP DVWA, a real finding on a live site.
- `SameSite=Strict` stops the browser sending the cookie on cross-site requests, which helps against CSRF.
- `security` cookie has no `HttpOnly`, so JavaScript can read it. Low impact (it only stores the difficulty level) but a flag gap.

### Login observations
- Credentials are sent in plain text in the POST body because the site runs over HTTP (bad: readable on the wire).
- Server issues a new session ID after login. This is session regeneration, which defends against session fixation (good).
- Login form includes a hidden anti-CSRF token, `user_token`. Needs handling when testing the login page with Burp tools later.
- Weaknesses to explore later: default credentials, no brute-force protection at low security.

### Cache headers (seen on responses)
- `Cache-Control: no-store, no-cache, must-revalidate`, `Pragma: no-cache`, `Expires: Thu, 19 Nov 1981 08:52:00 GMT`
- Meaning: responses should not be stored, and any stored copy must be revalidated. Correct setting for sensitive pages.
- Cookie `Expires` (how long the browser keeps the cookie) is separate from response cache headers (how long a page may be reused).

### Server header
- `Server: nginx/1.28.2` is sent on responses. Version disclosure is a minor information leak that helps an attacker look for known vulnerabilities.

### Flagged requests to test further
1. **Login POST**: credentials over HTTP, `user_token` to handle.
2. **First GET**: sets PHPSESSID and `security` cookies.
3. **SQLi probe**: `GET /vulnerabilities/sqli/?id=%27&Submit=Submit`
   - Sent a single quote (`'`) as the `id` parameter with `security=low`.
   - Result: `500 Internal Server Error` with an empty body (`Content-Length: 0`).
   - Reading: the input likely reached the SQL query and broke its syntax, which is a sign the parameter may be injectable. The server showed no error message, so this is a hint to follow up on, not proof.
   - Next step: compare against a normal `id=1` request, then test with Repeater.

### HTTP history review (DVWA session)
| Request | Method | Cookies sent | Worth testing further? |
|---|---|---|---|
| `/login.php` (login) | POST | PHPSESSID, security | Yes (credentials, token) |
| `/vulnerabilities/sqli/?id=%27&Submit=Submit` | GET | PHPSESSID, security=low | Yes (500 on single quote) |
| (add more rows) | | | |

### Reference
- Set the target scope: https://portswigger.net/burp/documentation/desktop/getting-started/setting-target-scope
- Site map: https://portswigger.net/burp/documentation/desktop/tools/target/site-map




## Day 2: Repeater, first pass

**Request used:** DVWA login request (POST /login.php)

**Baseline (valid):** admin / password -> 302 Found, Location: index.php, new PHPSESSID issued. This confirms a real successful login.

**Invalid attempts (all identical outcome):**

- admin / wrongpassword
- wronguser / password
- admin / ' or '1'='1 (payload in password field)
- ' or '1'='1 / ' or '1'='1 (payload in both fields)

All four returned 302 Found, Location: login.php, with no authenticated session created.

**Conclusion:** The login form requires an exact valid username AND password match. A basic `' or '1'='1` payload does not bypass authentication here, suggesting the login query is not trivially injectable at Low security -- unlike DVWA's dedicated SQL Injection module (a separate page), which is built to be vulnerable. Worth testing that page tomorrow for a true SQLi bypass.

**Note on method:** DVWA issues a new PHPSESSID on every page load, regardless of login outcome -- a new session ID alone is **not** proof of success. The reliable signal is the `Location` header: `index.php` = success, `login.php` = failure. Also had to grab a fresh `user_token` and `PHPSESSID` for every attempt, since DVWA's CSRF token is tied to the session and a stale one causes every request to fail identically, which can be mistaken for a credential-testing result.
