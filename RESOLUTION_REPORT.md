# Resolution Time Analysis — NYC 311 Service Requests

**Date:** 2026-03-19
**Dataset:** 2,275 closed service requests, April-September 2025
**Method:** DuckDB SQL analysis of `ops_data.csv`

---

## Executive Summary

Resolution times vary by **three orders of magnitude** across complaint types, from under 1 hour (NYPD noise/parking) to over 1,200 hours (DOB building/use). The responsible agency - not the borough - is the primary driver of resolution speed. DOB complaints account for 22% of requests but dominate the worst-performer list entirely.

---

## Key Findings

### 1. Agency Is the Determining Factor

| Agency | Requests | Median Hours | Mean Hours |
|--------|----------|-------------|-----------|
| NYPD | 606 | 1.3 | 3.1 |
| DEP | 132 | 6.4 | 67.5 |
| DOHMH | 52 | 12.5 | 51.4 |
| DOT | 375 | 53.9 | 258.5 |
| HPD | 612 | 87.7 | 368.1 |
| DOB | 498 | 744.0 | 1,593.2 |

DOB's median resolution time is **572x slower** than NYPD's. Even within agencies, variation is large: HPD resolves HEAT/HOT WATER complaints at a 37-hour median but takes 185 hours for PLUMBING.

### 2. The Five Worst Complaint Types

| Complaint Type | Agency | Median Hours | Median Days | P90 Hours |
|---------------|--------|-------------|------------|----------|
| Building/Use | DOB | 1,269 | 53 days | 6,396 |
| General Construction/Plumbing | DOB | 543 | 23 days | 3,464 |
| Elevator | DOB | 396 | 16 days | 3,870 |
| PLUMBING | HPD | 185 | 8 days | 2,031 |
| Street Light Condition | DOT | 172 | 7 days | 1,357 |

All three DOB complaint types have P90 values exceeding 3,000 hours (4+ months). These are not outliers - they represent the normal tail of the distribution.

### 3. Borough Differences Are Mostly Complaint Mix (Simpson's Paradox)

Raw borough medians range from 14 hours (Queens) to 53 hours (Staten Island). But this is misleading:

- **Queens appears fast** because 42% of its requests go to NYPD (fast resolution), masking the fact that its DOB complaints are the slowest in the city (1,306-hour median).
- **Within DOB**, Queens is the worst borough (1,306h median) and Manhattan the fastest (464h).
- **Within NYPD**, borough differences are negligible (0.7-1.7 hours).

Controlling for agency, borough differences shrink dramatically but don't disappear. DOB's Queens-Manhattan gap (1,306 vs 464 hours) likely reflects the plan review bottleneck identified in the Comptroller audit: Queens saw a 93% increase in plan approval times.

### 4. Why DOB Is So Slow: Resolution Pattern Analysis

DOB complaints follow a distinctive failure pattern visible in their resolution descriptions:

- **"Attempted to investigate... no access"** - the top resolution for Building/Use (63 cases, 2,317h median). The inspector shows up, can't get in, and the clock keeps running.
- **"Made a second attempt"** - 14 cases at 2,271h median. A repeat of the access problem.
- **"Investigated and issued violations"** - even successful enforcement takes 1,148h median.
- **"Reviewed and closed"** - administrative closures are faster (59h) but represent triage, not resolution.

This maps directly to the Comptroller's finding that 60% of Requests for Corrective Action had no evidence of re-inspection. The enforcement model requires physical access to private property, and when access is denied, cases stall indefinitely.

### 5. Extreme Right Skew Across All Types

The overall mean (496h) is 13x the median (37h). But skewness varies:

- **Water System** has the worst ratio (10.6x) - most resolve in 6 hours, but a long tail of complex cases pulls the mean to 68 hours.
- **DOB types** have lower ratios (1.7-3.1x) not because they're less skewed, but because even their medians are already high. The entire distribution is shifted right.
- **NYPD types** are the most symmetric (1.8-2.9x ratio) - fast response with a modest tail.

### 6. Speed Tier Distribution

| Tier | Requests | % |
|------|----------|---|
| < 1 hour | 278 | 12% |
| 1-24 hours | 686 | 30% |
| 1-7 days | 621 | 27% |
| 1-4 weeks | 329 | 14% |
| 4+ weeks | 361 | 16% |

Nearly 1 in 6 requests takes over a month. Only DOB and HPD contribute to the 4+ week tier, with DOB dominating. NYPD never appears in the 4+ week tier.

---

## Patterns Explaining Slow Resolution

1. **Complaint-driven enforcement requires property access.** DOB can't resolve building code complaints without entering the property. When access is denied, cases enter a retry loop that can last months. This is a structural constraint of the enforcement model, not a staffing problem.

2. **Plan review backlogs compound enforcement delays.** The Comptroller found 80% longer plan approval times, with some homeowners receiving violation notices while their correction plans were still pending DOB review. The data confirms this: DOB's resolution times span weeks to months, consistent with plans sitting in review queues.

3. **HPD housing complaints cluster by building condition.** HEAT/HOT WATER resolves at 37h median (emergency priority), but PLUMBING (185h) and PAINT/PLASTER (149h) reflect chronic building maintenance failures. These co-occur geographically, as the NYS Comptroller monitoring tool notes.

4. **DOT street light complaints depend on infrastructure cycles.** At 172h median, street light repairs likely batch into maintenance runs rather than responding to individual complaints, explaining the long but predictable resolution times.

5. **NYPD resolves fast because the response model is different.** Police dispatch to the location, assess, and close - no property access needed, no plan review, no re-inspection cycle. The operational model, not the complaint severity, determines the timeline.

---

## Recommendations for Further Analysis

- Link DOB resolution times to the specific neighborhoods identified in the Comptroller equity audit (Jamaica, Flushing, Borough Park) to test whether penalty-heavy districts also have the longest waits.
- Decompose DOB resolution times by resolution description to quantify what share of the delay is access-related vs. plan-review-related vs. re-inspection gaps.
- Model the counterfactual: if DOB shifted 10% of complaint-driven inspections to proactive, risk-based targeting, what would the expected impact on resolution times be?
