# Week 6, Day 6: Threat Actor Deep Dive Notes

Groups covered: APT29 (G0016), Lazarus Group (G0032), FIN7 (G0046)

## Concepts

- **Tactic** is the goal (for example Persistence). **Technique** is how the goal is reached (T1547.001). **Procedure** is what a specific group actually did, shown in the "procedure examples" on each technique page.
- A technique's tactic label comes from where MITRE files it, not from what the group used it for. Mshta (T1218.005) is Defense Evasion even though APT29 used it to execute scripts.
- Some techniques span several tactics (Valid Accounts, External Remote Services, Boot or Logon Initialization Scripts). Pick one and note the other.
- Dual use: T1071.001 appears under both C2 and Exfiltration for APT29 because MITRE's procedure text says HTTP was used for both. MITRE itself files the technique under Command and Control only.
- Sources differ: some entries come from the group page (G####) and some from campaign pages such as SolarWinds (C0024), Operation Ghost (C0023) and Operation Dream Job (C0022). Keep a Source column.
- A newer ATT&CK ID (T1685, T1686, T1680) is still a real technique. Copy its official name from the page.

## Interview talking points

- Motive drives technique choice: espionage means stealth, destruction means loud and thorough, profit means speed and volume.
- Impact is the clearest split: none for APT29, wipers and defacement for Lazarus, ransomware for FIN7.
- The same matrix produces different detection priorities per actor. Examples: audit-log tampering for APT29, mass file deletion for Lazarus, Kerberoasting and ransomware precursors for FIN7.

## Corrections log (my first drafts vs. the sources)

| Where | I first wrote | Corrected to |
|---|---|---|
| APT29 | UAC bypass as initial access | Initial access was supply chain, compromised identities over VPN/Citrix and password spraying. UAC bypass (T1548) is not a confirmed entry yet |
| APT29 | T1586.003 under Initial Access | Resource Development |
| APT29 | T1218.005 under Execution | Defense Evasion per MITRE (note the Execution use) |
| APT29 | Discovery was T1595.002 | T1595.002 is Reconnaissance. Real Discovery entries are T1083 and T1680 |
| APT29 | "Discover weak points in cloud accounts" | Not in sources. Use Azure Run Command, synced on-prem admins into Office 365, password spraying |
| Lazarus | Batch file "destroys binaries" | Deletes its own binaries to remove evidence |
| Lazarus | Changed the Windows Defender alert system | SHARPKNOT disables the System Event Notification and Alerter services; TangoDelta kills McAfee processes |
| Lazarus | Sends Windows user account data to C2 | IndiaIndia sends window titles; during Operation Dream Job it queried AD for the employee and admin list |
| Lazarus | "mcafe" and "Lazar" | McAfee, Lazarus Group |
| FIN7 | Data sent via MEGA and DNS | DNS is C2 (and backup C2). Exfiltration is to MEGA |
| FIN7 | Images and videos | Screenshots and desktop video recordings (T1113) |
| FIN7 | Ransomware described mid-summary | Ransomware is the last stage |
| FIN7 | Missing techniques | Added Exchange exploitation, Kerberoasting, ZeroLogon and RDP |
