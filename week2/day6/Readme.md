# Week 2 — Day 6: Consolidation + Advanced PCAP Lab

## Summary

Today combined a cold PCAP analysis challenge with three hands-on consolidation blocks: SQL injection across DVWA's three security levels, an Nmap Scripting Engine deep dive, and an internal-vs-external verification pass against Metasploitable2 using SSH, `ps aux`, and `netstat -tulnp`.

## What was done

1. **Advanced PCAP challenge (cold, no hints):** Analyzed two unfamiliar captures — a deliberately malformed DHCP Discover packet (`PRIV_bootp-both_overload_empty-no_end.pcap`) showing sname/file option overload with three distinct missing-End-option errors, and a real-world HTTP trace (`tcp-ethereal-file1.trace`) showing a 152,372-byte file upload reassembled across 132 TCP segments via plaintext multipart/form-data POST.
2. **DVWA SQL injection across all three security levels.** See [`sql-injection-dvwa.md`](./sql-injection-dvwa.md).
3. **Nmap Scripting Engine (NSE) deep dive.** See [`nmap-nse-deep-dive.md`](./nmap-nse-deep-dive.md).
4. **Internal vs. external service verification.** See [`internal-vs-external-verification.md`](./internal-vs-external-verification.md).
5. **Week 2 Summary README** — consolidated tools, PCAPs, and concepts across all of Week 2. See [`../README.md`](../README.md).

## Key takeaways

- **The same payload produces three different outcomes depending on the defense layer**, not three different attacks: Low (no defense) lets `' OR '1'='1` become live SQL logic and dumps the table; Medium (blind character escaping) defuses the breakout but produces a revealing SQL syntax error instead; High (parameterized queries) never lets input enter the query structure at all, so the same input just fails to match anything.
- **A script returning no output isn't automatically a failure.** `smb-vuln-ms17-010` produced no result against Metasploitable2 — tracing the actual SMB negotiation confirmed the script ran correctly and determined the check simply doesn't apply, since the target runs Samba, not Windows SMB. Verifying *why* something is silent matters as much as verifying why something fires.
- **External port scans and internal process inspection answer different questions.** Nmap shows what's reachable and guesses the service; `ps aux`/`netstat -tulnp` from inside confirm the exact binary, its privilege level, and surface services (an unrestricted `distccd` listener, a root-owned Ruby DRb server) that aren't fully visible or interpretable from the outside alone.
- **`ps aux` and `netstat -tulnp` answer different questions too** — all running processes vs. only processes with an open listening socket — and the `-l` flag specifically is what narrows `netstat` to listeners only.

## Files in this folder

- `sql-injection-dvwa.md` — DVWA SQL injection demonstrated and explained at Low/Medium/High security
- `nmap-nse-deep-dive.md` — NSE script categories, `http-title`, and diagnosing the silent `smb-vuln-ms17-010` result
- `internal-vs-external-verification.md` — `/etc/passwd` structure, `ps aux` vs `netstat -tulnp`, and the full port-to-process comparison
