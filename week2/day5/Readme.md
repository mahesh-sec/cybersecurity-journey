# Week 2 — Day 5: SOC Analyst Mindset & PCAP Anomaly Detection

## Summary

Today's focus shifted from learning individual protocols/attacks to thinking like a SOC analyst: establishing what *normal* traffic looks like for DNS, HTTP, ARP, and SMB, so deviations are recognizable without needing a signature for every possible attack.

## What was done

1. **Theory — SOC analyst mindset:** Studied DNS/HTTP/ARP/SMB baseline-vs-anomaly framework. Watched relevant sections (SOC Tools, Common Threats and Attacks) of TCM Security's free SOC 101 course on YouTube.
2. **PCAP anomaly spotting (cold, no hints):** Analyzed two real captures — a RARP request/reply pair, and an ARP storm capture. See [`pcap-analysis.md`](./pcap-analysis.md).
3. **Protocol mastery self-test:** Wrote out DNS resolution, TCP handshake, DHCP DORA, ARP poisoning, and TLS handshake from memory, then checked against ground truth. See [`protocol-self-test.md`](./protocol-self-test.md).
4. **Defensive detection rules:** Reviewed the Day 2 Protocol Attack Table and articulated the detection flag for each attack (ARP poisoning, DHCP starvation, HTTP smuggling, DNS spoofing), plus DNS tunneling which came up separately. See [`detection-rules.md`](./detection-rules.md).
5. **Wireshark filter practice:** Practiced filters live against the ARP storm capture, including debugging why `ip.addr` doesn't work on ARP traffic. See [`wireshark-cheatsheet.md`](./wireshark-cheatsheet.md).

## Key takeaways

- **Mechanism vs. anomaly are different questions.** Correctly explaining *what* a device is doing (e.g. a gateway serving multiple subnets) doesn't automatically surface *what's abnormal about how it's doing it* (volume, rate, response ratio). Both have to be checked explicitly.
- **Protocol context changes what "normal" looks like.** A pattern that's suspicious in one protocol (duplicate MAC claims in ARP) can be completely normal in a related one (RARP's request structure).
- **A zero-result filter can be informative, not just an error.** Before assuming a filter is wrong, check whether the absence of results is actually consistent with what's already known about the traffic.
- **Escalation should separate evidence from hypothesis.** State what's confirmed, name plausible causes without asserting one as fact, and recommend a specific next investigative step.
- **Recognition-level knowledge (this stage) vs. operational detection rules (later stage) are different bars.** Being able to state and explain a flag from memory is the current goal; precise filter syntax, threshold tuning, and MITRE/CAPEC mapping are reference material to build real fluency with once SIEM and detection-engineering content appears later in the roadmap.

## Files in this folder

- `pcap-analysis.md` — RARP and ARP storm capture analysis
- `protocol-self-test.md` — DNS, TCP, DHCP, ARP poisoning, TLS handshake recall + corrections
- `detection-rules.md` — Detection flags for ARP poisoning, DHCP starvation, HTTP smuggling, DNS spoofing, DNS tunneling
- `wireshark-cheatsheet.md` — Filters practiced today, including ARP-specific filter gotchas
