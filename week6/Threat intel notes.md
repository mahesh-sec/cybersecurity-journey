# Week 6 Day 1: Threat Intelligence Foundations

## What is threat intelligence?
Analyzed, contextualized information about threats and adversaries that helps defenders make decisions and take action.

## The four levels

| Level | Question it answers | Who uses it | Example outputs |
|---|---|---|---|
| Strategic | Which threats and activities create business risk, and who is behind them and why? | Executives, CISO, board members, risk teams, legal and compliance teams | Executive briefings, resource allocation reports |
| Operational | What is a specific actor or campaign doing? | SOC managers, threat analyst teams, threat hunters | Actor profiles, campaign reports, attack-chain narratives |
| Tactical | What methods (TTPs) does the attacker use to breach systems? | SOC analysts, threat hunters, incident responders (daily use) | Attack mappings, behavior-based analysis, incident response playbooks |
| Technical | What indicators (IOCs) can we detect or block? | SOC analysts, incident responders | Malicious IPs, domains, URLs, file hashes |

> Note: sources group these differently. Some use three levels (strategic, operational, tactical) and treat technical as part of tactical. The boundaries are not a formal standard.

## Which levels does a SOC analyst work with most?
Mostly **technical and tactical**, because daily work is triaging alerts, matching indicators, and recognizing attacker behavior during incidents. Operational intel supports hunting; strategic intel is aimed at executives.

## Notes from Kimmons video (Simply Cyber)
- **What threat intel is in practice:** contextualized data gathered and recorded from breaches and research.
- **How it gets operationalized:**
  - Reactive: when an incident occurs, check whether it maps to known threat intel to understand it and prevent further damage.
  - Proactive: feed IOCs into detection tools and hunt for known actor behavior.
- **ATT&CK:** (add what he said about analysts using MITRE ATT&CK; use for Day 2)

## Sources
- Nordlayer: https://nordlayer.com/learn/threat-management/types-of-threat-intelligence/
- Simply Cyber, "You MUST understand Cyber Threat Intelligence to Blue Team": https://www.youtube.com/watch?v=tWHqHy-MC1U
