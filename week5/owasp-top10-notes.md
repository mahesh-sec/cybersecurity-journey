# OWASP Top 10:2025 Notes

Source: https://top10.owasp.org/2025/

| # | Category | Root Cause | Example Attack | Primary Defense |
|---|----------|-----------|----------------|-----------------|
| A01 | Broken Access Control | Server doesn't enforce who can access what | Changing an ID in the URL to view another user's data (IDOR) | Deny by default, check permissions server-side on every request |
| A02 | Security Misconfiguration | Insecure defaults, unused features, verbose errors | Logging in to an admin panel with default credentials | Hardened baseline config, remove unused features |
| A03 | Software Supply Chain Failures | Untrusted or compromised dependencies and build tools | Malicious update in a third-party package | Verify dependencies, pin versions, monitor the supply chain |
| A04 | Cryptographic Failures | Weak or missing encryption of sensitive data | Intercepting data sent over plain HTTP, cracking weak hashes | Strong algorithms, TLS everywhere, proper key management |
| A05 | Injection | Untrusted input mixed into commands or queries | SQL injection: `1' OR '1'='1` | Parameterized queries, input validation |
| A06 | Insecure Design | Missing security thinking at design stage | Business logic abuse, e.g. unlimited password reset attempts | Threat modeling, secure design patterns |
| A07 | Authentication Failures | Weak login, session or credential handling | Credential stuffing, session hijacking | MFA, strong session management, rate limiting |
| A08 | Software or Data Integrity Failures | Code or data trusted without integrity checks | Tampered update accepted by the app | Digital signatures, integrity verification |
| A09 | Security Logging and Alerting Failures | Events not logged, no alerts on attacks | Attack goes unnoticed for months | Log security events, set up alerting |
| A10 | Mishandling of Exceptional Conditions | Errors and edge cases handled badly | Crafted input triggers a crash or leaks internal details | Handle errors safely, fail closed, test edge cases |
