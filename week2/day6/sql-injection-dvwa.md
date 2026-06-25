# SQL Injection — DVWA (Low / Medium / High)

**Date:** Week 2, Day 6
**Target:** DVWA on Metasploitable2 (`192.168.56.101`)
**Module:** SQL Injection

---

## 1. Objective

Demonstrate the classic tautology-based SQL injection (`' OR '1'='1`) against DVWA's User ID lookup field at all three security levels, and explain — not just observe — why the same payload produces three different outcomes depending on the server-side defense in place.

---

## 2. Methodology & Results

### Low Security — Full Bypass

**Baseline test (IDs 1–5):** Each numeric ID returned exactly one user's first/last name, confirming normal query behavior before injecting anything.

**Payload:**
```
' OR '1'='1
```

**Underlying query (no input sanitization at Low):**
```sql
SELECT first_name, last_name FROM users WHERE user_id = '' OR '1'='1';
```

**Result:** Every user in the `users` table was returned in a single request.

**Why it works:** The leading `'` closes the string literal early, turning the rest of the input into live SQL logic rather than data. `'1'='1'` is a string comparison that's always true, and since it's joined with `OR`, the WHERE clause becomes true for every row regardless of the (now-irrelevant) `user_id = ''` condition.

---

### Medium Security — Error-Based Leak (Defense Bypassed Differently)

**Same payload, same input field.**

**Result:**
```
You have an error in your SQL syntax; check the manual that corresponds to your
MySQL server version for the right syntax to use near '\' OR \'1\'=\'1' at line 1
```

**Underlying query (escaping applied — likely `mysqli_real_escape_string()`):**
```sql
WHERE user_id = '\' OR \'1\'=\'1';
```

**Why this happens:** Medium security escapes the `'` character unconditionally — turning it into a literal `\'` — but does so blindly, with no awareness of surrounding query structure. The escaped string is no longer valid SQL, so MySQL throws a syntax error rather than either matching one row or matching all rows.

**Why this still matters as a finding:** A raw SQL error returned to the browser is itself informative — it confirms the backend is MySQL and reveals part of the query's literal structure. This is the foundation of **error-based SQL injection**: crafting payloads specifically to make the database leak information through its own error messages, rather than through normal query results.

---

### High Security — Clean Block (Parameterized Queries)

**Same payload, same input field.**

**Result:** No error, no extra rows — behaves exactly like submitting a non-existent ID.

**Why it works (the actual fix, not just a patch):** High security uses **parameterized queries / prepared statements**. The query structure is compiled first, with a placeholder for the input value; the input is then bound to that placeholder purely as data. It is never concatenated into the query string and therefore can never be interpreted as SQL syntax — there is nothing for a `'` to "break out of," because the query structure was already fixed before the input was ever considered.

---

## 3. The Three-Tier Comparison

| Security Level | Defense | Mechanism | Result |
|---|---|---|---|
| **Low** | None | Input concatenated directly into query string | Full data dump — input becomes executable SQL logic |
| **Medium** | Character escaping | `'` blindly converted to `\'`, regardless of context | SQL syntax error — defused but malformed, leaks DB info |
| **High** | Parameterized queries | Input bound as a value to a precompiled query template | Clean failure — input never enters the query structure at all |

**Key takeaway:** Escaping (Medium) is a patch — it stops the specific character-level attack but can still misfire or be defeated by encoding tricks. Parameterized queries (High) are the actual fix used in real production code, because user input is structurally incapable of becoming part of the query logic, regardless of what characters it contains.

---

## 4. Key Commands / Steps Reference

| Step | Action |
|---|---|
| 1 | Navigate to `http://192.168.56.101/dvwa/`, log in (`admin` / `password`) |
| 2 | DVWA Security tab → set level → Submit |
| 3 | SQL Injection module → enter payload in User ID field → Submit |
| 4 | Repeat at each security level, observing the different failure/success mode |
