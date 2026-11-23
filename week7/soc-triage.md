
# SOC Triage Notes – Week 7

*Source: TCM Security SOC 101 (The SOC and Its Role, SOC Models/Roles/Organizational Structures, Incident and Event Management).*

## What a SOC does
SOC stands for Security Operations Center. It is a centralized unit within an organization that handles security incidents, events and issues.

## Roles in a SOC

**SOC analyst tiers**
- Tier 1 analyst
- Tier 2 analyst
- Tier 3 analyst (in some cases)

**Specialized roles**
- Threat hunter
- Threat intelligence analyst
- Malware analyst
- Forensic analyst
- Incident responder
- Vulnerability manager
- Security engineer

**Management roles**
- SOC manager
- CISO
- Director of security

## Event vs incident
- **Event:** an observable action that happens within an organization and has the potential to become a security incident.
- **Incident:** an occurrence that can actually harm the organization's security and information.

## Where event data is collected / how incidents are managed
<!-- add what the Incident and Event Management chapter said about data sources and incident management -->

## What each tier does
<!-- Tier 1, Tier 2, Tier 3 responsibilities: add from the video -->

## How an analyst handles an incoming alert
<!-- 3–5 bullets; compare with the worked example below -->

## Worked example: BlueStacks installer alert (any.run)
- Alert: "Malicious activity", threat score 100/100 (an *event* that could have become an *incident*)
- Triage: split the verdict into parts, checked the file behind the alert on VirusTotal, confirmed the network destination was the vendor domain
- Outcome: false positive, closed as benign (it never became an incident)
- Full write-up: see `malware-analysis.md`
