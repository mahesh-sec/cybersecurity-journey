# APT29 (G0016): TTP Map

Week 6, Day 6 | Source: attack.mitre.org/groups/G0016 and its campaign pages (C0024 SolarWinds Compromise, C0023 Operation Ghost)

## Overview

| Field | Detail |
|---|---|
| Aliases | Cozy Bear, The Dukes, NOBELIUM, IRON RITUAL, IRON HEMLOCK, NobleBaron |
| Sponsor | Russian foreign intelligence (SVR) |
| Active since | 2008 |
| Targets | Government, diplomatic, think-tank and technology organisations, mainly in Europe, NATO countries and the US |
| Motivation | Espionage: long-term, quiet access. Does not aim to disrupt |
| Best-known campaign | SolarWinds Compromise (trojanized Orion update) |

## Summary

APT29 is a threat group attributed to Russian foreign intelligence (SVR) and active since 2008. It mainly targets European and NATO countries, and its most famous operation is the SolarWinds compromise. Its goal is espionage, so it avoids disruption and tries not to alert the victim.

It gets in through supply-chain compromise (the trojanized SolarWinds update), compromised identities used over VPN and Citrix, and password guessing or spraying against mailboxes. It hides where its logins come from by using residential proxies and Azure VMs.

Once inside, it escalates privileges (for example by exploiting CVE-2021-36934, using sticky keys, or giving admin rights to a newly created service principal) and abuses cloud features such as Azure Run Command and synced on-prem admin accounts to move into Office 365. It weakens defences by changing firewall rules and turning off audit logging.

It collects what it needs (emails, internal wikis), compresses it into password-protected archives, and sends it out over HTTPS so that it looks like normal web traffic. It has no Impact techniques mapped.

## Kill-chain table

| Tactic | ID | Technique | How APT29 uses it | Source |
|---|---|---|---|---|
| Resource Development | T1586.003 | Compromise Accounts: Cloud Accounts | Residential proxies and Azure VMs hide where logins into victim environments come from | G0016 |
| Initial Access | T1195.002 | Supply Chain Compromise: Compromise Software Supply Chain | Trojanized SolarWinds Orion update | C0024 |
| Initial Access | T1133 | External Remote Services | Compromised identities used to reach networks via VPN and Citrix | G0016 |
| Execution | T1651 | Cloud Administration Command | Azure Run Command and Azure AOBO used to run code on VMs | G0016 |
| Execution | T1218.005 | System Binary Proxy Execution: Mshta | Runs malicious scripts through the built-in mshta binary (MITRE files it under Defense Evasion) | G0016 |
| Persistence | T1037 | Boot or Logon Initialization Scripts | Hijacked application startup scripts so malware runs at startup | G0016 |
| Persistence | T1037.004 | Boot or Logon Initialization Scripts: RC Scripts | Installed a run command so malware runs at startup | G0016 |
| Persistence | T1547.001 | Boot or Logon Autostart Execution: Registry Run Keys / Startup Folder | Added Registry Run keys | G0016 |
| Persistence | T1078.003 | Valid Accounts: Local Accounts | Targets dormant accounts, such as those of people who have left | G0016 |
| Privilege Escalation | T1098.003 | Account Manipulation: Additional Cloud Roles | Gave company administrator rights to a newly created service principal | C0024 |
| Privilege Escalation | T1546.008 | Event Triggered Execution: Accessibility Features | Sticky keys for privileged console access without logging in | G0016 |
| Privilege Escalation | T1068 | Exploitation for Privilege Escalation | Exploited CVE-2021-36934 | G0016 |
| Defense Evasion | T1686 | Firewall rule modification | netsh firewall rules that limited certain outbound UDP packets | C0024 |
| Defense Evasion | T1685.001 | Audit log disabling | auditpol used to stop audit logs being collected | C0024 |
| Defense Evasion | T1685.002 | Cloud audit disabling | Disabled Purview Audit on targeted accounts before stealing M365 email | G0016 |
| Credential Access | T1110.001 | Brute Force: Password Guessing | Guessed passwords against a list of mailboxes | G0016 |
| Credential Access | T1110.003 | Brute Force: Password Spraying | Password spray attacks | G0016 |
| Discovery | T1083 | File and Directory Discovery | Read the Exchange virtual directory configuration with Get-WebServicesVirtualDirectory | C0024 |
| Discovery | T1680 | Local storage discovery | fsutil to check free disk space before actions that create large files | C0024 |
| Lateral Movement | T1021.001 | Remote Services: Remote Desktop Protocol | RDP from public-facing systems to internal servers | C0024 |
| Lateral Movement | T1021.002 | Remote Services: SMB/Windows Admin Shares | Admin accounts used to connect over SMB | C0024 |
| Lateral Movement | T1021.007 | Remote Services: Cloud Services | Synced on-prem privileged accounts used to move into Office 365 via Azure AD PowerShell | G0016 |
| Lateral Movement | T1078.002 | Valid Accounts: Domain Accounts | Stolen administrator credentials | C0023 |
| Collection | T1560.001 | Archive Collected Data: Archive via Utility | 7-Zip password-protected archives before exfiltration | C0024 |
| Collection | T1213 | Data from Information Repositories | Read internal wikis for sensitive business information | C0024 |
| Collection | T1114.002 | Email Collection: Remote Email Collection | Collected mail from Azure AD and Exchange, including via EWS | G0016 |
| Command and Control | T1071.001 | Application Layer Protocol: Web Protocols | HTTP used for C2 | C0024 |
| Command and Control | T1001.002 | Data Obfuscation: Steganography | Hid implant-to-C2 communications | C0023 |
| Exfiltration | T1071.001 | Application Layer Protocol: Web Protocols | Same technique, dual use: MITRE says HTTP was used for C2 and exfiltration | C0024 |
| Exfiltration | T1048.002 | Exfiltration Over Alternative Protocol: Asymmetric Encrypted Non-C2 | Simple HTTPS request to a password-protected archive staged on a victim OWA server | C0024 |
| Reconnaissance | none mapped | n/a | Nothing confirmed in my notes | n/a |
| Impact | none mapped | n/a | Espionage-focused group, so no destructive techniques | n/a |


## To verify on attack.mitre.org

- [ ] Official names for T1686, T1685.001, T1685.002 and T1680
- [ ] T1548 (UAC bypass), T1555.003 and T1595.002 were in my first list. Keep them only if they appear on G0016, and add their procedure text
- [ ] Check for spearphishing (T1566.001 / T1566.002) and any other Initial Access entries
- [ ] Confirm the tactic label shown on each technique page (several span two tactics)
