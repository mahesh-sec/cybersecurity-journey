# Authentication, Session Management & IDOR Notes

## Authentication / session labs
| Lab | Weakness | How I exploited it | Fix |
|---|---|---|---|
| TODO | e.g. username enumeration via response difference | TODO | Generic error messages, rate limiting |
| TODO | TODO | TODO | TODO |

## IDOR labs
| Lab | Object referenced | What I changed | What I accessed | Fix |
|---|---|---|---|---|
| TODO | e.g. `/chat?id=2.txt` | TODO | TODO | Server-side ownership check |
| TODO | TODO | TODO | TODO | TODO |

**IDOR in one line:** the app uses a user-supplied identifier to fetch data but never checks that the requester owns it.

## DVWA cookie inspection
- Cookies seen: `PHPSESSID`, `security` (TODO: confirm)
- Flags: `HttpOnly` TODO / `Secure` TODO / `SameSite` TODO
- Observation: TODO (e.g. session ID predictability, missing Secure flag over HTTP)

## Key takeaways
- TODO
