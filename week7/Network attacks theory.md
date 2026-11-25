# Week 7, Day 3: Network Attacks (Security+ SY0-701, Objective 2.4)

Source: Professor Messer SY0-701 videos (Denial of Service, DNS Attacks, On-path Attacks, Application Attacks).

## On-path attack (formerly man-in-the-middle)
- Attacker sits between two parties to intercept, read or modify traffic.
- Common methods: ARP poisoning, rogue access point, SSL stripping (HTTPS downgraded to HTTP).
- Indicators: unexpected certificate warnings, multiple MAC addresses for one IP, changed ARP/DNS tables, unusual latency.
- Mitigations: TLS validation, VPN, dynamic ARP inspection, secure protocols.

## Replay attack / credential replay
- Attacker captures valid data (a login, a token, a request) and resends it later.
- Credential replay: captured authentication data is reused to impersonate the user.
- Often follows an on-path attack.
- Mitigations: nonces, timestamps, short-lived session tokens, MFA.

## DoS / DDoS
- DoS: overwhelm a service so it becomes unavailable. DDoS: same, from many systems at once.
- Volume-based: UDP / ICMP floods. Protocol-based: SYN flood. Application-layer: valid-looking requests at huge scale.
- Amplified: a small request triggers a large response (e.g. DNS amplification).
- Reflected: spoofed source IP makes responses go to the victim.
- Indicators: sudden traffic spike, legitimate users cannot connect, many source IPs.
- Mitigations: rate limiting, CDN / upstream scrubbing, autoscaling.

## DNS attacks
- DNS poisoning (cache poisoning): false records inserted into a resolver's cache so a correct name returns a malicious IP.
- Can happen through an on-path attack or by directly poisoning the cache.
- Related: domain hijacking, typosquatting (tricks the user before resolution).
- Mitigation: DNSSEC, trusted resolvers.

## Quick comparison
| Attack | What breaks | Impact (CIA) |
|---|---|---|
| On-path | Trust between two parties | Confidentiality, Integrity |
| Replay | Freshness of valid data | Authentication / Integrity |
| DDoS | Service capacity | Availability |
| DNS poisoning | Name resolution | Integrity, Confidentiality |

## Anki cards made
- What is the difference between DoS and DDoS?
- Amplified vs reflected DDoS?
- How does DNS cache poisoning work?
- Why is credential replay often paired with an on-path attack?
- Name three indicators of an on-path attack.
