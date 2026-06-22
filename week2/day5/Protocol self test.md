# Day 5 — Protocol Mastery Self-Test

Written from memory (no notes), then reviewed for accuracy and gaps. Original recall below, followed by corrections.

---

## 1. DNS Resolution Flow

**Recall:** Client checks local cache → if absent, query goes to configured DNS server (ISP or public resolver) → resolver checks its own cache → if absent, queries a root server → root returns the relevant TLD server's info → resolver queries the TLD server → TLD server returns the authoritative nameserver for the domain → resolver queries the authoritative nameserver → nameserver checks its zone file and returns the IP → resolver returns the IP to the client.

**Corrections:**
- Missing step: between browser cache and the resolver, there's also an **OS-level resolver cache** and a check of the local `hosts` file — both checked before a query ever leaves the machine.
- Resolver cache checks should explicitly include a **TTL validity check** — a cached record is only used if its TTL hasn't expired.
- Minor wording fix: root servers don't hand back the IP for the specific destination domain — they hand back a **referral** (NS records + IPs) for the relevant TLD's nameservers in general.

**Status:** Core flow correct, missing the OS/hosts-file cache layer.

---

## 2. TCP 3-Way Handshake + Teardown

**Recall:** Client sends SYN (with MSS, window size, window scale options) → server responds SYN-ACK (its own MSS, window size, options) → client sends ACK → handshake complete. During the session, each side ACKs packets it receives. To close, one side sends FIN, the other ACKs and sends its own FIN, which gets ACKed, ending the connection cleanly.

**Corrections:** None to the core sequence — accurate as written.

**Addition for completeness:** Closed ports respond to a SYN with **RST**, not SYN-ACK — relevant for recognizing port-scanning traffic, where a flood of RSTs is the expected response to a scan against closed ports.

**Status:** Correct and complete for the happy-path; RST behavior added as a bonus fact.

---

## 3. DHCP DORA Sequence

**Recall:** Device joining a network sends a **Discover** (broadcast, includes its MAC, requests IP/gateway/DNS/other options) → DHCP server responds with an **Offer** (broadcast, includes proposed IP, gateway, lease time, requested options) → device sends a **Request** (broadcast, confirming it accepts the offer) → server sends an **Ack** (broadcast, finalizing the lease) → device begins using the assigned IP.

**Corrections:** None — sequence and broadcast behavior for all four messages stated correctly.

**Status:** Fully correct.

---

## 4. ARP Poisoning

**Recall:** Attacker joins the network. Normally, a device ARP-requests a MAC for a given IP (broadcast), and the legitimate owner replies with its real MAC, which gets cached. An attacker intercepts/responds with a forged reply claiming their own MAC is the correct mapping, and the victim caches the false entry — redirecting future traffic for that IP to the attacker. Also correctly identified a second variant: the attacker sends **unsolicited (gratuitous) ARP replies** with no preceding request at all, and victims cache the false mapping anyway.

**Corrections:** None — both the reactive (race-the-real-reply) and gratuitous (unsolicited) poisoning variants were correctly distinguished.

**Status:** Fully correct, including the less commonly remembered gratuitous-ARP variant.

---

## 5. TLS Handshake

**Recall:** Occurs after TCP handshake. Client sends ClientHello (supported TLS version, cipher suites) → server sends ServerHello (chosen version, chosen cipher suite) → server sends its Certificate → server sends CertificateVerify (described as a hash of the handshake-so-far, encrypted with the server's private key) → client validates the certificate, then verifies CertificateVerify using the server's public key → client generates a session key, encrypts it with the server's public key, sends it to the server → server decrypts with its private key → both sides send ChangeCipherSpec + Finished (containing a hash of the full handshake, used to detect MITM/replay tampering) → both sides compare their calculated hash against the received Finished hash to confirm no tampering occurred.

Also correctly noted: TLS 1.3 completes in 1 round trip vs. 1.2's 2 round trips; TLS 1.3 uses ECDHE exclusively for key exchange vs. 1.2's RSA-or-ECDHE; TLS 1.3 offers 5 cipher suites, all ECDHE-based; TLS 1.3 encrypts the certificate, while 1.2 sends it in plaintext.

**Corrections:**
1. **CertificateVerify is signed, not encrypted.** The server signs a hash of the handshake transcript with its private key to prove identity — signing and encrypting are different operations (the hash isn't secret, so there's nothing to hide; the signature proves only the holder of the private key produced it).
2. **Session key establishment depends on the key exchange method, and the original recall only describes one of two methods.** The "client generates a session key, encrypts with server's public key" description is specifically the **RSA key exchange** flow (TLS 1.2 only). When **ECDHE** is used (available in both 1.2 and 1.3, and the only option in 1.3), both sides perform a Diffie-Hellman exchange and **independently derive** the shared secret — no key is encrypted and transmitted over the wire in that flow.

**Status:** Strong overall structure and accurate version-difference facts; two precision corrections needed around signing vs. encryption, and RSA vs. ECDHE key exchange mechanics.

---

## Summary

| Topic | Accuracy | Key gap |
|---|---|---|
| DNS resolution | ~90% | Missing OS/hosts-file cache layer |
| TCP handshake | ~95% | Complete; RST added as bonus context |
| DHCP DORA | 100% | None |
| ARP poisoning | 100% | None — both variants correctly identified |
| TLS handshake | ~85% | Sign vs. encrypt mixup; RSA vs. ECDHE key exchange conflated |
