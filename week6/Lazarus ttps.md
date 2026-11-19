# Lazarus Group (G0032): TTP Map

Week 6, Day 6 | Source: attack.mitre.org/groups/G0032 and its campaign pages (C0022 Operation Dream Job)

## Overview

| Field | Detail |
|---|---|
| Sponsor | North Korea, attributed to the Reconnaissance General Bureau (RGB) |
| Active since | At least 2009 |
| Targets | Finance, cryptocurrency, defense, and other sectors |
| Motivation | Espionage, financial gain and destructive attacks |
| Best-known attack | Destructive wiper attack on Sony Pictures |
| Related campaigns | Operation Flame, Operation 1Mission, Operation Troy / DarkSeoul |

## Summary

Lazarus Group is a North Korean state-sponsored group attributed to the Reconnaissance General Bureau and active since at least 2009. It is responsible for the destructive wiper attack on Sony Pictures, and its malware is linked to other campaigns such as Operation Flame, Operation 1Mission and DarkSeoul. Its motives are espionage, financial gain and destruction.

It gets in with spearphishing emails that carry malicious Word documents or links. It runs code with PowerShell and cmd.exe, and one variant uses a batch file to delete its own binaries so it leaves less evidence. It stays on the system after a reboot by placing malicious code or a shortcut in the Startup folder or adding a Registry Run key.

It weakens defences by using netsh to change or disable the Windows firewall, terminating McAfee-related processes (TangoDelta), and disabling the System Event Notification and Alerter services (SHARPKNOT). It builds C2 on legitimate domains it has compromised in other countries.

Inside the network it queries Active Directory for employee and admin lists, reports window titles to C2, compresses collected data (RAR, encrypted zip), and sends it out over its C2 channel (HTTP/HTTPS) or by email. At the end it destroys evidence and data, overwriting files and wiping disk structures, and has defaced systems with a threatening wallpaper. This gives it the biggest Impact footprint of the three groups.

## Kill-chain table

| Tactic | ID | Technique | How Lazarus uses it | Source |
|---|---|---|---|---|
| Resource Development | T1584.001 | Compromise Infrastructure: Domains | Compromised domains in Italy and other countries for C2 | C0022 |
| Initial Access | T1566.001 | Phishing: Spearphishing Attachment | Emails with malicious Word documents | G0032 |
| Initial Access | T1566.002 | Phishing: Spearphishing Link | Emails with malicious links | G0032 |
| Execution | T1059.001 | Command and Scripting Interpreter: PowerShell | Runs commands and malicious code | G0032 |
| Execution | T1059.003 | Command and Scripting Interpreter: Windows Command Shell | cmd.exe to run commands; a batch file deletes the malware's own binaries | G0032 |
| Persistence | T1547.001 | Boot or Logon Autostart Execution: Registry Run Keys / Startup Folder | Malicious code in the startup folder or a Run key | G0032 |
| Persistence | T1547.009 | Boot or Logon Autostart Execution: Shortcut Modification | LNK shortcut in the user's Startup folder | G0032 |
| Defense Evasion | T1055.001 | Process Injection: DLL Injection | Reflective DLL injection in a malware sample | G0032 |
| Defense Evasion | T1686.003 | Firewall modification | netsh used to open incoming connections or disable the Windows firewall | G0032 |
| Defense Evasion | T1685 | Disabling security tools | TangoDelta kills McAfee processes; SHARPKNOT disables the System Event Notification and Alerter services | G0032 |
| Credential Access | T1110.003 | Brute Force: Password Spraying | Generated Administrator-style usernames and weak passwords against Windows shares (used for lateral movement) | G0032 |
| Discovery | T1087.002 | Account Discovery: Domain Account | Queried AD servers for the employee and admin list | C0022 |
| Discovery | T1010 | Application Window Discovery | IndiaIndia sends window titles of running processes to C2; KilaAlfa keylogger reports the foreground window title | G0032 |
| Lateral Movement | T1078 | Valid Accounts | Used administrator credentials to reach restricted network segments | G0032 |
| Lateral Movement | T1021.001 | Remote Services: Remote Desktop Protocol | SierraCharlie malware spreads over RDP | G0032 |
| Lateral Movement | T1534 | Internal Spearphishing | Phished from inside an already-compromised organisation | C0022 |
| Collection | T1005 | Data from Local System | Collected data and files from compromised networks | G0032 |
| Collection | T1560 | Archive Collected Data | RAR, plus RomeoDelta zipping, encrypting and uploading directories | G0032 |
| Command and Control | T1071.001 | Application Layer Protocol: Web Protocols | C2 over HTTP and HTTPS | G0032 |
| Exfiltration | T1041 | Exfiltration Over C2 Channel | Sends data and files out through its C2 channel | G0032 |
| Exfiltration | T1048.003 | Exfiltration Over Alternative Protocol: Unencrypted Non-C2 | SierraBravo-Two emails victim information over SMTP | G0032 |
| Impact | T1485 | Data Destruction | Custom secure-delete function overwrites file contents | G0032 |
| Impact | T1491.001 | Defacement: Internal Defacement | Replaced wallpaper with a threatening image after wiping the disk structure | G0032 |
| Reconnaissance | none mapped | n/a | Nothing confirmed in my notes | n/a |
| Privilege Escalation | none mapped | n/a | Nothing confirmed in my notes | n/a |


## To verify on attack.mitre.org

- [ ] Official names for T1686.003 and T1685
- [ ] Disk Structure Wipe (the T1491.001 text mentions it). Look it up and add it under Impact
- [ ] Supply-chain compromise was in my theory notes as a Lazarus signature. Add the ID if it is on G0032
- [ ] Tactic label for T1078 (it spans several tactics) and T1110.003 (listed under Credential Access)
- [ ] Fill or confirm the empty rows (Reconnaissance, Privilege Escalation)
