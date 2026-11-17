## Decoder

**Tool:** Burp Suite Community, Decoder tab. **Target:** DVWA running locally.

Decoder converts data between encodings and can hash it. The key skill is recognising what format a value is in before choosing an option.

### 1. PHP session cookie

- Copied the `PHPSESSID` value from a captured DVWA request (a 32-character hex string, redacted here).
- "Decode as plain text" left it unchanged. The other decode options produced garbage.
- **Why:** it is not encoded data. It is a random session ID that PHP uses as a lookup key on the server, so there is nothing to decode.
- **Security note:** a predictable session ID could be guessed or hijacked, which is why it must be random.

### 2. Base64

- Decoded `QmFzZTY0IGlzIGNvb2wh` with **Decode as > Base64**.
- Result: `Base64 is cool!`
- Base64 strings are recognisable by their character set (letters, digits, `+`, `/`) and often end with `=` padding.

### 3. HTML encoding

- Encoded `low` (DVWA's `security` cookie value) with **Encode as > HTML**.
- Result: `&#x6c;&#x6f;&#x77;`. Each letter becomes a hex numeric entity (`6c` is 108, the ASCII code for `l`).
- Decoding it with **Decode as > HTML** returned `low`.
- **Why it matters:** browsers render these entities as normal text, so attackers use encoding to get strings past naive filters (relevant for XSS later). Encoding is reversible.

### 4. Hashing

Hashed two inputs that differ by one character, using **Hash... > MD5**:

| Input | MD5 |
|---|---|
| `low` | `53cced8d281a1a0ace3cb6594daaa4f7` |
| `Low` | `28d0edd045e05cf5af64e35ae0c4c6ef` |

- Changing one letter from lowercase to uppercase produced a completely unrelated hash.
- Decoder shows the raw bytes in a hex view. Copying the bytes without spaces gives the usual 32-character form.
- My first attempt showed identical output for both inputs because the second run hashed the same text again. Re-running with a capital `L` gave the correct result.
- **Pyramid of Pain link:** this is the "trivial" level. An attacker can change one byte of a malicious file and every hash-based IOC stops matching.

### Encoding vs hashing

| | Reversible? | Purpose |
|---|---|---|
| Encoding (Base64, HTML, URL) | Yes, anyone can undo it | Represent data safely or in a different format |
| Hashing (MD5, SHA-256) | No, one-way | Fingerprint data, verify integrity |

![Decoder: Base64 and HTML results](screenshots/decoder-base64-html.png)
![Decoder: MD5 of low vs Low](screenshots/decoder-md5.png)

## Comparer

**Goal:** compare a failed DVWA login with a successful one to see what differs.

**Setup:** Firefox proxied through Burp (127.0.0.1:8080), Intercept **off**. Burp logs everything in Proxy > HTTP history, and items were sent to Comparer from there.

### Request comparison (Words mode)

Compared the POST to `/login.php` with a wrong password and the correct password. Four differences:

| Field | Why it differs |
|---|---|
| `password` | The one thing I changed |
| `Content-Length` | 83 vs 88. The correct password is 5 characters longer |
| `user_token` | DVWA's anti-CSRF token. It is regenerated each time the login page loads |
| `PHPSESSID` | The two requests came from different sessions |

**Takeaway:** because the CSRF token changes every time, a brute-force tool cannot just replay one captured request. Each attempt needs a fresh token.

### Response comparison (Words mode)

Both responses were `302 Found`, 458 bytes, with `Content-Length: 0`. Four differences:

| Field | Meaning |
|---|---|
| `Date` | Timing noise (responses were four seconds apart) |
| `Set-Cookie` `expires` | Calculated from the current time, so it shifts with `Date` |
| `PHPSESSID` | A new session ID issued each response |
| `Location` | `login.php` (failed) vs `index.php` (success) |

**Takeaway:** the status code and response length were identical, so they cannot tell success from failure. Only the `Location` header does. Brute-force tools judge a guess by what changes in the response, so they have to read a field like `Location` and ignore the noise.

**Defender view:** a burst of failed logins that all redirect to `login.php` is a detectable pattern in the logs. That links to the host/network artifacts level of the Pyramid of Pain.

![Comparer: request comparison](screenshots/comparer-request.png)
![Comparer: response comparison](screenshots/comparer-response.png)
