# Pyramid of Pain

**Week 6, Day 5** | Topic: Indicators of Compromise (IOCs) and the Pyramid of Pain

## Overview

The Pyramid of Pain was introduced by David Bianco in 2013. It ranks the types of indicators a defender can use to detect an attack by how much *pain* it causes the attacker when the defender detects and blocks them.

- **Lower levels** are easy for defenders to collect but trivial for attackers to change.
- **Higher levels** cost the attacker real time, money and effort, but they are harder for defenders to detect.

```
            /\
           /  \        TTPs                 Tough
          /----\
         /      \      Tools                Challenging
        /--------\
       /          \    Network/Host         Annoying
      /------------\   Artifacts
     /              \  Domain Names         Simple
    /----------------\
   /                  \ IP Addresses        Easy
  /--------------------\
 /                      \ Hash Values       Trivial
/------------------------\
```

## The six levels

### 1. Hash values (Trivial)

- A hash (MD5, SHA-1, SHA-256) uniquely identifies a file. Defenders use hashes to identify known malware samples, for example by looking them up on VirusTotal.
- Changing a single character or bit in a file produces a completely different hash, so the attacker can evade hash-based detection with almost no effort.
- Hashes are still useful for referencing a specific sample, but they are weak for long-term detection.

### 2. IP addresses (Easy)

- Defenders can block malicious IPs at the firewall.
- Attackers can switch IPs easily by moving to a different network, or by using VPNs, proxies and Tor.
- **Fast Flux** makes this harder to block: one domain rotates through many changing IP addresses, so blocking one IP achieves little.

### 3. Domain names (Simple)

- Blocking a domain the attacker uses for C2 or phishing forces them to create and register a new one, and update their DNS records.
- This takes more effort than swapping an IP, but it is still simple. Registration is cheap, and attackers can automate it with domain generation algorithms (DGAs) and dynamic DNS.
- **Homograph / Punycode attacks** use Unicode lookalike characters to imitate a trusted domain. Example: `adıdas.de` (dotless "ı") is stored as `xn--addas-o4a.de`.
- Attackers also hide destinations behind URL shorteners. Adding `+` to some shortened links previews the real destination.
- Detection sources: proxy logs and web server logs.

### 4. Host and network artifacts (Annoying)

- Artifacts are the traces an attacker leaves behind when carrying out an attack.
- **Host artifacts:** registry keys, dropped or modified files, suspicious process execution (for example, a process spawned from Word).
- **Network artifacts:** unusual User-Agent strings, URI patterns, C2 communication patterns.
- Detecting these forces the attacker to go back and change their tooling or methods, which is annoying and time consuming.
- Detection sources: Wireshark/TShark on PCAPs, IDS alerts (Snort), endpoint logs.

### 5. Tools (Challenging)

- Tools are what the attacker uses to carry out the attack: malicious macro documents, backdoors, custom EXE/DLL files, payloads, password crackers.
- If defenders detect the tools, the attacker has to find or build replacements, or learn new ones. That costs time and money, and many will give up or pick another target.
- Detection methods:
  - Antivirus signatures
  - YARA rules
  - Fuzzy hashing (for example, ssdeep), which matches files that are *similar* even if they are not identical
- Sample sources: MalwareBazaar, Malshare.

### 6. Tactics, Techniques and Procedures (Tough)

- TTPs describe *how* the attacker operates, from initial access through persistence to data exfiltration.
- This is the hardest level for an attacker to change, because they would have to change how they work, not just swap a tool or an address.
- TTPs are cataloged in the **MITRE ATT&CK** framework.
- Example: detecting a Pass-the-Hash attack through Windows event log monitoring can reveal the compromised host and stop lateral movement.
- Detecting TTPs leaves the attacker two options: spend significant time and training to change their approach, or give up and target someone else.

## Summary table

| Level | Indicator | Pain for attacker | Why |
|---|---|---|---|
| 1 | Hash values | Trivial | One changed bit gives a new hash |
| 2 | IP addresses | Easy | New network, VPN, proxy, Tor or Fast Flux |
| 3 | Domain names | Simple | Must register a new domain and update DNS (but this can be automated) |
| 4 | Host/network artifacts | Annoying | Must change tooling and methods |
| 5 | Tools | Challenging | Must build, buy or learn new tools |
| 6 | TTPs | Tough | Must change their whole way of operating |

## Key takeaway

> The amount of pain you cause an adversary depends on the types of indicators you are able to make use of. (David Bianco)

As you move up the pyramid, detection causes more pain for the attacker, but the indicators are also harder for defenders to find and use. Hashes are easy to collect and easy to evade. TTPs are hard to detect but cost the attacker the most.

## Link to MITRE ATT&CK

TTPs sit at the top of the pyramid, and ATT&CK is the catalog of them. MITRE's *Summiting the Pyramid* project scores detection analytics against the pyramid so defenders can build detections that are harder for attackers to evade.

## IOC extraction exercise

**Report analyzed:** [From a Single Click: How Lunar Spider Enabled a Near Two-Month Intrusion](https://thedfirreport.com/2025/09/29/from-a-single-click-how-lunar-spider-enabled-a-near-two-month-intrusion/) (The DFIR Report, September 2025)

**Summary of the case:** A JavaScript file disguised as a tax form downloaded an MSI package that deployed Brute Ratel, which injected Latrodectus into `explorer.exe`. The attacker then used BackConnect (VNC), Cobalt Strike and a custom .NET backdoor to harvest credentials, move laterally, and exfiltrate data with Rclone over FTP. The intrusion lasted almost two months.

All network indicators are defanged (`[.]`) so they cannot be clicked by accident.

### Level 1: Hash values (Trivial)

SHA-256 shown. The report also lists MD5 and SHA-1 for each file.

| File | Role in the intrusion | SHA-256 |
|---|---|---|
| `upfilles.dll` | Brute Ratel loader | `f4cb6b684ea097f867d406a978b3422bbf2ecfea39236bf3ab99340996b825de` |
| `wscadminui.dll` | Brute Ratel badger (day 5) | `6c3b2490e99cd8397fb79d84a5638c1a0c4edb516a4b0047aa70b5811483db8f` |
| `system.dl_` / `cron801.dl_` | Cobalt Strike beacon | `77eede38abdc740f000596e374b6842902653aeafb6c63011388ebb22ec13e28` |
| `sys.dll` | Cobalt Strike stager | `100e03eb4e9dcdab6e06b2b26f800d47a21d338885f5dc1b42c56a32429c9168` |
| `lsassa.exe` | Custom .NET backdoor | `203eda879dbdb128259cd658b22c9c21c66cbcfa1e2f39879c73b4dafb84c592` |
| `zero.exe` | Custom Zerologon (CVE-2020-1472) exploit | `36bc32becf287402bf0e9c918de22d886a74c501a33aa08dcb9be2f222fa6e24` |
| `rustscan.exe` | Network scanner | `37471af00673af4080ee21bd248536147e450d2eff45e8701a95d1163a9d62fe` |
| `run.bat` | Rclone exfiltration script | `411dfb067a984a244ff0c41887d4a09fbbcd8d562550f5d32d58a6a6256bd7b2` |
| `start.vbs` | Rclone launcher | `1a8ebf914ebea34402eecbf0985f05ae413663708d2fcc842fc27057ac5ec4ed` |
| `c356468.exe` | Listed in the report's hashes; role not described | `8fb5034aedf41f8c8c4c4022fdde7db3c70a5a7c7b5b4dec7f6a57715c18a5bf` |

### Level 2: IP addresses (Easy)

| Family | IP addresses |
|---|---|
| Cobalt Strike | `206.206.123[.]209`, `45.129.199[.]214`, `31.13.248[.]153` |
| Brute Ratel | `95.164.68[.]73`, `138.124.183[.]215`, `91.194.11[.]183`, `94.232.249[.]100`, `94.131.108[.]254`, `94.232.249[.]108`, `45.150.65[.]85`, `195.123.225[.]161`, `195.211.98[.]249`, `195.123.225[.]251` |
| BackConnect | `185.93.221[.]12`, `193.168.143[.]196` |
| Lsassa backdoor | `162.0.209[.]121` |
| Metasploit | `217.196.98[.]61` |
| Exfiltration (FTP server) | `45.135.232[.]3` |

### Level 3: Domain names (Simple)

| Family | Domains |
|---|---|
| Latrodectus | `workspacin[.]cloud`, `illoskanawer[.]com`, `grasmetral[.]com`, `jarkaairbo[.]com`, `scupolasta[.]store` |
| Brute Ratel | `anikvan[.]com`, `altynbe[.]com`, `boriz400[.]com`, `erbolsan[.]com`, `samderat200[.]com`, `dauled[.]com`, `kasymdev[.]com`, `kasym500[.]com`, plus two subdomains of the legitimate `tyk[.]io` service: `ridiculous-breakpoint-gw[.]aws-use1[.]cloud-ara[.]tyk[.]io` and `uncertain-kitten-gw[.]aws-euc1[.]cloud-ara[.]tyk[.]io` |
| Lsassa backdoor | `cloudmeri[.]com` |
| Cobalt Strike | `avtechupdate[.]com` |

### Level 4: Host and network artifacts (Annoying)

| Artifact | Type | Detail |
|---|---|---|
| Rclone config | Host | `rclone.conf` with FTP user `J0eBidenAbrabdy1aS3ha2Yeami` (the first attempt used the truncated `J0eBidenAbrabdy1aS3ha2`) |
| Renamed Rclone | Host | Dropped as `sihosts.exe` in `C:\ProgramData`, alongside `start.vbs`, `run.bat` and `rclone.conf` |
| Registry Run key | Host | Key named `Update` pointing at the Brute Ratel DLL |
| Scheduled task | Host | `SchedulerLsass`, running `%ALLUSERSPROFILE%\USOShared\lsassa.exe` |
| Latrodectus user-agent | Network | `Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Tob 1.1)` |
| Cobalt Strike URI paths | Network | `/vodeo/wg01ck01` and `/vodeo/vid_wg01ck01` |
| Lsassa C2 pattern | Network | POST to `/comm.php` roughly every 250 seconds, sending hostname and username |
| RDP client name | Network | `VPS2DAY-32220LE`, which leaked the attacker's hosting provider |

### Level 5: Tools (Challenging)

| Tool | Purpose |
|---|---|
| Latrodectus | Loader/downloader, injected into `explorer.exe`; also pulled a stealer module |
| Brute Ratel C4 | C2 framework (badger) |
| Cobalt Strike | C2 framework (beacons) |
| BackConnect | VNC-based remote access module |
| Metasploit | Attempted lateral movement (the C2 connection failed) |
| `lsassa.exe` | Custom .NET backdoor with scheduled-task persistence |
| `zero.exe` | Custom Zerologon exploit |
| AdFind | Active Directory enumeration |
| PsExec | Lateral movement |
| rustscan | Network scanning |
| Rclone | Data exfiltration |
| 7-Zip | Archiving collected data |

Runas also appears in the report's tool column. It is a built-in Windows feature that the attacker used with stolen credentials, so it sits close to the TTP level.

### Level 6: TTPs (Tough)

The report maps about 40 techniques to MITRE ATT&CK. A few that stand out:

| Tactic | Technique |
|---|---|
| Initial Access | Drive-by Compromise (T1189) |
| Execution | JavaScript (T1059.007), Rundll32-launched DLLs |
| Persistence | Registry Run Keys (T1547.001), Scheduled Task (T1053.005) |
| Privilege Escalation | Access Token Manipulation (T1134), Bypass User Account Control (T1548.002) |
| Defense Evasion | Process Injection (T1055), File Deletion (T1070.004) |
| Credential Access | LSASS Memory (T1003.001), Credentials In Files (T1552.001) |
| Lateral Movement | Remote Desktop Protocol (T1021.001), Exploitation of Remote Services (T1210) |
| Exfiltration | Automated Exfiltration (T1020), Exfiltration Over Unencrypted Non-C2 Protocol (T1048.003) |

### Reflection

- **Counts by level:** 10 file hashes, 18 IP addresses, 17 domains, 8 host/network artifacts, 12 tools, and about 40 ATT&CK techniques.
- **The lowest three levels are the easiest to collect and the easiest to evade.** The attacker used 15 different Brute Ratel and Latrodectus domains and many IPs, so blocking a few would barely slow them down. A different build of any of the files would also change every hash.
- **Renaming shows the pain gap.** The attacker renamed Rclone to `sihosts.exe`. A file-name or hash rule misses that, but a detection for Rclone's behavior (FTP exfiltration of file shares with those command-line flags) would not.
- **Legitimate tools raise the bar for defenders.** Much of the intrusion used built-in Windows tools (`runas`, `rundll32`, `net`, `nltest`, `PsExec`). These cannot be blocked by hash or IP, so only behavioral detection at the TTP level catches them. Examples are the repeated LSASS access pattern, the `ms-settings` registry hijack used for the UAC bypass, and process injection.
- **Takeaway:** the report's own detections section mixes network rules, Sigma rules (behavior) and YARA rules (tools). Detections higher up the pyramid are what would have forced this attacker to change how they operate.

## References

- David Bianco, [The Pyramid of Pain](http://detect-respond.blogspot.com/2013/03/the-pyramid-of-pain.html)
- TryHackMe, [Pyramid of Pain room](https://tryhackme.com/room/pyramidofpainax)
- MITRE ATT&CK: <https://attack.mitre.org/>
- MITRE CTID, [Summiting the Pyramid](https://ctid.mitre.org/blog/2024/12/16/summiting-the-pyramid-bring-the-pain)
