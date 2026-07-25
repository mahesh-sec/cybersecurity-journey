# TCP Port Scanner

A simple TCP connect scanner using Python's `socket` module.

## What it does
Attempts a TCP handshake against each port in a given list/range using `connect_ex()`, which returns an integer error code instead of raising an exception — `0` means the handshake succeeded (port open), any other value means it failed (closed/filtered).

## Usage
```bash
python port_scanmeta.py
```
Edit the `ip_addr` and `ports` arguments in the `__main__` block to target a different host or port range.

## Example Output
```
port 445 is open
```

## Security Concept
Demonstrates the TCP three-way handshake at the socket level. `connect_ex()` is preferred over `connect()` for scanning because it returns a status code instead of throwing an exception on failure, which keeps the scan loop simple across many ports.

## Known Limitation
This scanner only distinguishes "open" (handshake succeeded) vs. "closed" (immediate refusal). It does not currently distinguish a **filtered** port (firewall silently drops the packet, causing a timeout) from a genuinely **closed** port (active RST response) — both currently print as "closed." A future improvement would be to catch `socket.timeout` separately from `ConnectionRefusedError` and report "filtered" vs. "closed" accordingly, matching how tools like nmap classify port states.

Note: raw connect-based scanning also does not perform application-layer protocol negotiation. For protocols like SMB, which require the client to send a formatted request before the server responds, a plain `recv()` after connect will time out with no data — see `week4/smb-deep-enum.md` for the full explanation and correlation with `enum4linux`.
