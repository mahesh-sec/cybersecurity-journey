
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


# SOC 101 notes: Event and Incident Management (Week 7, Day 3)

## Event management (before an alert exists)
1. **Collect** events from EDR, firewalls, IDS/IPS, application logs and other systems.
2. **Normalize** the data into one consistent schema.
3. **Analyze and correlate** events across sources to spot activity that could be a security threat. Correlation rules raise the alerts analysts triage.

## Incident management process
1. **Identification:** detect and confirm that an incident is happening.
2. **Classification:** rate it by severity and impact.
3. **Investigation:** work out how it happened by correlating logs and related events.
4. **Containment:** isolate affected systems so it cannot spread or cause more damage.
5. **Eradication:** remove the malware or the root cause.
6. **Recovery:** restore systems to normal operation and verify they are clean.
7. **Post-incident:** write the full report and record how to prevent the same incident again.

## How an analyst handles an incoming alert
- Read the alert: what rule fired, on which asset, and why.
- Decide true positive or false positive by checking the cause and context, not the score alone.
- Scope it: which hosts, users and destinations are involved, and did anything execute?
- Escalate or close: escalate confirmed or unclear high-impact alerts, and close false positives with a reason.
- Document what was checked, the evidence, and the decision.

## Link to today's lab
- BlueStacks installer: scored 100/100 but was a false positive. The NETSUPPORT alert came from a bundled signed 7-Zip, and the other alerts were normal installer behavior.
- PXA Stealer task: true positive for the delivery stage (TDS fingerprint check, then a payload download). Nothing executed in the task.
