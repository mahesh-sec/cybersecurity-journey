# MITRE ATT&CK Notes (Week 6)

## Core concepts

- **Tactic** = the adversary's goal, the *why* (e.g. Credential Access). Format: `TA####`
- **Technique** = how the goal is achieved, the *how* (e.g. Phishing). Format: `T####`
- **Sub-technique** = a specific variant of a technique. Format: `T####.###`
  - Example: `T1566.001` = Phishing (T1566) → Spearphishing Attachment (.001)
- The Enterprise matrix has **14 tactics**, shown as columns. The matrix also has Mobile and ICS versions.
- The tactic order below is the *typical* attack flow. Real attackers can skip, repeat or reorder tactics.

## The 14 Enterprise tactics (in execution order)

| # | ID | Tactic | In my own words |
|---|----|--------|-----------------|
| 1 | TA0043 | Reconnaissance | Gathering information about the target (infrastructure, IPs, employees, credentials) to plan the attack. |
| 2 | TA0042 | Resource Development | Setting up what the attacker needs beforehand: servers, domains, accounts, malware and tools. Nothing touches the victim yet. |
| 3 | TA0001 | Initial Access | Getting the first foothold in the victim's network or systems. |
| 4 | TA0002 | Execution | Running malicious code in the victim's environment. |
| 5 | TA0003 | Persistence | Keeping access to the environment even after reboots, password changes or other interruptions. |
| 6 | TA0004 | Privilege Escalation | Gaining higher-level permissions (admin, root, SYSTEM) to reach more sensitive resources. |
| 7 | TA0005 | Defense Evasion | Avoiding detection, e.g. disabling security tools, clearing logs, hiding files. |
| 8 | TA0006 | Credential Access | Stealing credentials such as usernames, passwords and tokens. |
| 9 | TA0007 | Discovery | Mapping out the environment: systems, accounts, network layout, what can be reached. |
| 10 | TA0008 | Lateral Movement | Moving from one system to another inside the network. |
| 11 | TA0009 | Collection | Gathering the data the attacker is interested in. |
| 12 | TA0011 | Command and Control | Communicating with and controlling compromised systems. |
| 13 | TA0010 | Exfiltration | Stealing data out of the network, often compressed or encrypted to avoid detection. |
| 14 | TA0040 | Impact | Disrupting, manipulating or destroying systems and data (ransomware, deletion, DoS, resource hijacking). |

> Note: the IDs are not in numerical order (TA0011 comes before TA0010) because they were assigned when each tactic was created, not by position in the attack flow.

## Technique mapping exercise

Map attacks I've performed in this program to ATT&CK. Look each one up on https://attack.mitre.org (use the search box) and justify the choice.

| Attack / lab | Where I did it | Tactic | Technique ID and name | Why this fits |
|--------------|----------------|--------|-----------------------|---------------|
| SQL injection | DVWA / PortSwigger | Initial Access (TA0001) | T1190 Exploit Public-Facing Application | The web app failed to sanitize input before using it in a database query, so a flaw in an internet-facing app gave me a way in. |
| XSS | DVWA / PortSwigger | Execution (TA0002) | T1059.007 Command and Scripting Interpreter: JavaScript | The injected payload is JavaScript that runs in the victim's browser. |
| SSRF | | Initial Access (TA0001) | T1190 Exploit Public-Facing Application | I exploited a flaw in a public-facing app to make the server send requests on my behalf, reaching things I couldn't reach directly. |
| SUID privilege escalation | | Privilege Escalation (TA0004) | T1548.001 Abuse Elevation Control Mechanism: Setuid and Setgid | A binary with the SUID bit set runs with its owner's (root's) privileges, which I abused to gain higher permissions. |
| SMB enumeration | Metasploitable | Discovery (TA0007) | T1135 Network Share Discovery | Enumerating SMB shares to see what network resources were exposed (enum4linux / smbmap). |

> Alternative mappings considered: XSS could also map to T1539 (Steal Web Session Cookie) if the payload steals a cookie. SSRF against a cloud metadata endpoint would add T1552.005. Nmap scanning of SMB ports maps to T1046 (Network Service Discovery).

## Sources

- https://attack.mitre.org/matrices/enterprise
- https://attack.mitre.org/tactics/enterprise
- https://www.picussecurity.com/resource/blog/mitre-attack-framework-beginners-guide
