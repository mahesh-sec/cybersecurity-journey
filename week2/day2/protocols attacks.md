# Protocol Attack Table — Week 2, Day 2

A reference table documenting four foundational network attack types: what each one targets, how it works step-by-step, what an attacker gains, and what a defender would look for in logs or traffic.

---

## 1. ARP Poisoning

**What is attacked:** The ARP cache of a device on a local network (mapping between IP addresses and MAC addresses).

**How it works, step-by-step:**
1. The attacker joins the local network (e.g. via Wi-Fi or a switch port).
2. The attacker sends forged ARP replies to the victim, claiming the attacker's own MAC address is the correct mapping for the gateway's (or another host's) IP address.
3. Because ARP has no built-in authentication, the victim's machine accepts the unsolicited reply and overwrites its ARP cache entry.
4. The victim now sends traffic intended for the real gateway/host to the attacker's MAC address instead.
5. The attacker typically also poisons the gateway's ARP cache in the same way, claiming to be the victim, so traffic flows both ways through the attacker (classic man-in-the-middle setup).
6. The attacker can now read, modify, or drop traffic before forwarding it on, or pair this position with further attacks (e.g. DNS spoofing).

**What the attacker gains:** A man-in-the-middle position between the victim and the rest of the network (or the internet), enabling traffic interception, credential capture, session hijacking, or injection of forged responses (e.g. fake DNS replies).

**What a defender looks for:**
- Wireshark filter: `arp.duplicate-address-detected` or manually checking for duplicate IP-to-MAC mappings.
- Multiple ARP replies for the same IP address claiming different MAC addresses.
- Gratuitous ARP packets sent without a corresponding request.
- Static ARP entries unexpectedly changing on critical hosts (gateway, DNS server).
- Tools: `arpwatch`, switch port security features (Dynamic ARP Inspection).

---

## 2. DNS Spoofing

**What is attacked:** The DNS resolution process — either a resolver's cache, or a single victim's DNS query in transit.

**How it works, step-by-step:**

*Resolver-side cache poisoning:*
1. A recursive resolver receives a query for a domain it doesn't have cached and sends an outbound query to the authoritative nameserver chain to resolve it.
2. The attacker races to inject a forged DNS response before the legitimate authoritative server replies, guessing the correct transaction ID and source port.
3. If the attacker wins the race, the resolver accepts and caches the forged record — either a fake A record for one hostname, or a fake NS/glue record hijacking the entire zone.
4. Every client behind that resolver receives the poisoned answer until the record's TTL expires.

*On-path (ARP + DNS spoofing) variant:*
1. The attacker first poisons ARP so the victim's traffic routes through the attacker's machine.
2. When the victim sends a DNS query, the attacker intercepts it directly and replies with a forged answer before (or instead of) the real DNS server's response reaching the victim.
3. This affects only the single victim machine, not a shared cache, and the attacker controls the TTL of the forged response.

**What the attacker gains:** The ability to redirect victims to attacker-controlled servers (e.g. fake login pages, malware download sites) while the victim believes they're reaching the legitimate domain.

**What a defender looks for:**
- Sudden, unexplained changes to a domain's resolved IP address.
- Duplicate DNS responses for the same query with different answers/transaction IDs.
- TTL values that don't match the legitimate record's known TTL.
- DNSSEC validation failures.
- ARP anomalies preceding DNS anomalies (a sign of the on-path variant).

---

## 3. DHCP Starvation

**What is attacked:** The DHCP server's pool of available IP addresses.

**How it works, step-by-step:**
1. The attacker generates a large number of DHCP Discover requests, each using a spoofed/randomized MAC address.
2. The legitimate DHCP server responds to each with an Offer and eventually leases out IP addresses to these fake clients.
3. The attacker repeats this rapidly until the entire DHCP address pool is exhausted.
4. Legitimate devices joining the network can no longer obtain a valid IP lease, causing a denial of service.
5. Often paired with a follow-up attack: once the real DHCP server is starved or disabled, the attacker stands up a rogue DHCP server, which now becomes the only one answering, allowing the attacker to hand out a malicious gateway/DNS server address to new clients.

**What the attacker gains:** Denial of service against new clients joining the network, and/or the ability to become the de facto DHCP server, gaining control over DNS and gateway settings handed to victims.

**What a defender looks for:**
- A sudden spike in DHCP Discover packets from many different MAC addresses in a short time.
- DHCP pool utilization approaching 100% unexpectedly fast.
- Multiple DHCP servers responding to the same Discover broadcast (visible as multiple Offers with different server IPs).
- Switch-level mitigation: DHCP snooping, port security limiting MAC addresses per port.

---

## 4. HTTP Request Smuggling

**What is attacked:** The discrepancy in how a front-end server (e.g. a proxy or load balancer) and a back-end server interpret the boundaries between HTTP requests in the same connection.

**How it works, step-by-step:**
1. An HTTP request can specify its body length using either the `Content-Length` header or `Transfer-Encoding: chunked`.
2. If a request includes both headers, the front-end and back-end servers may disagree on which one to trust.
3. **CL.TE:** The front-end uses `Content-Length`, the back-end uses `Transfer-Encoding`. The attacker crafts a request where the back-end interprets part of the body as the start of a second, smuggled request.
4. **TE.CL:** The reverse — front-end uses `Transfer-Encoding`, back-end uses `Content-Length`, again causing a desynchronization.
5. The smuggled portion of the request gets processed by the back-end as if it came from the next legitimate user's connection (since many back-ends reuse connections between the front-end and back-end for multiple users' requests).

**What the attacker gains:** The ability to bypass front-end security controls, hijack another user's request/response (potentially capturing their session data), poison the web cache, or smuggle requests that the front-end would normally have blocked.

**What a defender looks for:**
- Logging discrepancies between front-end and back-end request counts.
- Requests containing both `Content-Length` and `Transfer-Encoding` headers (a major red flag — most legitimate clients never send both).
- Unexpected responses being delivered to the wrong client.
- WAF/proxy configuration: normalize or reject ambiguous requests, disable connection reuse to back-ends where possible.

---

## Sources
- attack.mitre.org
- cve.mitre.org
- PortSwigger Web Security Academy — HTTP request smuggling
- Cloudflare Learning Center — DNS spoofing, ARP poisoning
