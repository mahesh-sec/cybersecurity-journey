# Cross-Site Scripting (XSS) Write-up

**Week 5, Day 4** | Part of `cybersecurity-journey/week5/`

## 1. What is XSS?

XSS is when untrusted input is executed as JavaScript in a victim's browser under a trusted website's origin. The attacker injects JavaScript into a page the victim already trusts, so the script runs with that site's origin and can reach its cookies and session data.

**Typical impact**
- Stealing cookies and session tokens (cookies marked `HttpOnly` cannot be read by JavaScript)
- Acting as the user: changing settings, sending requests on their behalf
- Logging keystrokes
- Showing fake login forms on the trusted page

## 2. Types of XSS

### 2.1 Reflected XSS
- The attacker crafts a malicious link, with the payload in a URL parameter or form field, and tricks the victim into opening it.
- The server echoes the payload straight back in the response. Nothing is stored.
- Depends on social engineering, since the victim has to click the link.

### 2.2 Stored XSS
- The attacker submits the payload and the server saves it (for example, in the database).
- Whenever other users request the affected page, the payload is served to them and executes.
- No crafted link is needed: anyone who visits the page is affected. This is why stored XSS is generally considered more dangerous than reflected.

### 2.3 DOM-based XSS
- The vulnerability is in client-side JavaScript. Attacker-controlled data flows from a **source** into a dangerous **sink**.
- Happens entirely in the browser. With payloads in the URL fragment (`#...`), the payload may never reach the server, so server-side logs and filters cannot see it.

| | Examples |
|---|---|
| **Sources** (where attacker data enters) | `location.hash`, `location.search`, `document.referrer` |
| **Sinks** (where it becomes dangerous) | `innerHTML`, `document.write()`, `eval()` |

### 2.4 Comparison

| Type | Where the payload lives | Stored on server? | Victim action needed |
|---|---|---|---|
| Reflected | Request (URL/form), echoed in response | No | Click a crafted link |
| Stored | Server-side storage, served to visitors | Yes | Just visit the page |
| DOM-based | Client-side source flowing to a sink | No | Usually a crafted link |

## 3. Context matters

Escaping and encoding are specific to the context where data ends up. The same input can be safe in one context and dangerous in another:

- **SQL context:** `mysqli_real_escape_string()` escapes characters like `'` so input cannot break out of the SQL query. This stops SQL injection.
- **HTML context:** the same input, printed into a page without encoding, can still execute as HTML/JavaScript. SQL escaping does nothing to `<`, `>` or `<script>`.

Also, a payload that works in plain HTML may fail inside an HTML attribute, a JavaScript string or a URL, which is why filters get bypassed by adapting the payload to its context. *(Add real examples from the Medium-level lab.)*

## 4. DVWA XSS: Low security

### 4.1 Reflected (Low)

- **Payload used:** `<script>alert('XSS')</script>`
- **Example attack link:**
  `http://127.0.0.1:42001/vulnerabilities/xss_r/?name=%3Cscript%3Ealert%28%27XSS%27%29%3C%2Fscript%3E`
  - `?name=` is the parameter the server echoes back.
  - The browser URL-encodes the payload (`%3C` = `<`, `%3E` = `>`, `%28` = `(`, `%29` = `)`, `%27` = `'`, `%2F` = `/`), and the server decodes it before reflecting it.
  - In a real attack, the host would be the trusted vulnerable site, which makes the link look legitimate.
- **Where it travels in the request:** the `name` GET parameter in the URL.
- **Where it appears in the response:** inserted unencoded in the HTML right after "Hello" (confirmed with View Page Source).
- **Result:** alert popup showing `XSS`.

**First attempt:** `<script>danger</script>` showed only "Hello". The page showed no literal text, which meant the browser had treated the input as HTML and run the script. `danger` is not a defined variable, so it threw a `ReferenceError`, visible in the browser console. A payload that does something visible (`alert`, `console.log`) confirms execution more clearly.

**Source code analysis (Low):**
1. Checks that a `name` parameter exists in the GET request and is not null.
2. Takes the value from `$_GET['name']`.
3. Prints it straight back into the page after "Hello".

The code never sanitizes or encodes the input, so the browser cannot tell the payload apart from the page's own HTML. This missing output encoding is the root cause.

### 4.2 Stored (Low)

**Source code analysis (Low), write side:**
1. `trim()` removes leading and trailing whitespace from the message and the name.
2. `stripslashes()` removes backslashes from the message only.
3. `mysqli_real_escape_string()` escapes special characters for SQL on both fields.
4. Both are inserted into the `guestbook` table (`comment`, `name` columns).

**What this means**
- The code protects against SQL injection but does nothing against XSS. None of the steps encode `<`, `>` or `<script>`, so the payload is stored unchanged.
- The single quote in the payload gets a backslash only so the INSERT statement parses correctly. The database stores the quote itself, so the payload comes back intact.
- `stripslashes()` being missing on the Name field makes no difference to a basic XSS payload, because we are attacking the page output, not the query.
- The write-side snippet only stores data. The vulnerable moment is when the guestbook page reads the rows back and prints them without HTML encoding. That display code is not in this snippet.

**Test results** *(fill in after running the test)*
- **Payload used:**
- **Field used (Message / Name):**
- **Result on submit:**
- **Result on reload (without resubmitting):**
- **Where it appears in page source:**
- **Who is affected and how:** every visitor to the guestbook page, with no crafted link needed.

**Cleanup:** reset with DVWA's Setup / Reset Database button, or the payload keeps firing.

## 5. DVWA XSS: Medium security

*(Carried over to the weekend.)*
- **How the filter differs from Low:**
- **Bypass payload and why it works:**

## 6. Labs

*(Add the three labs completed, with the payload that worked and why.)*

| Lab | Context input landed in | Payload | Why it worked |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

## 7. Defences

- **Output encoding:** encode data for the context it is output into. In PHP, `htmlspecialchars()` turns `<` into `&lt;`, so a payload displays as harmless text instead of executing.
- **Input escaping is not enough:** SQL escaping protects the query, not the page.
- **To add after the High/CSP block:** Content Security Policy, `HttpOnly` cookies, and any other mitigations.

## 8. Key takeaways

- XSS happens when untrusted input is output into a page without being encoded for that context.
- Reflected needs a victim to click a crafted link, stored hits every visitor, and DOM-based happens when client-side code moves a source into a sink.
- Escaping is context-specific: protecting against SQL injection does not protect against XSS.
- A script that runs but shows nothing (like `danger`) still counts as execution. Check the console and page source.
