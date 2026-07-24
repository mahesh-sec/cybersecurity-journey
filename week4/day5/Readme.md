# Banner Grabber

A simple Python CLI tool that connects to one or more TCP ports on a target host and grabs whatever service banner is returned — the same underlying technique Nmap's `-sV` flag uses to identify service versions, just built from raw sockets with no external libraries.

## What it does

For each port passed in:
1. Opens a TCP socket (`AF_INET`, `SOCK_STREAM`) to the target.
2. For port 80, sends a minimal `HEAD / HTTP/1.0` request first, since HTTP servers don't banner unprompted (unlike SSH, FTP, and SMTP, which greet immediately on connect).
3. Reads back whatever the service sends (`recv`) and prints it.
4. Handles closed/unresponsive ports gracefully instead of crashing the whole scan.

## Usage

```bash
python banner_grabcli.py -ip <target_ip> -p <port1> <port2> ... -t <timeout_seconds>
```

Example:
```bash
python banner_grabcli.py -ip 192.168.56.101 -p 21 22 25 53 80 111 139 445 3306 -t 4
```

Arguments:
- `-ip` (required) — target IP address
- `-p` (required) — one or more ports, space-separated
- `-t` / `--timeout` (optional, default `3`) — socket timeout in seconds

## Sample output (against Metasploitable2)

```
The port 21 is open on ip 192.168.56.101 and version of the service running on that port is 220 (vsFTPd 2.3.4)
The port 22 is open on ip 192.168.56.101 and version of the service running on that port is SSH-2.0-OpenSSH_4.7p1 Debian-8ubuntu1
The port 25 is open on ip 192.168.56.101 and version of the service running on that port is 220 metasploitable.localdomain ESMTP Postfix (Ubuntu)
port 53 : no response or closed timed out
The port 80 is open on ip 192.168.56.101 and version of the service running on that port is HTTP/1.1 200 OK
Server: Apache/2.2.8 (Ubuntu) DAV/2
X-Powered-By: PHP/5.2.4-2ubuntu5.10
port 111 : no response or closed timed out
port 139 : no response or closed timed out
port 445 : no response or closed timed out
The port 3306 is open on ip 192.168.56.101 and version of the service running on that port is 5.0.51a-3ubuntu5
```

## CVE cross-reference

Banners grabbed above were cross-referenced against known CVEs for those exact service versions.

| Service | Version | CVE | Notes |
|---|---|---|---|
| vsftpd | 2.3.4 | CVE-2011-2523 | Backdoor deliberately planted in the distributed source; triggered via a crafted username on port 21, opens a shell on port 6200. |
| OpenSSH | 4.7p1 Debian-8ubuntu1 | No CVE record found for this exact build | Very old (2007-era) release; worth deeper manual research if needed. |
| Apache | 2.2.8 | CVE-2008-0005, CVE-2007-6388, CVE-2007-6420/6421/6422, CVE-2008-2364, CVE-2007-5000, CVE-2008-0455/0456 | Range of issues across `mod_proxy_balancer` (CSRF/XSS/DoS), `mod_proxy_http` (DoS), `mod_imagemap` (XSS), and `mod_negotiation` (CRLF injection/XSS). |
| PHP | 5.2.4-2ubuntu5.10 | CVE-2007-4850 | libcurl integration in PHP 5.2.4/5.2.5 allows `safe_mode`/`open_basedir` bypass and arbitrary file read via a `file://` request containing a null-byte sequence. |
| MySQL | 5.0.51a-3ubuntu5 | CVE-2008-4097 | Local privilege-check bypass via `CREATE TABLE` with symlinked `DATA DIRECTORY`/`INDEX DIRECTORY` arguments; incomplete fix for CVE-2008-2079. |

## Known limitations

- Ports 111, 139, and 445 return no banner with this tool — these services (RPC, NetBIOS, SMB) require a protocol-specific handshake packet before responding, rather than sending an unprompted banner like SSH/FTP/SMTP. A single generic `connect + recv` isn't enough to fingerprint them; that would need protocol-aware probes (e.g. what `enum4linux`/`smbmap` do for SMB).
- Port 53 (DNS) is UDP by default, so a `SOCK_STREAM` (TCP) connection attempt correctly finds nothing.
- MySQL's raw response includes a binary auth-negotiation salt after the version string, which prints as garbled text when decoded as UTF-8 — this is expected, not a bug.
