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

# Day 3 — Burp Repeater Mastery

## What it is and when I use it
Repeater lets me resend a single HTTP request as many times as I want,
editing it each time and reading the response. I use it to test input
fields for vulnerabilities (SQLi, XSS) and to test multi-step processes
like password change or verification flows, where I can replay or modify
one step at a time to see whether the server validates properly.

## Workflow
- Proxy first: capture the traffic, then send the interesting request
  to Repeater (Ctrl+R).
- Tab groups: keep separate tests in separate tabs so they don't
  interfere with each other.
- Diff view: compare two responses to see exactly what changed after I
  modified an input.
- Repeater vs Proxy vs Intruder:
  - Proxy captures and intercepts live traffic.
  - Repeater tests one request manually, one change at a time.
  - Intruder automates many requests by substituting payloads into
    marked positions in a request.

## Tab setup (DVWA, security=low unless noted)
| Tab | Purpose | What I changed |
|-----|---------|-----------------|
| 1 | SQLi baseline | `id=1` |
| 2 | SQLi boolean bypass | `id=' or '1'='1` |
| 3 | SQLi column count | `id=1' ORDER BY 2/3-- -` |
| 4 | SQLi UNION extraction | `id=1' UNION select user,password from users-- -` |
| 5 | CSRF password change — baseline | matching `password_new`/`password_conf` |
| 6 | CSRF — mismatch / missing field | `password_conf` changed/removed |
| 7 | CSRF — Referer tests (medium) | Referer removed, then forged |

## SQL Injection

### Boolean bypass
- Payload: `id=' or '1'='1` with `&Submit=Submit` as a separate parameter
- Baseline (`id=1`): 1 row returned
- Payload: 5 rows returned (every user in the table)
- Takeaway: confirmed classic SQLi boolean bypass — WHERE clause became
  always-true.
- Mistake found: URL-encoding the `&` between `id` and `Submit` (as `%26`)
  swallows `Submit` into the `id` value, so the parameter never reaches
  the server and the query never runs. Only encode characters inside a
  parameter's value, never the separator between parameters.

### Column count
- `id=1' ORDER BY 2-- -` → 200 OK (still valid)
- `id=1' ORDER BY 3-- -` → 500 Internal Server Error
- Conclusion: query selects 2 columns

### UNION extraction
- Payload: `id=1' UNION select user,password from users-- -`
- Extracted:
  - admin   : `5f4dcc3b5aa765d61d8327deb882cf99`
  - gordonb : `e99a18c428cb38d5f260853678922e03`
  - 1337    : `8d3533d75ae2c3966d7e0d4fcc69216b`
  - pablo   : `0d107d09f5bbe40cade3de5c71e9e9b7`
  - smithy  : `5f4dcc3b5aa765d61d8327deb882cf99`
- Finding: `admin` and `smithy` share an identical hash, meaning they
  share the same password — visible without cracking anything, since
  these are unsalted MD5 hashes. Unsalted hashing leaks password reuse.

## CSRF / password-change testing

### Low security
- Mismatched `password_new`/`password_conf` → "password did not match"
- Missing `password_conf` → same "did not match" (empty string compared
  against the new password, same code path as a mismatch)
- Lesson: test one variable at a time — my first Referer test was
  invalid because I still had mismatched passwords in that request, so
  it failed on validation before Referer was ever checked.

### Medium security — Referer check finding
- No Referer header, passwords matching → 200 OK, "Password Changed"
- Forged Referer (`http://evil-attacker.com/`), passwords matching →
  200 OK, "Password Changed"
- Finding: medium's Referer check did not block either case on this
  DVWA build. The commonly cited description (medium rejects a Referer
  that doesn't contain the host) did not hold here — Referer-based CSRF
  protection is not actually effective on this install.

### High security (token) — in progress
- Testing: capture `user_token` from a fresh page load, use it once,
  reload the page to regenerate the token, then replay the old request
  with the stale token.
- Expected: stale-token replay rejected ("CSRF token is incorrect").

## Most useful diff
- Compared: SQLi baseline (`id=1`, 1 row) vs boolean bypass (`id=' or
  '1'='1`, 5 rows)
- Difference: payload returned every row in the users table instead of
  one row
- Takeaway: clearest before/after evidence of the injection actually
  working, and it's what led into the column-count and UNION steps.

## What tripped me up
- Encoding the `&` parameter separator by mistake makes a parameter
  silently disappear, with no error — hard to debug without comparing
  to a working request.
- Repeater requests don't update the browser's cookies or session
  state — a `Set-Cookie` from a Repeater response only reaches Repeater,
  not the browser. State changes need to go through the Cookie header
  directly, or the original intercepted request needs to be forwarded.
- DVWA's CSRF token isn't single-use — it stays valid in the session
  until the token-issuing page is reloaded with a GET, not consumed on
  a successful POST. A captured request can be replayed as long as the
  token hasn't been regenerated by a fresh page load.
- Isolate one variable per test — mixing in a mismatched password while
  testing the Referer header made the Referer result meaningless.

  ## Burp Intruder: Attack Types (Week 6, Day 4)

Intruder automates sending many modified versions of one request. You mark **payload positions** in the request, choose an **attack type**, and load one or more **payload sets**. The attack type decides how payloads are placed into positions.

### Sniper
- **How it works:** One payload set. It fuzzes one position at a time while the other positions keep their original values, then moves to the next position.
- **When to use it:** Fuzzing a single parameter or several parameters independently, e.g. testing one field for injection or anomalous responses.
- **Request count (2 positions, 3 payloads):** 6 (payloads x positions)

### Battering Ram
- **How it works:** One payload set. The same payload is placed into all positions at the same time.
- **When to use it:** When one value has to appear in several places at once, e.g. a username sent in both a body field and a header or cookie.
- **Request count (2 positions, 3 payloads):** 3

### Pitchfork
- **How it works:** One payload set per position. The nth payload from each set is used together, in parallel. It stops when the shortest list runs out.
- **When to use it:** Testing known pairs that belong together, e.g. username:password pairs from a leaked credential list.
- **Request count (2 positions, 3 payloads each):** 3

### Cluster Bomb
- **How it works:** One payload set per position. It tries every combination across all sets.
- **When to use it:** Guessing when you don't know which values pair up, e.g. brute-forcing a login with a username list and a password list. The request count grows fast (product of the list sizes).
- **Request count (2 positions, 3 payloads each):** 9

### Quick comparison

| Attack type   | Payload sets | Positions filled        | Requests (2 pos, 3 payloads) |
|---------------|--------------|-------------------------|------------------------------|
| Sniper        | 1            | One at a time           | 6                            |
| Battering Ram | 1            | All, same payload       | 3                            |
| Pitchfork     | 1 per position | All, paired by index  | 3                            |
| Cluster Bomb  | 1 per position | All, every combination | 9                           |

---

## Lab: Sniper Fuzz on DVWA (Low security)

**Target:** DVWA SQL Injection page, `id` parameter
**Setup:** Request intercepted in Burp Proxy and sent to Intruder; only the `id` value marked as a position; attack type set to Sniper.
**Payload list:** numeric IDs 0-99, plus `"`, `'`, `or '1'='1'`, `'or'1'='1`

### Observations

| Payload | Status | Length | What changed in the response |
|---------|--------|--------|-------------------------------|
| 0-99 (valid/invalid IDs) | 200 | 4556 (baseline) | Normal page template; no error shown even for nonexistent user IDs |
| 89 | 200 | 0 | Empty response body - this ID doesn't exist in the DB, but the app gives no "user not found" message, just a blank/empty page |
| `"` (double quote) | 200 | short | Treated as a literal character, not SQL syntax - confirms the query uses single quotes to wrap the value, not double |
| `'` (single quote) | 500 | - | Breaks the SQL string literal -> unhandled DB syntax error. First strong signal of SQL injection: input is concatenated directly into the query |
| `or '1'='1'` (no leading quote) | 500 | - | Still breaks syntax - without a quote to close the string first, `or` sitting inside the expected quoted value causes a parse error |
| `'or'1'='1` | 200 | 4888 | **Full SQL injection** - leading `'` closes the string literal, turning the query into `WHERE id='' or '1'='1'`, which is true for every row. Response dumped every account in the database |

### Takeaways
- The single quote (`'`) causing a 500 error is the clearest injection indicator: it means user input reaches the SQL query unescaped and unparameterized.
- `'or'1'='1` confirms it's exploitable: closing the string early and appending an always-true condition (`'1'='1'`) bypasses the intended `WHERE id=<input>` filter entirely and returns all rows - a full data disclosure.
- The app leaks no distinction between "valid ID, no rows" and "invalid ID" in plain responses (both just render emptyish pages), so blind enumeration isn't useful here - but error-based and boolean-based injection both work.
- **Root cause:** input is concatenated into a single-quoted SQL string with no sanitization, escaping, or parameterized queries.

---

## Lab: Cluster Bomb on DVWA Login (Low security)

**Target:** DVWA login form
**Setup:** Username and password marked as positions; attack type set to Cluster Bomb.
**Wordlists:**
- Usernames: admin, user, gordonb, 1337, pablo, smithy
- Passwords: password, admin, letmein, charley, abc123, bug

### Result
Every request returned status 302 with nearly identical response length - status/length alone couldn't tell valid from invalid logins. The difference was in the `Location` header of the redirect: successful logins redirect to `index.php` (the dashboard), failed logins redirect back to `login.php`.

**Valid combinations found:**

| Username | Password |
|----------|----------|
| admin    | password |
| gordonb  | abc123   |
| 1337     | charley  |
| pablo    | letmein  |
| smithy   | password |

Note `smithy` and `admin` share the same password (`password`) - a reminder that password reuse across accounts is itself a finding worth flagging in a real pentest, since compromising one account's credential can expose others.

### How I identified it
Opened each candidate response and checked the `Location` header: `index.php` = successful login, `login.php` = failed. Status code and content length were identical across success/failure, so they couldn't be used to filter results directly (a Grep - Extract rule on the `Location` header would have surfaced this as its own column and saved time checking responses one by one).

### Why Cluster Bomb and not Sniper
Sniper only varies one position at a time while holding the other at its original value - it can't test a username and password together as a pair. Cluster Bomb tries every combination of both payload sets, which is exactly what's needed here since the valid password differs per account and isn't known in advance. Pitchfork would only work if the username/password pairs were already known and lined up by index (e.g. from a leaked credential list) - here we were guessing blind, so Cluster Bomb's full combination coverage was necessary.
