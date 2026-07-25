# SMB Deep Enumeration — Metasploitable (192.168.56.101)

## Objective
Go beyond the basic SMB scan from Week 2 using `enum4linux` and correlate findings with a custom Python port scanner, to understand what dedicated enumeration tools reveal that a raw port scan cannot.

## Tools Used
- `enum4linux` v0.9.1
- `smbmap` v1.10.7 (attempted — see limitations)
- Custom Python TCP port scanner (`port_scanmeta.py`)

## Command
```
enum4linux -U -S -G -r -o -n -i 192.168.56.101
```

## Key Finding: Anonymous / Null Session Access Enabled

```
[+] Server 192.168.56.101 allows sessions using username '', password ''
```

This single misconfiguration is the root cause of everything below — it allows an unauthenticated attacker to pull the full user list, enumerate groups, walk the RID space, and list at least one share, all without valid credentials.

## Users Enumerated (Direct + RID Cycling)

`enum4linux` returned 35 accounts via direct SAM enumeration, including standard Linux system accounts (`root`, `daemon`, `www-data`, `mysql`, `postgres`, `sshd`, etc.) mapped into the Samba/NT-style user database. Notably, `msfadmin` (RID `0xbb8` / 3000 decimal) stands out as a non-system, human-created account — a strong candidate for the intended entry point into this box.

RID cycling (RID range 500–550, 1000–1050) against domain SID `S-1-5-21-1042354039-2475377354-766472396` confirmed the same accounts and additionally revealed group RIDs (Domain Admins, Domain Users, Domain Guests, and per-user primary groups following the Unix UID=GID convention).

## Share Enumeration

| Share    | Type | Anonymous Mapping | Listing |
|----------|------|--------------------|---------|
| print$   | Disk | DENIED             | N/A     |
| tmp      | Disk | **OK**             | **OK**  |
| opt      | Disk | DENIED             | N/A     |
| IPC$     | IPC  | N/A                | N/A     |
| ADMIN$   | IPC  | DENIED             | N/A     |

**Finding:** the `tmp` share is fully browsable with a null session — no credentials required. This is the concrete evidence to cite for the "anonymous access enabled" finding in a report (Scope/Findings/Remediation format).

## OS Fingerprint
Samba 3.0.20-Debian — a legacy version with well-documented CVEs (including a known backdoor vulnerability in this exact version), consistent with Metasploitable's intentionally vulnerable design.

## Correlation with Custom Python Port Scanner

```
python port_scanmeta.py
port 445 is open
```

The custom TCP scanner confirmed port 445 is open via a raw `connect_ex()` handshake, but a generic banner-grab (`recv()` immediately after connect) returns nothing and times out. This is expected: SMB is a **request-response protocol**, not a "server greets first" protocol like SSH or FTP — the client must send a properly formatted SMB2 Negotiate Protocol Request before the server responds. A raw socket script proves the port is open; it can't easily replicate the SMB protocol handshake itself. This is exactly the value dedicated tools like `enum4linux` (and `impacket`/`smbmap` underneath) add — they already speak the SMB protocol.

**Takeaway:** a lightweight custom scanner is useful for fast open/closed triage across many ports; purpose-built enumeration tools are necessary once you need actual protocol-level interaction.

## Limitations / Known Issues

`smbmap` failed on this system with `MaybeEncodingError` from Python's `multiprocessing` module — a known compatibility bug between `smbmap 1.10.7` and Python 3.13 (the `SMBConnection` object contains a local lambda that cannot be pickled across worker processes). This is an environment/tooling issue, not a target-side failure. `enum4linux`'s built-in share mapping (Mapping/Listing/Writing columns) was used as the primary source for share permission data instead.

## Comparison: Week 2 Basic Scan vs. Today's Deep Enumeration

| | Week 2 (basic scan) | Week 4 Day 6 (deep enumeration) |
|---|---|---|
| Port 445 status | Open | Open (confirmed independently) |
| Service version | Not captured | Samba 3.0.20-Debian |
| User accounts | None | 35 accounts, incl. `msfadmin` |
| Groups / RIDs | None | Domain Admins/Users/Guests + per-user groups |
| Share list | None | 5 shares identified |
| Share permissions | None | `tmp` anonymously readable |
| Root cause identified | No | Yes — null sessions enabled |
