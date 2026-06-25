# Nmap Scripting Engine (NSE) — Deep Dive

**Date:** Week 2, Day 6
**Target:** Metasploitable2 (`192.168.56.101`)
**Tool:** `nmap` with NSE

---

## 1. Objective

Explore NSE script categories, run targeted scripts against Metasploitable2, and document what each script actually reveals — including correctly diagnosing a script that returns no result.

---

## 2. `nmap --script-help "http-*"`

Lists every NSE script whose name starts with `http-`. Output spans multiple categories, including:
- **Safe discovery** scripts (e.g. `http-title`) — passive information gathering, no exploitation attempted
- **Vulnerability discovery** scripts — check for the presence of a specific known flaw without exploiting it
- **Vulnerability exploit** scripts — go further than detection, actually triggering or confirming exploitability

This is the menu of available HTTP-recon scripts; not all need to be memorized, but recognizing the category distinction (safe/discovery vs. exploit) is the useful takeaway — it tells you, before running a script, roughly how invasive it is.

---

## 3. `nmap --script http-title 192.168.56.101 -p 80`

**Output:**
```
PORT   STATE SERVICE
80/tcp open  http
|_http-title: Metasploitable2 - Linux
```

**What it does:** Connects to the web server and extracts whatever is in the page's `<title>` HTML tag — a fast way to fingerprint what's running on a web port without opening a browser. Confirmed the title here is literally "Metasploitable2 - Linux."

**How to read script output:** The `|_` prefix is how Wireshark/Nmap denotes a single-line NSE script result attached to a specific port.

---

## 4. `nmap --script smb-vuln-ms17-010 -p 445 192.168.56.101`

**Output:**
```
PORT    STATE SERVICE
445/tcp open  microsoft-ds
```

No `smb-vuln-ms17-010` result line appeared — no VULNERABLE, no NOT VULNERABLE, nothing.

### Diagnosing the silent result

Re-ran with `--script-trace` to inspect the actual SMB negotiation Nmap performed. The trace showed:
- A full, clean SMB negotiation completed (NetBIOS query → SMB negotiate → NTLM session setup → tree connect to `IPC$` → named pipe open → clean close)
- No errors, no timeouts, no rejected connections
- The server identified itself explicitly during negotiation as:
  ```
  Unix Samba 3.0.20-Debian
  WORKGROUP
  ```

**Conclusion:** The script ran successfully and correctly determined that **MS17-010 (EternalBlue) does not apply to this target**, because MS17-010 is a vulnerability specific to Microsoft's own Windows SMB implementation — not Samba, which is a completely separate, Linux-native SMB/CIFS reimplementation with its own codebase. The script's silent (non-)output is the expected, correct behavior for a Windows-specific check run against a Samba target, not a sign of failure.

**Why this is still a useful result:** It correctly redirects attention to Samba-specific vulnerabilities instead — Metasploitable2's actual well-known SMB flaw is **CVE-2007-2447** (the Samba `username map script` command injection / unauthenticated RCE), which is the vulnerability this box is actually designed to demonstrate, documented separately in Day 4's `smb-enumeration.md`.

---

## 5. Summary Table

| Script | Result | Interpretation |
|---|---|---|
| `http-title` | `Metasploitable2 - Linux` | Confirmed working web service, fingerprinted page title |
| `smb-vuln-ms17-010` | No output (silent) | Correctly inapplicable — target is Samba 3.0.20-Debian, not Windows SMB |

---

## 6. Key Commands Reference

| Command | Purpose |
|---|---|
| `nmap --script-help "http-*"` | Lists all HTTP-related NSE scripts with descriptions |
| `nmap --script http-title -p 80 <IP>` | Extracts the web page title from the target |
| `nmap --script smb-vuln-ms17-010 -p 445 <IP>` | Checks specifically for the EternalBlue SMB vulnerability |
| `nmap --script <name> <IP> -v --script-trace` | Shows the raw protocol negotiation a script performs — useful for diagnosing silent/unexpected results |
