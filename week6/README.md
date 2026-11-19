# Week 6: Burp Suite Mastery + MITRE ATT&CK + Threat Intelligence

**Goal:** Use Burp Suite confidently, and use MITRE ATT&CK as the shared language of threat intel.

## Files

| File | Contents |
|---|---|
| [Burp notes.md](Burp%20notes.md) | Proxy and scope, HTTP history, Repeater workflow, Intruder attack types, Decoder and Comparer |
| [Burp notes day5 section.md](Burp%20notes%20day5%20section.md) | Day 5 Decoder and Comparer section |
| [Mitre attack notes.md](Mitre%20attack%20notes.md) | The 14 Enterprise tactics in execution order, technique IDs, mapping my past attacks to techniques |
| [Threat intel notes.md](Threat%20intel%20notes.md) | Intel levels and IOC notes |
| [Pyramid of pain.md](Pyramid%20of%20pain.md) | The pyramid, plus the IOC list extracted from a public malware report |
| [Apt29 ttps.md](Apt29%20ttps.md) | APT29 kill-chain table cited to MITRE IDs |
| [Lazarus ttps.md](Lazarus%20ttps.md) | Lazarus Group kill-chain table cited to MITRE IDs |
| [Fin7 ttps.md](Fin7%20ttps.md) | FIN7 kill-chain table cited to MITRE IDs |
| [Threat actor comparison.md](Threat%20actor%20comparison.md) | Three-way comparison by motivation and technique choice |
| [Threat actor ttps.md](Threat%20actor%20ttps.md) | Merged write-up of all three actors |
| [Day6 notes.md](Day6%20notes.md) | Day 6 working notes |
| [Phase1 completion report.md](Phase1%20completion%20report.md) | Tools, concepts, and labs from Weeks 1-6 |

## Day by day

| Day | Focus | Output |
|---|---|---|
| 1 (Mon) | Intel levels, repo setup, Burp Proxy deep dive (scope, site map, HTTP history) | `Burp notes.md` skeleton |
| 2 (Tue) | ATT&CK structure, matrix end to end, mapping SQLi/XSS/SSRF/SUID/SMB to technique IDs, Repeater first pass | `Mitre attack notes.md` |
| 3 (Wed) | Repeater workflow, replaying SQLi/XSS payloads, multi-step password-change chaining | Repeater section in `Burp notes.md` |
| 4 (Thu) | Pyramid of Pain, Intruder: Sniper fuzz and Cluster Bomb credential attack on DVWA login, lockout and rate-limit defenses | Intruder section in `Burp notes.md` |
| 5 (Fri) | Decoder (Base64, hashing), Comparer (valid vs invalid login diff), IOC list from a malware report | `Pyramid of pain.md`, finished `Burp notes.md` |
| 6 (Sat) | APT29, Lazarus, FIN7 kill-chain tables and three-way comparison | `Apt29 ttps.md`, `Lazarus ttps.md`, `Fin7 ttps.md`, `Threat actor comparison.md`, `Day6 notes.md` |
| 7 (Sun) | Merged threat actor write-up, Phase 1 report, LinkedIn update, full-chain Burp review, Phase 2 preview | `Threat actor ttps.md`, `Phase1 completion report.md`, this README |

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
