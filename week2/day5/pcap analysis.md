# Day 5 — PCAP Analysis: Spot the Anomaly

Two packet captures analyzed cold (no prior hints), applying baseline-vs-anomaly reasoning from the morning's SOC analyst mindset block.

---

## 1. `rarp_req_reply.pcapng` — RARP Request/Reply

**Initial read:** Flagged the matching sender/target MAC in the first packet as a possible sign of an attacker holding a device's MAC and requesting its IP for spoofing purposes.

**Actual finding:** This is RARP (Reverse ARP), EtherType `0x8035` — not standard ARP (`0x0806`). RARP solves the opposite problem from ARP: a device that knows its own MAC but has no IP yet asks the network to assign one. It's a legacy precursor to DHCP, used historically by diskless workstations/thin clients at boot.

**Packet breakdown:**

| Packet | Type | Sender MAC | Sender IP | Target MAC | Target IP |
|---|---|---|---|---|---|
| 1 | RARP Request (broadcast) | `00:0c:29:34:0b:de` | `0.0.0.0` | `00:0c:29:34:0b:de` | `0.0.0.0` |
| 2 | RARP Reply (unicast) | `00:0c:29:c5:f6:9b` | `10.1.1.10` | `00:0c:29:34:0b:de` | `10.1.1.100` |

**Why sender MAC = target MAC in Packet 1 (not an anomaly):** In a RARP request, the requesting device has no IP and is asking "what IP goes with this MAC?" There's no second device's MAC to reference at this point — the requester puts its own MAC in both fields because the only known data point is its own hardware address. This is RARP's normal request structure, not evidence of MAC spoofing.

**Verdict:** No anomaly. Two clean packets — a device requesting an IP assignment via RARP, and a RARP server answering it. Conceptually identical to a single DHCP Discover/Offer pair, just using an older protocol.

**Lesson:** The instinct to flag duplicate MAC fields is correct for *regular ARP* (where it indicates cache poisoning — multiple MACs claiming the same IP). Applied to RARP's normal request format, the same pattern is expected, not suspicious. Protocol context changes what "normal" looks like.

---

## 2. `220703_arp-storm__1_.pcapng` — ARP Storm

**Initial read:** A single router/gateway sending ARP requests to multiple devices across what looked like several subnets, with the sender IP changing because the device serves multiple networks.

**Actual finding:** That mechanism description was correct — but it missed the actual anomaly the capture is named for.

**Capture stats (parsed via scapy):**
- Total ARP packets: **622**
- Capture duration: **~29 seconds**
- Opcode breakdown: **622 Requests, 0 Replies**
- Distinct sender MAC: **1** (`00:07:0d:af:f4:54`) — same physical device throughout
- Distinct sender IPs (gateway identities used): **9**, e.g. `24.166.172.1` (292 requests), `69.76.216.1` (205 requests), `65.26.92.1` (47 requests)
- Distinct target IPs queried: **303**
- Address ranges are public/ISP-style (`24.x`, `65.x`, `69.x`), not private LAN ranges — consistent with an ISP-side access router/CMTS serving multiple subscriber subnets, each with its own gateway IP ending in `.1`

**Corrected mechanism (confirmed accurate):** One physical device (one MAC) acts as the gateway for several different subnets. It already holds a valid IP on each subnet it serves (the `.1` addresses) — it is not requesting an IP for itself. For each subnet, it sends ARP requests under that subnet's gateway identity, asking "who has this target IP, send me your MAC." The sender IP changes per packet because the device switches which subnet-identity it's acting under; the MAC stays constant because it's the same physical hardware throughout.

**The actual anomaly — volume and reply ratio, not the multi-subnet logic:**
- 622 requests in 29 seconds, across 303 distinct targets, is far beyond what normal "resolve a MAC when there's traffic to send" behavior looks like.
- **Zero replies returned** to any of the 622 requests — a healthy network would show at least some hosts answering.
- This combination (high volume + zero response) is what justifies the file being named an "ARP storm" and is what a SOC analyst would actually alert on, independent of knowing the root cause yet.

**Possible causes (not yet confirmed, listed for investigation):**
- Device misconfiguration / ARP table rebuild after an outage (re-resolving its entire subscriber range at once)
- Switching loop or broadcast storm amplifying ARP traffic
- Compromise or abuse of the gateway device, sweeping its IP range
- Targets may simply be offline/unreachable, explaining the zero replies independent of the sweep's cause

**Escalation note (refined):**
> Observed 622 ARP requests in ~29 seconds from MAC `00:07:0d:af:f4:54`, sweeping 303 distinct target IPs across at least 9 subnets it appears to gateway for. Zero ARP replies were captured in response. This volume and sweep pattern is anomalous for normal gateway behavior. Possible causes include device misconfiguration (e.g. ARP table rebuild after an outage) or compromise/abuse of the device. Recommend checking device logs and recent config changes before concluding root cause.

**Lesson:** Mechanism (what the device is doing and why) and anomaly (what's statistically abnormal about how it's doing it) are separate questions. Getting the mechanism right doesn't automatically surface the anomaly — volume, rate, and response ratio have to be checked explicitly. When escalating, separate confirmed evidence from hypothesis, and recommend an investigative next step rather than asserting a root cause.
