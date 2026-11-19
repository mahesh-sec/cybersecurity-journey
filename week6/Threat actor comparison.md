# APT29 vs Lazarus vs FIN7: Comparison

Week 6, Day 6 | Based on my kill-chain tables for each group (see `apt29-ttps.md`, `lazarus-ttps.md`, `fin7-ttps.md`)

## Side by side

| | APT29 | Lazarus Group | FIN7 |
|---|---|---|---|
| Motivation | Espionage | Espionage, financial gain, destruction | Financial gain |
| Sponsor | Russian SVR | North Korea (RGB) | Criminal group |
| Active since | 2008 | At least 2009 | 2013 |
| Initial access | Supply chain, compromised identities over VPN/Citrix, password spraying | Spearphishing attachments and links | Exploiting public-facing apps, spearphishing, malicious USB keyboards |
| Signature move | Cloud identity abuse | Wipers and defacement | Ransomware and fast domain takeover |
| Defense evasion | Firewall rules, audit logging disabled (including cloud audit) | Firewall changes, killing security tools, deleting its own binaries | Firewall rules |
| C2 | HTTP, steganography | HTTP/HTTPS over compromised legitimate domains | DNS, with DNS as backup |
| Exfiltration | HTTPS (same channel as C2) to a staged archive | Own C2 channel, SMTP | MEGA cloud storage |
| Impact | None mapped | Data destruction, defacement | Ransomware |

## Comparison paragraph

APT29 wants long-term access, so it avoids noise. It abuses identities and cloud services, turns off audit logs, and sends data out over normal-looking HTTPS, and it has no Impact techniques. Lazarus has several motives, including destruction, so it is willing to be loud: it wipes disks, defaces systems, kills security tools and deletes its own binaries to remove evidence. FIN7 wants money quickly, so it relies on speed and volume: it exploits public-facing applications, takes over domains with Kerberoasting and ZeroLogon, uses DNS and MEGA for quick channels, and ends with ransomware. The same ATT&CK matrix therefore gives different detection priorities for each group.

## What this means for a SOC analyst

| Group | Watch for |
|---|---|
| APT29 | New service principals and role grants, password spraying against mailboxes, audit-log changes (auditpol, Purview), unusual mailbox access (EWS), logins from residential proxy or Azure IP ranges |
| Lazarus | netsh firewall changes, security tools being killed, LNK files or Run keys in startup locations, mass file overwrites or disk wipes, new domains used for C2 |
| FIN7 | Exchange exploitation, Kerberoasting (many service-ticket requests), ZeroLogon attempts, new Windows services, DNS TXT/OPT query anomalies, uploads to MEGA, ransomware precursors |
