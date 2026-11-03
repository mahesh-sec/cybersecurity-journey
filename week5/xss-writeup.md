# Cross-Site Scripting (XSS) Write-up

## Types (in my own words)
- **Reflected:** payload in the request is echoed straight back in the response.
- **Stored:** payload is saved (e.g. a comment) and runs for every visitor.
- **DOM-based:** client-side JS writes attacker data into the page unsafely, no server round-trip needed.

## DVWA
| Level | Type | Payload | Result | Bypass logic |
|---|---|---|---|---|
| Low | Reflected | `<script>alert('XSS')</script>` | Alert popup via the `name` GET parameter | none needed — confirmed earlier this week |
| Low | Stored | `TODO` | TODO | none needed |
| Medium | Reflected | `TODO` | TODO | TODO (what the filter blocked, what got around it) |
| Medium | Stored | `TODO` | TODO | TODO |
| High | TODO | `TODO` | TODO | TODO |

## PortSwigger labs — Apprentice (3 completed, one per type)
| # | Lab name | Type | Context | Typical payload |
|---|---|---|---|---|
| 1 | Reflected XSS into HTML context with nothing encoded | Reflected | Search results echoed straight into the page | `<script>alert(1)</script>` |
| 2 | Stored XSS into HTML context with nothing encoded | Stored | Blog comment field, rendered for every visitor | `<script>alert(1)</script>` |
| 3 | DOM XSS in `document.write` sink using source `location.search` | DOM-based | Search query tracking script writes `location.search` straight into the page with `document.write` | `"><svg onload=alert(1)>` |

**TODO:** confirm the exact payload you used for each (the ones above are the standard documented approach) and note anything that differed — e.g. if your DOM lab was the `innerHTML` sink variant instead of `document.write`, swap that in.

## Impact
Session/cookie theft, credential theft, defacement, phishing inside a trusted page, actions as the victim.

## Fix
Output encoding for the right context (HTML/attribute/JS/URL), Content-Security-Policy without unsafe-inline, `HttpOnly` + `SameSite` cookies, avoid unsafe sinks like `innerHTML`/`document.write`.
