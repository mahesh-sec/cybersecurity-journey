# Service Banner Grabber

## What It Does
Connects to one or more TCP ports on a target host and grabs the service banner returned by whatever is listening — the raw text many services send back on connection (or in response to an HTTP HEAD request on port 80), which often reveals the software name and version running on that port.

## How It Works
- Opens a raw TCP socket to each requested port with a configurable timeout.
- If the port is 80, it sends a minimal `HEAD / HTTP/1.0` request to prompt an HTTP response (many services respond on connect alone; HTTP servers need a nudge).
- Reads up to 1024 bytes back and decodes it as the banner; connection errors (timeout / refused) are caught and reported per-port instead of crashing the whole scan.

## Usage
```bash
python banner_grabber.py -ip <target_ip> -p <port1> <port2> ... [-t <timeout>]
```

| Flag | Description | Default |
|---|---|---|
| `-ip` | Target IP address (required) | — |
| `-p` | One or more ports to check, space-separated (required) | — |
| `-t`, `--timeout` | Socket timeout in seconds | `3` |

**Example:**
```bash
python banner_grabber.py -ip 192.168.56.101 -p 21 22 80 -t 3
```

## Example Output
```
The port 21 is open on ip 192.168.56.101 and version of the service running on that port is 220 (vsFTPd 2.3.4)
The port 22 is open on ip 192.168.56.101 and version of the service running on that port is SSH-2.0-OpenSSH_4.7p1 Debian-8ubuntu1
port 80 : no response or closed timed out
```

## Security Concept
This is **service/version enumeration**, the step that follows port scanning in a real reconnaissance workflow. Knowing a port is open (from the port scanner) tells you *what's reachable*; grabbing the banner tells you *what's actually running* — which is what lets an analyst or pentester cross-reference a specific software version against known CVEs. This is the same principle behind Nmap's `-sV` service detection and is a core building block of vulnerability assessment.

## Possible Improvements
- Some services (e.g. Metasploitable2's vsFTPd 2.3.4) are intentionally vulnerable — pairing this tool's output with a quick CVE lookup would turn it into a mini vulnerability-scanning demo.
- Currently only port 80 gets an active probe; other common ports (e.g. 21 FTP, 22 SSH) rely on the service banner on connect, which not all services send — could add protocol-specific probes for more services.
