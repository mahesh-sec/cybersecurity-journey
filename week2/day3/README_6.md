# Day 3 Theory — TLS 1.2 vs TLS 1.3 Handshake & HTTPS Metadata Leakage

**Week 2, Day 3 — Cybersecurity Self-Study Roadmap**

---

## 1. TLS 1.2 Handshake (RSA Key Exchange)

1. **ClientHello** — client sends supported TLS version and supported cipher suites.
2. **ServerHello** — server responds with the TLS version and cipher suite it selected.
3. **Certificate** — server sends its certificate (contains domain name + server's public key).
4. **CertificateVerify** — server proves it holds the private key matching that certificate.
5. **Key Exchange** — client generates a random pre-master secret, encrypts it with the server's public key, and sends it.
6. **Finished** — both sides confirm the handshake integrity.

### Certificate validation (client side)

The client validates the certificate using the CA's public key:

```
CA computes: hash(certificate)
CA encrypts that hash with CA's private key  → this is the CA's signature

Client receives certificate + signature
Client decrypts signature using CA's public key → recovers CA's hash
Client independently computes hash(certificate)

If both hashes match → certificate is authentic and untampered
```

### CertificateVerify (proving the server holds the private key)

Certificate validation alone only proves the *certificate* is legitimate — it doesn't prove
the server on the other end of the connection actually owns the private key for it. That's
what `CertificateVerify` is for:

```
Server computes: hash(entire handshake transcript so far)
Server encrypts that hash with its own private key → sends as CertificateVerify

Client decrypts CertificateVerify using the server's public key (from the certificate)
Client independently computes hash(handshake transcript so far)

If both match → the server genuinely holds the private key, not just a copied certificate
```

This separation matters: without this step, an attacker presenting a stolen-but-valid
certificate could pass certificate validation without ever proving live possession of the
private key.

### Key exchange and session encryption

```
Client generates a random session key (using the negotiated cipher)
Client encrypts it with the server's public key → sends to server
Server decrypts it using its private key
→ Both sides now share the same session key, used to encrypt all further data
```

### Finished messages (anti-MITM / anti-replay check)

```
Client: hash(full conversation so far) → encrypt with session key → send as "Finished"
Server: hash(full conversation so far) → encrypt with session key → send as "Finished"

Each side decrypts the other's Finished message and compares it
against its own locally computed hash.

If they match → no MITM or replay attack occurred during the handshake
```

---

## 2. TLS 1.3 — What Changes

| | TLS 1.2 | TLS 1.3 |
|---|---|---|
| Key exchange | RSA (key exchange) or ECDHE | **Always ECDHE** |
| Authentication | RSA signature | RSA or other signature scheme |
| Round trips | 2 | **1** |
| Forward secrecy | No (RSA key exchange) | **Yes** (ECDHE) |
| Certificate visibility on wire | Plaintext | Encrypted (once early keys are derived) |

### Forward secrecy — the real difference

In TLS 1.2 with RSA key exchange, the server reuses the **same long-term public/private
key pair** across many sessions. If that private key is ever compromised, an attacker who
recorded past encrypted traffic can decrypt **every previous session**, because all of
those sessions' keys were derived from the same long-term key.

In TLS 1.3, ECDHE generates a **fresh, random key pair for every single session**. Even if
the server's long-term private key is later compromised, past sessions cannot be decrypted,
since their session keys were never derived from it. This property is called
**forward secrecy**.

> Note: private keys are never transmitted on the wire in *either* version — that's not what
> changes between 1.2 and 1.3. What changes is whether session keys are *derivable* from a
> single long-term secret (1.2/RSA) or freshly generated per-session (1.3/ECDHE).

---

## 3. Why HTTPS Still Leaks Metadata

Even though TLS encrypts the payload, several things remain visible to anyone observing
the traffic:

### SNI (Server Name Indication)

The `ClientHello` includes the SNI field so the server knows which domain's certificate to
present (needed for virtual hosting, where one server hosts multiple domains on one IP).
The `ClientHello` is the **first message of the handshake**, sent before any key exchange
has occurred — there is no session key yet to encrypt it with. So SNI is sent in **plaintext
by default** in both TLS 1.2 and TLS 1.3.

> TLS 1.3 supports ECH (Encrypted Client Hello) to hide SNI, but most servers don't support
> it yet — so in practice, SNI is still visible on the vast majority of HTTPS traffic today.

### Certificate exposure

- **TLS 1.2:** the certificate is sent fully in **plaintext** right after ServerHello, since
  no encryption keys exist at that point yet. This means the server's public key (embedded
  in the cert) and domain name are visible to anyone capturing traffic.
- **TLS 1.3:** the ECDHE key exchange happens earlier (right after ServerHello), so the
  certificate message itself is **encrypted** using keys derived from that early exchange.
  An eavesdropper sees ciphertext, not the certificate.

This is a genuine, meaningful difference between the two versions — not just an SNI
similarity.

### IP addresses

Always visible in plaintext, in both versions, because routers need to read the IP header to
deliver the packet. TLS only encrypts the application payload, not network/transport headers.

### Timing and packet size (traffic analysis)

Even without reading any content, an observer can infer behavior from patterns — e.g. a
burst of large packets suggests a video loading; a short, small exchange suggests a login
or form submission. Encryption hides *content*, not *behavior patterns*.

---

*Notes compiled as part of Week 2 self-study (networking/protocol attacks phase) —
[cybersecurity-journey](https://github.com/mahesh-sec/cybersecurity-journey) repo.*
