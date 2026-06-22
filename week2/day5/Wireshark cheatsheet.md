# Day 5 — Wireshark Display Filter Cheatsheet

Filters practiced today, organized by use case. Includes notes on mistakes made while practicing, since the mistakes were as instructive as the correct filters.

---

## General IP / TCP

| Filter | Purpose |
|---|---|
| `ip.addr == x.x.x.x` | All traffic to/from a specific IP, either direction. **Only works for packets with an actual IP layer** (TCP/UDP/ICMP etc.) |
| `tcp.port == 80` | Traffic on a specific port, regardless of source/destination |

## HTTP

| Filter | Purpose |
|---|---|
| `http.request.method == "POST"` | Isolate POST requests — useful for spotting login/data-submission attempts |
| `frame contains "password"` | Raw string search across the entire frame — catches plaintext credentials anywhere in the packet |

## DNS

| Filter | Purpose |
|---|---|
| `dns.qry.name contains "google"` | Filter DNS queries containing a substring — useful for hunting specific domains |

## ARP

| Filter | Purpose |
|---|---|
| `arp.opcode == 2` | Show only ARP **replies** (opcode 1 = request, 2 = reply) |
| `arp.opcode == 1` | Show only ARP **requests** |
| `arp.src.proto_ipv4 == x.x.x.x` | Show ARP packets where x.x.x.x is the **sender** IP |
| `arp.dst.proto_ipv4 == x.x.x.x` | Show ARP packets where x.x.x.x is the **target** IP being asked about |
| `arp.src.proto_ipv4 == x.x.x.x \|\| arp.dst.proto_ipv4 == x.x.x.x` | Show ARP packets where x.x.x.x appears in either role |
| `arp.opcode == 1 && ip.src == x.x.x.x` | Combo filter example: requests AND a specific IP condition |

### Important gotcha learned today: `ip.addr` does not work on ARP packets

ARP operates directly over Ethernet and has no IP layer — the IP addresses inside an ARP packet (sender/target) are just data fields in the ARP payload, not part of a real IP header. Wireshark's `ip.addr` filter only matches packets that have an actual dissected IP layer, so it silently returns zero results on pure ARP traffic.

**Fix:** use the `arp.*` namespace specifically — `arp.src.proto_ipv4` and `arp.dst.proto_ipv4` — instead of `ip.addr`, when filtering ARP traffic.

### Second gotcha: `arp.src` vs `arp.dst` are not interchangeable, and a zero-result filter can itself be meaningful

Tested `arp.dst.proto_ipv4 == 24.166.172.1` against the ARP storm capture and got zero results. This wasn't a mistake — it confirmed that this IP only ever appeared as a **sender** (asking about other IPs), never as a **target** (being asked about) anywhere in that capture, consistent with it being a gateway address that sweeps outward rather than one other devices query. Lesson: a filter returning nothing isn't automatically a sign of a wrong filter — check whether zero actually makes sense given what's already known about the traffic before assuming an error.

---

## Workflow note

When investigating ARP-heavy captures: start broad (`arp.opcode == 1` or `== 2` to separate requests/replies), then narrow with `arp.src.proto_ipv4` / `arp.dst.proto_ipv4` to isolate a specific address's role, then combine conditions with `&&` once a specific hypothesis needs testing (e.g. "how many requests did this one gateway identity send").
