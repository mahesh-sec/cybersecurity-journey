
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
# SOC Alert Triage Simulation

## The Alert
- **Alert name:** Suspicious Office document spawning rundll32 and contacting multiple external IPs
- **Host / user affected:** WORKSTATION-04 / user: ravi (simulated)
- **Time:** 09:37:21
- **Detection source:** EDR / SIEM rule (simulated)
- **Sample:** First-stage Word macro launcher
- **SHA256:** `2cb81a1a59df4a4fd222fbcb946db3d653185c2e79cf4d3365b430b1988d485f`

## Step 1: Validate (is it real?)
**Evidence**
- Flagged malicious by **48 of 63** vendors on VirusTotal.
- In the sandbox run it contacted **10+ IPs and 9 domains** and dropped **16+ files**.
- Delivered as a Word document in a phishing email. It tricks the user into enabling macros, then shows a fake error ("Word experienced an error trying to open the file") as a decoy while the infection runs in the background.
- Dropped DLL: `%USERPROFILE%\Ygyhlqt\Bx5jfmo\R43H.dll`, run with `rundll32.exe` using the `Control_RunDLL` entry point.

**Verdict: True positive.**
This is not an authorized or benign tool. The document drops and runs a DLL and then beacons to many external hosts, which no legitimate Word file does.

## Step 2: Scope (how bad is it?)
**Persistence**
- Calls `CreateServiceW()` to install a Windows service that starts the malware copy automatically.
- The service name is random and imitates legitimate Windows services, so it blends in.

**C2 communication**
- Uses `HttpSendRequestW()` to send data over standard HTTP.
- Sensitive data is encrypted with custom algorithms, so the traffic is hard to tell apart from normal traffic.
- Uses multiple IPs and domains for C2, and multiple download URLs for the first loader, so blocking one does not stop the infection.

**Other affected machines**
- None observed in the sandbox run, since the sample collects data from the infected machine.
- In a real environment this cannot be assumed. I would hunt for the same hashes, the service-creation event, `rundll32.exe` with `Control_RunDLL`, and connections to the IOCs below.

**Severity: High**
- Confirmed malware with persistence and C2 on a user machine.
- A foothold like this can let the attacker reach the network and compromise other systems.
- Severity goes up to Critical if the user is senior staff or has access to sensitive data.

## Step 3: Escalate or Close
**Decision: Escalate to L2.** Confirmed malicious, persistent, and in contact with external infrastructure.

**Escalation note to L2:**
> At 09:37:21, user ravi on WORKSTATION-04 opened a Word document from a phishing email and enabled macros.
> File hash: 2cb81a1a59df4a4fd222fbcb946db3d653185c2e79cf4d3365b430b1988d485f (48/63 vendors flag it malicious).
> The macro downloaded and ran a DLL through rundll32.exe, then contacted 37.46.129[.]215 and other IPs and domains.
> Persistence: a new Windows service with a random name, created via CreateServiceW().
> I confirmed it is malicious using VirusTotal detections and sandbox behavior (multiple malicious IPs/domains contacted, files dropped).
> Recommend isolating the host, blocking the IOCs below, resetting ravi's credentials, and checking for other hosts with the same indicators.

## Step 4: Document

**Timeline** (adjust the order to match your sandbox process tree)
1. 09:37:21: User opens the Word document and enables macros.
2. Fake error message shown as a decoy.
3. Macro downloads the first loader (`NK05DJ2yiA.dll`, expected size 37,652 bytes) from one of the download URLs.
4. DLL dropped to `%USERPROFILE%\Ygyhlqt\Bx5jfmo\R43H.dll` and run via `rundll32.exe` / `Control_RunDLL`.
5. Windows service with a random name created via `CreateServiceW()`.
6. Malware beacons to C2 over HTTP via `HttpSendRequestW()`.

**IOCs**

| Stage | SHA256 |
|---|---|
| First-stage Word macro launcher | 2cb81a1a59df4a4fd222fbcb946db3d653185c2e79cf4d3365b430b1988d485f |
| Third-stage DLL | bbb9c1b98ec307a5e84095cf491f7475964a698c90b48a9d43490a05b6ba0a79 |
| Fourth-stage DLL | bd1e56637bd0fe213c2c58d6bd4e6e3693416ec2f90ea29f0c68a0b91815d91a |

**URLs:**
- http://abrillofurniture[.]com/bph-nclex-wygq4/a7nBfhs/
- http://allcannabismeds[.]com/unraid-map/ZZm6/
- http://ezi-pos[.]com/categoryl/x/
- http://giannaspsychicstudio[.]com/cgi-bin/PP/
- http://ienglishabc[.]com/cow/JH/
- https://etkindedektiflik[.]com/pcie-speed/U/
- https://vstsample[.]com/wp-includes/7eXeI/

**IPs:** 5.2.136[.]90, 37.46.129[.]215, 70.32.89[.]105, 110.172.180[.]180, 132.248.38[.]158, 138.197.99[.]250, 152.170.79[.]100, 157.245.145[.]87, 161.49.84[.]2, 190.55.186[.]229, 190.247.139[.]101, 203.157.152[.]9

**Actions taken / recommended**
- Isolate the host from the network.
- Block all IOCs above (IPs, domains, URLs) at the firewall, proxy and DNS.
- Remove the malicious service and dropped DLL, then reimage the machine.
- Reset the user's credentials.
- Hunt for the same hashes, service creation and `rundll32` activity on other hosts.
- Train users to spot lure documents and never enable macros on files received by email.
- Block macros in files that come from the internet.

**Lessons / what I'd do differently**
- Write the lessons yourself here: one or two lines on what you'd check first next time.
