# DNS Tunneling & DNS Amplification DDoS — Week 2, Day 2

Supplementary DNS attack theory studied alongside the core Protocol Attack Table.

---

## DNS Tunneling

**What is attacked/abused:** The trust placed in DNS traffic — DNS is almost always permitted outbound even on locked-down networks, since blocking it breaks all name resolution.

**How it works:**

*Exfiltration (data out):*
1. The attacker owns a domain (e.g. `evil.com`) and runs its authoritative nameserver.
2. Malware on the compromised host encodes stolen data (base32/base64) into a subdomain label, e.g. `733z3kr1td4t4chunk1.evil.com`.
3. The victim machine issues a normal-looking DNS query for that name.
4. The query transits the local resolver and gets forwarded up the chain like any other lookup, since no one else can answer for `evil.com` except the attacker's nameserver.
5. The attacker's nameserver logs the subdomain — the actual exfiltrated data — rather than caring about resolving anything.
6. Large files are broken into many sequential queries (DNS labels are limited to 63 characters, full hostnames to 253).

*Infiltration / C2 (commands in):*
1. The compromised host periodically queries the attacker's domain.
2. The attacker's nameserver replies with command data stuffed into the response — commonly via **TXT** records (free-form text) or **NULL** records (rarely used legitimately).
3. The malware decodes and executes the embedded command.

**What the attacker gains:** A covert channel for data exfiltration or command-and-control that bypasses most firewalls and proxies, since DNS inspection is typically much shallower than HTTP inspection.

**What a defender looks for:**
- Abnormally long subdomains/hostnames.
- High query volume to a single domain in a short window.
- High-entropy (random-looking) subdomain strings.
- Repeated queries for unusual record types (TXT, NULL).
- Queries to newly registered or low-reputation domains.
- Tools associated with this technique: `dnscat2`, `iodine`.

---

## DNS Amplification DDoS

**What is attacked:** Bandwidth/availability of a victim, using open DNS resolvers as unwitting amplifiers.

**How it works:**
1. An **open resolver** is a DNS server that answers recursive queries from anyone, not just its own network's clients.
2. DNS runs over UDP, which has no handshake and does not verify the source IP address on a packet.
3. The attacker crafts a small DNS query but forges the source IP field in the packet header to contain the **victim's** IP address instead of their own.
4. The attacker sends this spoofed query to an open resolver, requesting a record type known to produce a large response (classically `ANY`, or a DNSSEC-signed record).
5. The resolver reads the (forged) source field, has no way to know it was spoofed, and sends its — much larger — response to that address.
6. The victim receives a disproportionately large, unsolicited response they never actually requested.
7. Repeated at scale across thousands of open resolvers and many queries simultaneously, the combined response traffic floods the victim's bandwidth. Amplification factors have historically exceeded 50x the original query size.

**What the attacker gains:** A high-volume denial-of-service attack against the victim, at a fraction of the bandwidth cost to the attacker — the "amplification."

**What a defender looks for:**
- A sudden flood of inbound DNS *response* packets (source port 53) with no matching outbound queries.
- Traffic from many distinct DNS server IPs converging on one destination simultaneously.
- Abnormally large UDP packets on port 53.
- Mitigations: Response Rate Limiting (RRL) on DNS servers; BCP38 (ingress/egress filtering that blocks packets whose source IP doesn't belong to the originating network, stopping the spoofing at the source).

**Key distinction:** Unlike spoofing or tunneling, amplification doesn't deceive the victim or poison anything — the victim's own DNS resolution is untouched. It's a pure volume/availability attack riding on DNS infrastructure.

---

## Sources
- Cloudflare Learning Center
- Professor Messer (DNS, ARP video series)
- Krebs on Security
