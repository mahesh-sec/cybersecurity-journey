# Week 7 – Splunk Notes

**Course:** Intro to Splunk (eLearning), Splunk Education
**Replaces:** Splunk Fundamentals 1, module 1 (the Fundamentals courses have been retired)
**Date:** 24 Nov 2026
**Certificate:** [Intro to Splunk (eLearning)](certificates/splunk-intro-certificate.pdf)
---

## 1. What is Splunk?

Splunk is a data platform that collects, indexes, searches and analyzes machine data from across an organization, such as:

- Application data
- Network data
- Server and system logs
- Security data

It is widely used as a **SIEM** (Security Information and Event Management) tool. Security teams use it to search and correlate events from many sources in one place.

**Why it matters for security work:** a SOC analyst can search one platform for failed logins, suspicious network activity or unusual application behavior instead of logging into every system separately.

---

## 2. Splunk Web and user roles

| Role | What it can do |
|------|----------------|
| **Admin** | Manages the platform, creates apps, and creates and shares knowledge objects |
| **Power** | Creates and shares knowledge objects |
| **User** | Views objects shared with them or ones they have permission for |

**Knowledge objects** are saved items that make data easier to search and reuse, such as saved searches, reports and field definitions.

---

## 3. Searching data

Search is used to filter the ingested data down to what matters, for example failed logins or other security-related events.

**Narrowing results**
- **Time picker:** restrict a search to a time range to reduce the number of events.
- **Fields:** add extra context to each event.

**Default fields**

| Field | Meaning |
|-------|---------|
| `host` | The machine or device the event came from |
| `source` | The file, stream or input the event came from |
| `sourcetype` | The format or type of the data |

---

## 4. The five components of the search language

| Component | Purpose | Example |
|-----------|---------|---------|
| **Search terms** | Define what data to retrieve; the basis of every search | `failed` |
| **Commands** | Tell Splunk what to do with the results (format, chart, calculate statistics) | `stats`, `chart`, `table`, `sort` |
| **Functions** | Define how to chart or evaluate the results | `count`, `avg` |
| **Arguments** | Values added to a function | `count(src_ip)` |
| **Clauses** | Control how results are grouped or arranged | `by host`, `as` |

### Example: failed logins by source IP

```spl
sourcetype=linux_secure "Failed password" | stats count by src_ip | sort -count
```

| Part | Component |
|------|-----------|
| `sourcetype=linux_secure "Failed password"` | Search terms |
| `stats`, `sort` | Commands |
| `count` | Function |
| `by src_ip` | Clause |

> The sourcetype name depends on how the data was ingested, so treat this as a pattern rather than a command that works everywhere.

**Security use:** a high count of failed logins from one IP is a common sign of brute-force or password-guessing activity.

---

## 5. Reports and dashboards

### Search jobs and sharing
- A normal search job stays available for **10 minutes** by default.
- A **shared report** keeps its results available for **7 days**.

### Dashboards
Search results can be turned into dashboard panels using different visualizations:

- Pie charts
- Bar graphs
- Geographic maps
- Tables and other chart types

**Security use:** dashboards give a quick view of things like login failures over time, top source IPs, or events by location.

---

## Key takeaways

1. Splunk collects machine data from across the organization and makes it searchable in one place.
2. The time picker and fields are the quickest ways to narrow a search.
3. Every search is built from five components: terms, commands, functions, arguments and clauses.
4. Reports and dashboards turn searches into reusable views for monitoring.

## To revisit
- [ ] Using Fields course (Day 3)
- [ ] Practice the example search on sample data in a Splunk trial or local install
- [ ] Confirm exactly what the User role can create and share (check course wording)
