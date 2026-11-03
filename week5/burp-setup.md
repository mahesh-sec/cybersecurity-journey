# Burp Suite — Setup & First Hands-On

## 1. Setup
- Tool: Burp Suite Community Edition
- Browser proxy: 127.0.0.1:8080 (TODO: note whether you used Burp's built-in browser or FoxyProxy)
- Target: DVWA running locally (TODO: URL / how it's hosted, e.g. Docker or XAMPP)
- CA certificate: TODO — installed? (needed to intercept HTTPS)

## 2. First intercept — DVWA login (plain text credentials)
- Turned Intercept on in **Proxy**, submitted the DVWA login form.
- The request was a `POST /login.php` over **HTTP**; the username and password were visible in clear text in the request body.
- **Why it matters:** anyone on the same network path (public Wi-Fi, compromised router) could read these credentials.
- **Fix:** serve the login over HTTPS/TLS, add HSTS, set `Secure` and `HttpOnly` on session cookies.
- Screenshot: `screenshots/dvwa-login-intercept.png` (TODO: add)

## 3. Module overview
| Module | What it does | How I used it |
|---|---|---|
| **Proxy** | Sits between browser and server; lets me pause, inspect, edit and forward requests | Intercepted the DVWA login |
| **Repeater** | Resend a single request repeatedly with edits | Customised one HTTP request and compared responses |
| **Intruder** | Automates many requests with payload positions | Ran **Sniper** (one position, one wordlist) and **Cluster Bomb** (multiple positions, all combinations) |
| **Decoder** | Encode/decode data (URL, Base64, HTML, hex) | Decoded captured data |
| **Comparer** | Diffs two requests/responses | Compared two fields to spot the difference |

### Intruder attack types (quick reference)
- **Sniper:** one payload set, one position at a time. Good for fuzzing a single parameter.
- **Cluster Bomb:** one payload set per position, tries every combination. Good for username + password.
- (Battering Ram and Pitchfork exist too: same payload in all positions / payloads in parallel.)

## 4. Day 7 practice
### Repeater — tampered login
- Sent the intercepted login request to Repeater (Ctrl+R).
- Changed: TODO (e.g. password value, removed a parameter, long input)
- Response difference: TODO (status code, length, redirect location, error text)

### Intruder — sniper on the password field
- Position: `password=§...§`
- Wordlist: TODO (small custom list)
- Result: TODO — which payload stood out and how (response length / status)
- **Note:** DVWA's login form includes a `user_token` (anti-CSRF) that changes every request. A plain Intruder run can fail unless the token is handled (e.g. a Recursive grep payload), so state what you saw. The DVWA *Brute Force* page (a GET request, no token) is a simpler target.

## 5. Lessons learned
- TODO: 2–3 lines in your own words.
