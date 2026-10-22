## DVWA SQLi — Medium security

### What changed from Low

- The input field became a **dropdown** instead of free text, and the form
  submits via **POST** instead of GET — so the payload no longer appears in
  the URL and can't be edited there.
- The backend applies `mysqli_real_escape_string()` to the input before
  using it in the query.
- The query template itself changed — the `user_id` value is no longer
  wrapped in quotes:
  ```php
  $query = "SELECT first_name, last_name FROM users WHERE user_id = $id;";
  ```
  (Low used `WHERE user_id = '$id'` — quoted.)

### Bypassing the dropdown restriction

The dropdown only limits what the *browser UI* lets you pick — it places no
actual constraint server-side. Opened dev tools (right-click the dropdown →
Inspect), found the `<option value="1">` elements, and edited one option's
`value` attribute directly to the payload. Selecting that edited option and
submitting sends it exactly as typed.

### Why the escaping filter didn't stop the payload

`mysqli_real_escape_string()` only escapes characters that are special
*inside a quoted string* (`'`, `"`, backslashes, etc.). Because the query
template here has **no quotes** around `$id`, a payload with no quotes in it
gives the filter nothing to act on — it passes through completely
unchanged.

### Payload used

```
1 UNION SELECT user, password FROM users -- 
```

Resulting query:
```sql
SELECT first_name, last_name FROM users WHERE user_id = 1 UNION SELECT user, password FROM users -- ;
```

### Results — full table dump

| Username | Hash (MD5) |
|----------|-------------------------------------|
| admin    | 5f4dcc3b5aa765d61d8327deb882cf99 |
| gordonb  | e99a18c428cb38d5f260853678922e03 |
| 1337     | 8d3533d75ae2c3966d7e0d4fcc69216b |
| pablo    | 0d107d09f5bbe40cade3de5c71e9e9b7 |
| smithy   | 5f4dcc3b5aa765d61d8327deb882cf99 |

Hashes match the Low-level dump exactly (same unsalted MD5 values, same
cracked plaintexts: admin/password, gordonb/abc123, 1337/charley,
pablo/letmein, smithy/password).

### Finding summary

Medium security's input filtering escapes quote characters but the query
places `user_id` in an **unquoted numeric context**, so a payload containing
no quotes bypasses the filter entirely. The dropdown UI control is a
client-side restriction only and was bypassed by editing the `<option>`
element's value via browser dev tools — no proxy tool (e.g. Burp) was
needed since DVWA's SQLi form is simple enough to manipulate directly in
the DOM. Full credential compromise achieved identically to Low security.
