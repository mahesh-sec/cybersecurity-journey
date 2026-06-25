
# Day 5 — Defensive Detection Rules

Building on the Day 2 Protocol Attack Table. This file separates two things deliberately: the **recognition-level flags** I can currently state and explain from memory, and a **reference section** of more formal detection rules (filter syntax, log logic, MITRE/CAPEC mappings) for later depth — not yet memorized, captured here for when SIEM/detection-engineering work comes up later in the roadmap.

---

## What I can currently identify (recognition level)

### ARP Poisoning
**Flag:** Multiple ARP replies claiming different MAC addresses for the same IP address.
**Why this works:** ARP has no built-in authentication — any device can claim to own any IP, and the receiving device has no way to verify it. A legitimate IP should only ever map to one MAC; if two replies disagree, one of them is forged.

### DHCP Starvation
**Flag:** A large number of DHCP Discover requests arriving from many different (often spoofed) MAC addresses in a short time window.
**Why this works:** A legitimate network shouldn't see dozens of new devices joining simultaneously. A burst of Discovers from many distinct MACs is consistent with an attacker exhausting the DHCP pool to deny service to real clients.

### HTTP Request Smuggling
**Flag:** A request containing both `Content-Length` and `Transfer-Encoding` headers, where the two imply different message lengths.
**Why this works:** Legitimate clients essentially never send both headers. Their presence together signals an attempt to make front-end and back-end servers disagree about where one request ends and the next begins.

### DNS Tunneling
*(Note: this attack is not in the Day 2 table — it was attached to DNS in this conversation but is a separate attack type from DNS spoofing, which is what the table actually covers. Documented here since it came up and was correctly reasoned through.)*

**Flag:** High volume of queries from one device (or many devices) to the same parent domain, where subdomains look long/random/high-entropy rather than human-readable, combined with heavy use of less-common record types (TXT, NULL, CNAME) and a destination domain that isn't a recognized service.
**Why this works:** Tunneling encodes smuggled data inside subdomain labels and abuses record types that can carry more arbitrary data than a standard A record. Normal browsing doesn't generate this volume or entropy pattern to a single unfamiliar domain.

### DNS Spoofing
*(This is the attack actually covered in the Day 2 table — distinct from tunneling above.)*

**Flag:** The same DNS query receiving two different answers — e.g. different resolved IPs for the same domain/transaction ID, or a domain's resolved IP changing unexpectedly for a host that's historically been stable, or a TTL that doesn't match the legitimate record's known TTL.
**Why this works:** Spoofing relies on injecting a forged answer alongside or instead of the real one. The signature isn't volume or weird naming — it's a contradiction between two answers to the same question.

---

## Escalation framing (general principle, applies to all four)

When flagging any of the above, separate **confirmed evidence** from **hypothesis about root cause**, and end with a recommended next investigative step rather than asserting why the anomaly is happening. Example structure used during the ARP storm PCAP analysis:

> Observed [specific volume/pattern] from [device/IP/MAC] over [time window]. [Specific corroborating detail, e.g. reply count]. This pattern is anomalous for normal [protocol] behavior. Possible causes include [hypothesis A] or [hypothesis B]. Recommend [specific next step] before concluding root cause.

---

## Reference: more formal detection logic (for later depth, not yet memorized)

These are more precise versions of the above — specific filter syntax, log-rule phrasing, and standards references. Useful to revisit once SIEM/detection-engineering content appears later in the roadmap.

| Attack | Wireshark filter / log logic | Standards reference |
|---|---|---|
| ARP Poisoning | `arp.opcode == 2` then check for repeated `arp.src.proto_ipv4` with differing `arp.src.hwaddr`; Wireshark's built-in `arp.duplicate-address-detected` heuristic | MITRE ATT&CK T1557.002 |
| DHCP Starvation | `bootp.option.dhcp == 1` (Discover only), alert if >N Discovers from N distinct MACs within a short window; alert if Offer/Ack source IP isn't the known DHCP server (rogue server detection) | CAPEC-153 (no direct ATT&CK technique — infrastructure-level attack, not post-compromise behavior) |
| HTTP Request Smuggling | WAF rule: reject/normalize requests with both `Content-Length` and `Transfer-Encoding`; log correlation between front-end and back-end request counts | CWE-444 (implementation flaw, not a clean ATT&CK technique) |
| DNS Tunneling | `dns.qry.name` length/entropy thresholds; alert on high query volume to one parent domain; alert on disproportionate TXT/NULL record usage | MITRE ATT&CK T1071.004 |
| DNS Spoofing | Alert if two responses share a transaction ID/query name but differ in answer data; alert on TTL anomalies vs. historical baseline; DNSSEC validation failures | CAPEC-142; loosely under ATT&CK T1557 (Adversary-in-the-Middle) |

**Note on maturity of this mapping:** Not every attack here has a clean 1:1 MITRE ATT&CK technique — DHCP starvation and HTTP smuggling are better described by CAPEC or CWE entries, since ATT&CK is weighted toward post-compromise adversary behavior rather than every possible network-layer attack. Knowing *that* distinction is itself worth being able to say in an interview, rather than forcing a technique ID where one doesn't cleanly fit.
