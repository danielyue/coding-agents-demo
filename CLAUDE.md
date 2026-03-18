# NYC 311 Public Services Consulting Engagement

## Scenario

You are an analyst on a consulting team engaged by New York City to improve public services operations — specifically, the 311 service request system. The city wants to understand why some complaint types take dramatically longer to resolve than others and what operational changes could reduce resolution times without increasing headcount.

## Available Files

### Qualitative Sources (`engagement-docs/`)

- **`comptroller-audit-findings.txt`** — NYC Comptroller audit of the Department of Buildings (DOB). Key findings: complaint-driven enforcement model, equity gaps in penalties across neighborhoods, 80% increase in plan review times, 60% of correction requests with no re-inspection.
- **`mmr-311-performance.txt`** — Mayor's Management Report for the 311 Customer Service Center (FY2024). Key metrics: 38.2M total contacts, call answer rate decline from 85% to 74%, channel shift toward web/mobile, service level targets by agency.
- **`state-comptroller-monitoring.txt`** — NYS Comptroller monitoring tool methodology. Covers: neighborhood-level service request patterns, data quality caveats, geographic concentration of complaints.

### Quantitative Data (`ops_data.csv`)

2,275 rows of closed NYC 311 service requests (April–September 2025). Stratified sample across complaint types for analysis diversity.

**Columns:**

| Column | Description |
|---|---|
| `unique_key` | 311 service request ID |
| `created_date` | When the complaint was filed |
| `closed_date` | When the complaint was closed |
| `complaint_type` | Category (e.g., Noise - Residential, PLUMBING, Building/Use) |
| `descriptor` | Subcategory detail |
| `agency` | Responsible agency (NYPD, HPD, DOB, DOT, DEP, DSNY) |
| `borough` | NYC borough |
| `resolution_description` | How the complaint was resolved |
| `status` | All "Closed" in this dataset |
| `resolution_hours` | Hours from created to closed |

**Key patterns in the data:**

- Resolution times vary enormously by complaint type: NYPD types resolve in ~1 hour median; DOB types take 500+ hours (weeks)
- Borough-level comparisons are misleading without controlling for complaint type mix (Simpson's Paradox)
- The mean resolution time (496h) is 13x the median (37h) — extremely right-skewed distribution
- DOB complaints connect directly to the Comptroller audit findings about enforcement delays

## Analysis Goals

1. Quantify resolution time disparities across agencies, complaint types, and boroughs
2. Connect quantitative patterns to qualitative findings in the engagement documents
3. Identify actionable recommendations grounded in both data and institutional context
4. Present findings in formats suitable for a non-technical city leadership audience
