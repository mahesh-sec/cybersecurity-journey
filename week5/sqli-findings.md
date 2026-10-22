# SQL Injection Findings — Week 5, Day 2

## Theory

**What is SQL injection?**
A vulnerability where unsanitized user input gets concatenated directly into a
database query. The database can't tell the difference between the app's
intended code and the attacker's injected input, so the input changes the
query's logic instead of staying as plain data.

**Types of SQLi**

| Type | How it works |
|---|---|
| In-band / UNION | Attacker appends a UNION SELECT with a matching column count to pull data from other tables directly into the page output. |
| Error-based | The app displays raw database error messages, which leak data (table names, versions, subquery results) directly in the response. |
| Blind — Boolean | No errors or results are shown. Attacker injects a true/false condition and infers the answer from a difference in page content. |
| Blind — Time-based | Same as above, but the condition triggers a deliberate delay (e.g. SLEEP(5)) instead of a visible change. Answer is inferred from response time. |

**Why `' OR '1'='1` works**
Example query: `SELECT * FROM users WHERE username = '$input';`
Injected: `SELECT * FROM users WHERE username = 'mahesh' OR '1'='1';`
Since OR only needs one side true, and '1'='1' is always true, the WHERE
clause matches every row — the query returns the whole users table instead
of just one user's record.

**Primary defense: parameterized queries**
Input is bound as a literal value through a prepared statement, so the
database never interprets it as part of the query structure — it can only
ever be data, never code.


