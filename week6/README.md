# Week 6: Burp Suite Mastery + MITRE ATT&CK + Threat Intelligence

**Goal:** Use Burp Suite confidently, and use MITRE ATT&CK as the shared language of threat intel.

## Files

| File | Contents |
|---|---|
| [burp-notes.md](burp-notes.md) | Proxy and scope, HTTP history, Repeater workflow, Intruder attack types, Decoder and Comparer |
| [mitre-attack-notes.md](mitre-attack-notes.md) | The 14 Enterprise tactics in execution order, technique IDs, mapping my past attacks to techniques |
| [pyramid-of-pain.md](pyramid-of-pain.md) | The pyramid, plus the IOC list extracted from a public malware report |
| [threat-actor-ttps.md](threat-actor-ttps.md) | APT29, Lazarus Group, FIN7: sponsor, sectors, kill-chain tables cited to MITRE IDs |
| [phase1-completion-report.md](phase1-completion-report.md) | Tools, concepts, and labs from Weeks 1–6 |

## Day by day

| Day | Focus | Output |
|---|---|---|
| 1 (Mon) | Intel levels, repo setup, Burp Proxy deep dive (scope, site map, HTTP history) | `burp-notes.md` skeleton |
| 2 (Tue) | ATT&CK structure, matrix end to end, mapping SQLi/XSS/SSRF/SUID/SMB to technique IDs, Repeater first pass | `mitre-attack-notes.md` |
| 3 (Wed) | Repeater workflow, replaying SQLi/XSS payloads, multi-step password-change chaining | Repeater section in `burp-notes.md` |
| 4 (Thu) | Pyramid of Pain, Intruder: Sniper fuzz and Cluster Bomb credential attack on DVWA login, lockout and rate-limit defenses | Intruder section in `burp-notes.md` |
| 5 (Fri) | Decoder (Base64, hashing), Comparer (valid vs invalid login diff), IOC list from a malware report | `pyramid-of-pain.md`, finished `burp-notes.md` |
| 6 (Sat) | APT29, Lazarus, FIN7 kill-chain tables and three-way comparison | apt29/lazarus/fin7 TTP files, `threat-actor-comparison.md`, `day6-notes.md` |
| 7 (Sun) | Merged threat actor write-up, Phase 1 report, LinkedIn update, full-chain Burp review, Phase 2 preview | `threat-actor-ttps.md`, `phase1-completion-report.md`, this README |

## Key takeaways

**Burp Suite**
- Repeater is where testing actually happens: tab groups keep several hypotheses open, and the diff view shows what changed.
- Intruder attack types: Sniper = one position at a time (fuzzing a single field); Battering Ram = same payload in every position; Pitchfork = parallel lists matched by position; Cluster Bomb = every combination (credential attacks).
- Decoder handles encode/decode/hash; Comparer shows byte-level differences between two responses.
- A successful brute force in a lab says little about real risk until you account for lockout, CAPTCHA and rate limiting.

**MITRE ATT&CK**
- Tactics = why, techniques = how, sub-techniques = the specific variant (e.g. T1566.001).
- Mapping attacks I performed myself (SQLi, XSS, SSRF, SUID privesc, SMB enumeration) to technique IDs is the skill that transfers to SOC interviews.

**Threat intelligence**
- Intel levels: strategic, operational, tactical, technical. SOC analysts mostly work at tactical and technical.
- Pyramid of Pain: hashes are trivial for attackers to change, TTPs are tough. Detection should aim at the top.
- Motivation shapes technique: APT29 (espionage) favors stealth and living off the land, Lazarus (disruption/finance) uses destructive malware and crypto theft, FIN7 (profit) uses spear-phishing and POS malware.

## Week 6 checkpoint

- [x] Burp Suite used end to end: Proxy, Repeater, Intruder, Decoder, Comparer
- [x] MITRE ATT&CK notes and Pyramid of Pain write-up on GitHub
- [x] APT29 / Lazarus / FIN7 kill-chain tables committed
- [x] Phase 1 completion report written
- [x] LinkedIn updated with Phase 1 skills

## Next: Phase 2 (Weeks 7–16)

Security+, SOC tooling, pentesting, SIEM, Active Directory, cloud.
