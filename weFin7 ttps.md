# FIN7 (G0046): TTP Map

Week 6, Day 6 | Source: attack.mitre.org/groups/G0046

## Overview

| Field | Detail |
|---|---|
| Active since | 2013 |
| Motivation | Financial gain |
| Signature targets | Retail, restaurant and hospitality, plus other sectors over time |
| Other sectors I noted (verify on G0046) | Transport, software, consulting, financial services, media, food and beverage, pharmaceutical |
| Ransomware link | Used a version of Darkside ransomware; deploys ransomware as the end payload in big game hunting (verify the RaaS claim on the page) |

## Summary

FIN7 is a financially motivated group, active since 2013. It goes after everyday services such as retail, restaurants and hospitality, and over time also transport, software, consulting, financial services, media and food and beverage.

It gets in by exploiting public-facing applications (for example CVE-2021-31207 in Exchange) and with spearphishing emails that carry malicious Office or RTF attachments. It runs code with PowerShell (a script that launches shellcode and fetches a second payload) and the command prompt, including cmd.exe opened through Win+R keystrokes sent by malicious USB devices that act as keyboards.

It persists with Registry Run keys, startup items and new Windows services, and uses compromised credentials to get SYSTEM access on Exchange servers. It takes over domains quickly with Kerberoasting, ZeroLogon (CVE-2020-1472) and RDP, and uses net commands and csvde.exe to enumerate domain admins and export Active Directory data.

It collects files, screenshots and desktop video. For C2 it uses DNS (A, OPT and TXT records), with DNS also used as a backup channel when HTTP fails. It sends stolen data to the MEGA file-sharing site. The last stage is encrypting systems (including ESXi virtual disks) with ransomware so it can demand payment.

## Kill-chain table

| Tactic | ID | Technique | How FIN7 uses it | Source |
|---|---|---|---|---|
| Initial Access | T1190 | Exploit Public-Facing Application | Exploited CVE-2021-31207 in Exchange | G0046 |
| Initial Access | T1566.001 | Phishing: Spearphishing Attachment | Emails with malicious Office documents or RTF files | G0046 |
| Execution | T1059.001 | Command and Scripting Interpreter: PowerShell | Script that launches shellcode and retrieves a further payload; custom obfuscated invoker (POWERTRASH) | G0046 |
| Execution | T1059.003 | Command and Scripting Interpreter: Windows Command Shell | Runs commands via cmd.exe, including opening the Run dialog with Win+R sent by malicious USB keyboards | G0046 |
| Persistence | T1547.001 | Boot or Logon Autostart Execution: Registry Run Keys / Startup Folder | Run and RunOnce keys, plus Startup folder items | G0046 |
| Persistence | T1543.003 | Create or Modify System Process: Windows Service | Created new services and added them to startup directories | G0046 |
| Persistence | T1078.003 | Valid Accounts: Local Accounts | Compromised credentials used for SYSTEM access on Exchange servers | G0046 |
| Defense Evasion | T1686 | Firewall rule modification | Rules allowing inbound TCP 59999 and sshd.exe on TCP 9898 | G0046 |
| Credential Access | T1558.003 | Steal or Forge Kerberos Tickets: Kerberoasting | Invoke-Kerberoast for credentials and lateral movement | G0046 |
| Discovery | T1087.002 | Account Discovery: Domain Account | `net group "Domain Admins" /domain`, plus csvde.exe to export AD data | G0046 |
| Discovery | T1069.002 | Permission Groups Discovery: Domain Groups | `net group "domain admins" /domain` | G0046 |
| Lateral Movement | T1210 | Exploitation of Remote Services | ZeroLogon (CVE-2020-1472) against domain controllers | G0046 |
| Lateral Movement | T1021.001 | Remote Services: Remote Desktop Protocol | RDP between victim systems | G0046 |
| Collection | T1005 | Data from Local System | Collected files and sensitive information | G0046 |
| Collection | T1113 | Screen Capture | Screenshots and desktop video recordings | G0046 |
| Command and Control | T1071.004 | Application Layer Protocol: DNS | C2 over DNS using A, OPT and TXT records | G0046 |
| Command and Control | T1008 | Fallback Channels | Harpy backdoor uses DNS as backup C2 if HTTP fails | G0046 |
| Exfiltration | T1567.002 | Exfiltration Over Web Service: Exfiltration to Cloud Storage | Sent stolen data to MEGA | G0046 |
| Impact | T1486 | Data Encrypted for Impact | Encrypted ESXi virtual disks with a Darkside-based ransomware; deploys ransomware as the end payload in big game hunting | G0046 |
| Reconnaissance | none mapped | n/a | Nothing confirmed in my notes | n/a |
| Resource Development | none mapped | n/a | Nothing confirmed in my notes | n/a |
| Privilege Escalation | none mapped | n/a | Nothing confirmed in my notes | n/a |


## To verify on attack.mitre.org

- [ ] Official name for T1686
- [ ] Point-of-sale malware and card-data collection (a FIN7 signature) were not in my pasted list. Look for them under Collection
- [ ] Malicious USB keyboards: look for a Hardware Additions entry (T1200) under Initial Access
- [ ] Defense Evasion looks thin. Check for obfuscation entries
- [ ] Check the T1078.003 sub-technique against "SYSTEM on Exchange servers"
- [ ] Verify the sector list and the Darkside/RaaS wording
