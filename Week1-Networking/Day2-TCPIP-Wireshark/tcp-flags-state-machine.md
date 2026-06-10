# TCP Flags & State Machine — Deep Dive

## TCP Flags

Every TCP packet carries flags in its header. Each flag is 1 bit — either ON or OFF.

| Flag | Full Name | Meaning | When you see it |
|------|-----------|---------|-----------------|
| SYN | Synchronise | "I want to start a connection" | First packet of every TCP connection |
| ACK | Acknowledgement | "I received your data" | Almost every packet after the first SYN |
| FIN | Finish | "I want to close the connection" | End of connection — graceful close |
| RST | Reset | "Something went wrong — abort" | Error, port closed, or forced disconnect |
| PSH | Push | "Send this data to app immediately" | When app needs data right away, no buffering |
| URG | Urgent | "This data is urgent, process first" | Rare — almost never seen in modern traffic |

---

## TCP 3-Way Handshake (Open)
---

## TCP Connection Close (4-Way)
> Why 4 steps to close but 3 to open?
> Because each side closes independently — server may still have data to send after client is done.

---

## TCP RST — Abrupt Close
RST also appears when:
- A firewall blocks a connection
- One side crashes mid-connection
- An attacker sends a forged RST to kill a connection (RST Attack)

---

## TCP State Machine
---

## Wireshark Filters for Each Flag

| To find | Wireshark filter |
|---------|-----------------|
| SYN packets only | `tcp.flags.syn==1 && tcp.flags.ack==0` |
| SYN-ACK packets | `tcp.flags.syn==1 && tcp.flags.ack==1` |
| FIN packets | `tcp.flags.fin==1` |
| RST packets | `tcp.flags.reset==1` |
| Full handshake | `tcp.flags.syn==1` |
| PSH packets | `tcp.flags.push==1` |

---

## Key Observations from YouTube Capture
- Every new connection to YouTube started with **SYN → SYN-ACK → ACK**
- After handshake, **QUIC took over** — TCP was only used for the initial setup
- **ACK flag** was on almost every packet after the handshake
- No **RST** packets observed — clean connections throughout
