# any.run lab: PXA Stealer delivery task vs BlueStacks installer (Week 7, Day 3)

Safety: view-only analysis of public any.run tasks. No samples were downloaded or run locally. IOCs are defanged.

## Task summary (PXA Stealer)
- Verdict: malicious, family tag PXA Stealer.
- Chain: msedge opens elpulpofoto[.]com (phishing TDS, JS / proof-of-work fingerprint check) -> redirect to cifafinancial[.]ca and storages.cifafinancial[.]ca -> payload download.
- Outcome: delivery stage only. No child processes spawned from the flagged msedge process (PID 7248), so the stealer did not execute in this task.

## Process notes
- Edge launch flags (`--no-sandbox`, `--disable-quic`, HttpsUpgrades disabled) are likely how the sandbox starts the browser, so they are not proof of malice.
- PID 7248 is Chromium's `network.mojom.NetworkService` child, a normal process in every Edge launch. It was flagged "phishing" because of the traffic that went through it.
- The JSON blob (user agent, screen size, GPU, timezone, `pow` value) is browser fingerprinting by the TDS page, used to filter bots and sandboxes before serving the payload.

## IOCs (defanged)
| Type | Value |
|---|---|
| Domain | elpulpofoto[.]com |
| Domain | cifafinancial[.]ca |
| Domain | storages.cifafinancial[.]ca |
| IPs (Cloudflare ranges) | 188.114.96.3, 188.114.97.3, 172.67.187.73, 104.21.80.220 |
| URL path | /scl/fo/0/get/ (payload download) |
| File | Korean-named zip, REF-F805B184, left as .crdownload (partial) |
| SHA1 (partial file) | f0d282dcb6fe2dcf8505fe6d030a61595b561745 |

Not IOCs: Edge cache files (`.tbres`, `.tmp`) and `chrome_Unpacker_BeginUnzipping...` temp files such as `page_embed_script.js`.

## Suricata alerts
- PHISHING Phishing TDS HTTP activity observed (/api/v + pow), SID 81001868
- PAYLOAD PXA Stealer payload download (/scl/fo/0/get/), SID 81002061, 23,716 bytes

## MITRE ATT&CK
- T1665 Hide Infrastructure
- T1566.002 Phishing: Spearphishing Link
- T1105 Ingress Tool Transfer

## Comparison with Monday's harmless file (BlueStacks installer)
BlueStacksInstaller (MD5 98995D1198DE458A11ABE8AFD6D40272) scored 100/100 on any.run. My verdict: false positive. The NETSUPPORT alert came from a bundled signed copy of 7-Zip 19.00 (VirusTotal 0/71), the "Host CPU Enumeration" alert was install telemetry to cloud.bluestacks.com, and the netsh activity was firewall rules.

| Area | Harmless file (BlueStacks installer) | PXA Stealer sample |
|---|---|---|
| Verdict / score | Malicious 100/100 (my verdict: false positive) | Malicious, PXA Stealer |
| Submission type | File (.exe) | URL |
| Process tree | BlueStacksInstaller -> HD-CheckCpu, BSX-Setup -> wscript -> cmd -> netsh (x5) | Only normal msedge children |
| Child processes from flagged process | Yes, explainable | None, stealer did not execute |
| Domains | cloud.bluestacks.com | elpulpofoto[.]com, cifafinancial[.]ca, storages.cifafinancial[.]ca |
| Alerts | NETSUPPORT (bundled 7-Zip), Host CPU Enumeration | Phishing TDS, PXA payload download |
| ATT&CK | T1082 | T1665, T1566.002, T1105 |
| Files | Bundled 7z.exe | Partial Korean-named zip |
| Evasion | None | TDS fingerprint check, Cloudflare-fronted infra |
| Overall | Normal installer behavior | Delivery stage only |

## Conclusion
The score and the process tree alone did not separate the two. What did: every alert on the installer traced to an explainable cause, while the PXA alerts pointed to attacker behavior (TDS fingerprint check, CDN-fronted domains, a suspicious zip lure, a payload-download signature). An analyst should verify why each alert fired and check destinations and context instead of trusting the verdict or score.

Caveat: the tasks are not like-for-like (file vs URL submission), and the PXA task covers only the delivery stage.

## Open items
- Full payload hash (only the partial .crdownload hash was captured).
- Check the SHA1 on VirusTotal.
- Splunk hunt idea: `index=dns query="*cifafinancial.ca" | stats count by src_ip, query`
