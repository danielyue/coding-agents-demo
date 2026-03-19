# Recommendations for Reducing NYC 311 Resolution Times

**Date:** 2026-03-19
**Prepared for:** NYC Mayor's Office of Operations
**Dataset:** 2,275 closed service requests, April--September 2025
**Companion analysis:** RESOLUTION_REPORT.md (baseline quantitative findings)

---

## Executive Summary

Under the most optimistic assumptions, three targeted operational reforms can reduce average 311 resolution time by up to 33%; with realistic implementation friction, the likely reduction is 23--26%, short of but within range of the city's 30% target, without adding headcount. The reforms focus on the Department of Buildings (DOB) and the Department of Housing Preservation and Development (HPD) --- the two agencies that together account for 49% of requests but 93% of total resolution hours. Recommendation 1 restructures DOB's failed-access inspection model to eliminate the repeat-visit loop that traps 107 building code cases at a median of 87 days. Recommendation 2 imposes a 30-day escalation trigger on HPD housing cases stalled in phone-outreach limbo, capping the 78 longest-running cases that currently average 83 days. Recommendation 3 sets a 72-hour service standard for DOB administrative reviews, clearing a backlog of 75 Elevator and Building/Use complaints that sit open for weeks awaiting desk decisions. At the ceiling, these changes would reduce the system-wide mean from 21 days to 14 days (33%); after discounting for partial compliance and implementation lag, a realistic range is 15--16 days (23--26% reduction). Both estimates address the structural bottlenecks identified in the data and the Comptroller's audit.

---

## Methodology Note

**Quantitative evidence** comes from DuckDB SQL analysis of `ops_data.csv`, a stratified sample of 2,275 closed 311 service requests spanning six agencies and five boroughs. Resolution hours are calculated from created-to-closed timestamps. The counterfactual model uses a cap approach: for each recommendation, we ask *"what if the slowest cases in this category had resolved no slower than a target time?"* Cases already faster than the target are unchanged; cases slower than the target are set to the target; and the system-wide mean is recalculated. This produces a mechanical ceiling on savings --- it assumes every affected case hits the target exactly, with no case resolving faster. Actual savings depend on implementation quality and may be lower (see Limitations).

**Qualitative evidence** draws on three public reports: the NYC Comptroller's audit of DOB enforcement (2022--2023), the Mayor's Management Report for the 311 Customer Service Center (FY2024), and the NYS Comptroller's monitoring tool methodology. These reports are 1--3 years older than the operational data (April--September 2025); we assume the institutional patterns they describe persist, but DOB may have implemented partial reforms in the interim.

**Sampling note.** The 2,275-case dataset is described as a stratified sample, but the stratification methodology (strata definitions, proportional vs. equal allocation) is not documented. DOB accounts for 22% of the sample (498 cases); if this overrepresents DOB's share of actual citywide volume, the 496-hour system-wide mean is not directly generalizable to the city. Our recommendations target within-agency patterns (DOB access failure, HPD phone stall, DOB admin close) that should be robust to sampling design, but the combined percentage reduction is anchored to this sample mean.

**Limitations** are discussed in Section 8. The most important: this is a sample, not a census; the counterfactual model is a ceiling, not a forecast; and 311 data has known issues with duplicates and reporting bias.

---

## Recommendation 1: DOB Access-Failure Protocol

### The Problem

When a 311 complaint triggers a DOB inspection and the inspector cannot gain access to the property, the case enters a loop that effectively has no exit. The inspector attempts a visit, records "could not gain access," and the case sits open --- often for months --- until a second attempt is made. If the second attempt also fails, DOB closes the case as unresolvable. The complainant is told to refile.

This is the single costliest failure mode in the 311 system.

### The Evidence

In our dataset, **107 DOB cases** were resolved with access-failure descriptions. We identified these by matching resolution text containing "could not gain access," "denied access," or "no access" --- corresponding to DOB's standard closure language for failed inspections. (The full text-matching criteria are documented in `deep_analysis.py`.) We have not audited for false positives (e.g., "no access" appearing in a non-inspection context) or false negatives (DOB using alternative phrasing); given that these 107 cases drive 27.5% of total system hours, even modest misclassification rates would materially affect the impact estimate. These 107 cases represent just 4.7% of all requests but consume **311,046 total resolution hours** --- 27.5% of all hours across the entire system.

| Category | Cases | Median Hours | Mean Hours | Total Hours |
|----------|-------|-------------|-----------|-------------|
| DOB access failure | 107 | 2,079 | 2,907 | 311,046 |
| DOB investigated (no action needed) | 124 | 1,007 | 1,578 | 195,713 |
| DOB admin close | 144 | 80 | 439 | 63,200 |
| All other cases (non-DOB) | 1,777 | 24 | 166 | 295,689 |

The median access-failure case takes **2,079 hours** (87 days) to close --- twice as long as DOB cases where the inspector *did* gain access and found no violation (1,007 hours, or 42 days). The gap between these two medians (1,072 hours, or 45 days) is substantial. Not all of this gap is attributable to access logistics alone --- access-failure cases skew toward Illegal Conversion complaints (the most complex DOB case type), while investigated-no-action cases may include simpler complaints where the inspector found nothing wrong. The counterfactual model therefore uses the investigated-no-action median as a cap rather than a replacement: it asks what would happen if access-failure cases resolved *no slower than* the peer group, acknowledging that some of the gap reflects case complexity rather than process failure.

The Comptroller's audit confirms this pattern at scale: DOB issued 9,167 Requests for Corrective Action, but **60% remained open with no evidence of re-inspection** (comptroller-audit-findings.txt, Finding 6). The audit also found that DOB "attempted 71,954 inspections" against 74,035 complaints --- a near-1:1 ratio that leaves little capacity for follow-up when initial access fails (Finding 1).

The problem is concentrated in Building/Use complaints, particularly **Illegal Conversion** cases (142 in our sample, 1,253-hour median). These cases require interior access to confirm whether a residential building has been illegally subdivided --- access that occupants have every incentive to deny.

### The Recommendation

Replace blind repeat visits with a structured access-failure protocol:

1. **Scheduled-access appointments.** After an initial access failure, DOB contacts the complainant and the property owner to schedule a specific inspection window, rather than dispatching an inspector for an unannounced second visit that is equally likely to fail. *Enforcement tradeoff:* For Illegal Conversion cases, advance notice may allow occupants to temporarily conceal evidence. DOB should consider risk-tiered scheduling --- appointments for lower-risk complaints (No Certificate of Occupancy, commercial-use violations) where concealment is difficult, and expedited unannounced re-visits for Illegal Conversion cases where evidence is portable.
2. **Virtual triage for desk-reviewable cases.** Some Building/Use complaints (e.g., No Certificate of Occupancy, Illegal Commercial Use in Residential Zone) can be partially assessed through permit records, certificate of occupancy databases, and building plans without a physical visit. Route these to a desk review first; dispatch an inspector only if the desk review confirms probable cause. Of the 5 Building/Use descriptor types in our data, at least 2 (No Certificate of Occupancy and Illegal Commercial Use) are partially verifiable from existing DOB records.
3. **Access-warrant escalation.** For cases where scheduled access is refused, establish a clear timeline to escalate to an access warrant. Our data contains only 4 cases where DOB attempted warrant execution, too few to draw statistical conclusions, but they illustrate that the mechanism exists. *Dependency:* Warrant escalation requires judicial cooperation and court capacity that DOB does not control. Implementation timelines for this component are uncertain and should be planned in coordination with the court system.

### Estimated Impact

If access-failure cases resolved no slower than DOB investigated-no-action cases (1,007-hour cap), the system-wide mean would drop from **496 hours (21 days) to 403 hours (17 days)** --- an **18.9% reduction**. Of the 107 access-failure cases, 87 exceed the 1,007-hour cap and would be reduced; 20 are already below it and are unchanged.

**Sensitivity to comparator choice.** The 1,007-hour cap uses all DOB investigated-no-action cases as the peer group, which includes complaint types simpler than those in the access-failure population. A stricter same-complaint-type comparator --- using the median for Building/Use cases that *were* successfully investigated (1,242 hours) --- would reduce the savings. We present 18.9% as the upper bound; actual savings depend on how well the scheduled-access protocol addresses the case-complexity confound.

---

## Recommendation 2: HPD 30-Day Escalation and Case Bundling

### The Problem

HPD receives clusters of complaints from the same building --- HEAT/HOT WATER, PLUMBING, and PAINT/PLASTER filings that reflect a single underlying maintenance failure. These are processed as independent service requests, each requiring separate inspector dispatch and separate tenant outreach. When the tenant cannot be reached by phone, the case stalls in a phone-outreach loop that can run for months.

### The Evidence

HPD handles 612 cases in our sample, second only to NYPD in volume but with resolution times 120 times longer (88-hour median vs. NYPD's 1.3 hours). The variation within HPD is stark:

| Resolution Path | Cases | Median Hours | Mean Hours |
|----------------|-------|-------------|-----------|
| Inspection completed | 421 | 124 | 362 |
| Phone outreach | 151 | 219 | 641 |
| Duplicate | 38 | 51 | 104 |

Phone-outreach cases --- where HPD calls the complainant but cannot resolve the issue by phone --- take nearly twice as long as inspected cases. The worst offenders are PLUMBING complaints resolved by phone (59 cases, 482-hour median) and PAINT/PLASTER phone cases (28 cases, 542-hour median).

The extreme tail tells the story most clearly: **78 HPD cases** exceed 720 hours (30 days), averaging 1,985 hours (83 days). Within this tail, PLUMBING accounts for 42 cases and PAINT/PLASTER for 34, with 2 HEAT/HOT WATER cases.

The NYS Comptroller's monitoring tool notes that complaint types co-occur geographically: "areas with high HEAT/HOT WATER complaints also tend to have high PLUMBING and PAINT/PLASTER complaints, suggesting building-level maintenance issues rather than isolated problems" (state-comptroller-monitoring.txt, Key Patterns). *Important caveat:* This source describes neighborhood-level co-occurrence, not building-level co-occurrence. Our dataset lacks street addresses, so we cannot directly verify whether the same buildings generate multiple complaint types. The bundling recommendation therefore rests on the plausible inference that neighborhood-level co-occurrence reflects building-level conditions --- an assumption that should be validated with address-level data before implementation.

Separately, the broader 311 system is under capacity pressure. The Mayor's Management Report documents 38.2 million annual contacts with a flat headcount of 379 staff, and the inbound **call answer rate dropped from 85% to 74%** (mmr-311-performance.txt). HPD's outbound phone follow-up is operationally distinct from the 311 call center, but the system-wide shift toward digital channels (web visits up 21%) creates an opportunity: moving HPD tenant outreach from phone to SMS/email/web would align with the channel shift already underway.

### The Recommendation

1. **Building-level case bundling** *(contingent on address-level validation).* When HPD receives multiple complaints from the same building address within a rolling 30-day window, bundle them into a single building inspection rather than dispatching separately for each complaint type. The inspector examines all reported conditions in one visit. *Prerequisite:* This component should not proceed until address-level co-occurrence is validated using the full 311 dataset (see Limitation 11). Our sample lacks addresses, so the building-level clustering premise is inferred from neighborhood-level patterns, not proven.
2. **30-day auto-escalation for phone-stall cases.** If an HPD case remains open for 30 days in a phone-outreach status, auto-escalate to an in-person inspection. *Policy context:* HPD's phone-outreach-first model may be a deliberate triage choice --- many housing complaints can be resolved through landlord contact without an inspector visit, preserving scarce field capacity. The 30-day trigger does not eliminate phone outreach; it imposes a time limit. Of 612 HPD cases, 534 (87%) resolve within 30 days under the current model. This recommendation targets only the 78-case tail (13%) where phone outreach has clearly stalled.
3. **Shift phone-outreach to digital channels.** The 311 system's channel shift is already underway (web visits up 21%, call volume declining). For non-emergency HPD complaints, replace phone-based follow-up with SMS/email notification and an online self-report form. This is consistent with the broader digital-first trend documented in the MMR (mmr-311-performance.txt, Total Contacts).

### Estimated Impact

Capping HPD cases at 720 hours (the 30-day auto-escalation threshold) would reduce the system-wide mean from **496 hours (21 days) to 453 hours (19 days)** --- an **8.7% reduction**. The 78 affected cases currently average 1,985 hours (83 days); bringing them to 30 days saves approximately 98,700 total resolution hours. *Resource tradeoff:* Auto-escalation to in-person inspection would generate up to 78 additional inspector dispatches. HPD uses phone outreach partly because inspector capacity is limited; this recommendation assumes that bundled inspections (addressing multiple complaints per building visit) partially offset the additional workload. If inspector capacity cannot absorb the increase, HPD may need to reallocate staff from lower-priority inspection categories.

---

## Recommendation 3: DOB Plan Review Fast-Track

### The Problem

DOB's administrative review cases --- complaints that are assessed at a desk rather than through field inspection --- split into two distinct groups. Some close quickly (within days), but many sit open for weeks or months. These are not complex enforcement cases requiring property access; they are decisions that can be made from existing documentation. (Some long-running admin-close cases may reflect deliberate monitoring rather than neglect --- see Limitations.)

### The Evidence

DOB has **144 admin-close cases** in our dataset --- complaints resolved with "reviewed this complaint and closed it" or "reviewed this complaint and determined that no further action was necessary." While the median is 80 hours (3.3 days), the distribution has a heavy tail:

| Percentile | Hours | Days |
|-----------|-------|------|
| 25th | 14 | 0.6 |
| 50th (median) | 80 | 3.3 |
| 75th | 362 | 15 |
| 90th | 1,413 | 59 |

The gap between the 25th and 75th percentiles is enormous: a quarter of admin-close cases resolve in under a day, but another quarter take over two weeks. **75 of 144 admin-close cases** (52%) exceed 72 hours --- meaning they take longer than three business days for what is fundamentally a desk decision.

The breakdown by complaint type reveals where the delays concentrate:

| Complaint Type | Admin-Close Cases | Median Hours | Cases Over 72h |
|---------------|-------------------|-------------|----------------|
| Elevator | 89 | 182 | 56 |
| Building/Use | 49 | 59 | 16 |
| General Construction/Plumbing | 6 | 74 | 3 |

Elevator complaints dominate the admin-close backlog (89 cases, 182-hour median). Some of these involve elevator registration or permit status checks that should be resolvable from DOB's own databases within hours. However, some elevator admin-close delays may reflect DOB waiting for a scheduled periodic inspection cycle (annual or semi-annual) to verify compliance --- not reviewer idleness. The 72-hour SLA should apply to desk-reviewable cases (registration lookups, permit verification), not to cases awaiting field confirmation on a statutory cycle.

The Comptroller's audit provides institutional context: DOB plan approval times have increased 80% citywide as application volume rose 106% (comptroller-audit-findings.txt, Finding 4). The citywide average for major alteration approvals reached **124 business days** in Q1 2024. While plan review and complaint review are formally separate workflows, both require DOB technical expertise. We infer --- but cannot confirm from public data --- that the same staff pool serves both queues, creating competition for reviewer time when plan backlogs grow. If DOB uses dedicated complaint reviewers, the queue-reordering component would be less effective, and the binding constraint would be reviewer headcount rather than prioritization.

The audit further found that **homeowners were issued "Failure to Comply" violations while their plans were still pending DOB approval** (Finding 5). This creates a perverse dynamic: complaints generate enforcement activity that itself depends on the same overburdened review pipeline.

### The Recommendation

1. **72-hour service standard for desk reviews.** Establish a formal service-level agreement: any DOB complaint that can be resolved through administrative review (no field inspection required) must be closed within 72 hours (3 business days). This matches the pace already achieved by the fastest quartile of admin-close cases.
2. **Complaint-prioritized queue reordering.** When DOB technical staff allocate time between plan reviews and complaint reviews, complaints with open 311 service requests should receive priority. This does not require additional staff --- it reorders the existing queue to ensure that 311 complaints are not indefinitely deprioritized behind developer-submitted plan applications.
3. **Auto-close for verifiable conditions** *(longer-term).* For complaint types where the relevant information exists in DOB databases (elevator registrations, certificates of occupancy, permit status), build an automated check that closes the complaint if the database shows compliance --- no human review needed. This component requires integration between 311's case management system and DOB's permit/registration databases, which is a technology project likely requiring 6--12 months, not a quick process fix. It should be scoped as a Phase 2--3 initiative, not Phase 1.

### Estimated Impact

Capping admin-close cases at 72 hours would reduce the system-wide mean from **496 hours (21 days) to 472 hours (20 days)** --- a **5.0% reduction**. The 75 affected cases currently average 819 hours (34 days); compressing them to 72 hours (3 days) saves approximately 56,000 total resolution hours.

---

## Combined Impact Model

The three recommendations target non-overlapping populations, verified by checking that no case matches more than one category's text criteria (0 overlaps in the data). Recommendation 1 addresses DOB access-failure cases (identified by "could not gain access" / "denied access" resolution text), Recommendation 2 addresses HPD long-running cases, and Recommendation 3 addresses DOB admin-close cases (identified by "reviewed this complaint and closed" resolution text). Different agencies and different resolution descriptions --- no double-counting.

| Recommendation | Cases | Mechanism | Hours Saved | Individual % |
|---------------|-------|-----------|------------|-------------|
| 1. DOB Access-Failure Protocol | 107 (87 above cap) | Cap at 1,007h (42 days) | 213,164 | 18.9% |
| 2. HPD 30-Day Escalation (+ bundling) | 78 | Cap at 720h (30 days) | 98,698 | 8.7% |
| 3. DOB Admin Review Fast-Track | 75 | Cap at 72h (3 days) | 56,031 | 5.0% |
| **Total** | **260** | | **367,893** | |

When all three are applied simultaneously:

| Metric | Baseline | After All Three | Change |
|--------|----------|-----------------|--------|
| System-wide mean | 496 hours (21 days) | 335 hours (14 days) | -161 hours (-7 days) |
| Percent reduction | --- | --- | **32.6%** |
| Total hours saved | --- | --- | 367,893 |
| Cases affected | --- | 260 of 2,275 | 11.4% of cases |

**The combined 32.6% ceiling reduction exceeds the 30% target** by targeting just 11.4% of cases --- the ones with the most disproportionate resolution times. The remaining 88.6% of cases are untouched.

**What this means for the typical complainant.** Because these recommendations target the extreme tail, the median resolution time (37 hours, or 1.5 days) would barely change. The average resident filing a noise or parking complaint would see no difference. The impact is concentrated on the ~260 people per year (in this sample's proportions) whose DOB or HPD cases currently take 1--6 months to close. Framing the 30% target in mean terms measures tail compression, not typical-case improvement --- an important distinction for setting public expectations.

The individual percentages (18.9 + 8.7 + 5.0 = 32.6) happen to sum to the combined figure because the three populations are strictly non-overlapping. Each case is affected by at most one recommendation.

**These are ceiling estimates, not forecasts.** The model assumes every affected case hits the cap exactly and that all three recommendations are fully implemented. Partial compliance, implementation lag, and the case-complexity confound discussed under Recommendation 1 would all reduce actual savings. A reasonable discount for implementation friction might be 20--30% (a professional judgment informed by the specific risk factors identified in each recommendation --- the case-complexity confound in Rec 1, the unvalidated building-level premise in Rec 2, and the elevator inspection cycle ambiguity in Rec 3 --- rather than a generic adjustment), yielding an effective reduction of **23--26%** --- below the 30% target. The ceiling estimate (33%) clears the target; the realistic estimate does not. Closing the gap would require either more aggressive caps, broader coverage (targeting additional case types), or achieving better-than-expected compliance on the three existing recommendations. We recommend presenting the 23--33% range to decision-makers, with 30% as an achievable stretch goal rather than a guaranteed outcome.

---

## Implementation Sequencing

The three recommendations have different implementation timelines and dependencies:

**Phase 1 (0--3 months): DOB Admin Review SLA and Queue Reordering (Recommendation 3, components 1--2)**
This requires the least operational change --- it is a queue reordering and service-level commitment, not a new process. DOB already resolves 25% of admin-close cases in under a day, proving the capability exists. The 72-hour SLA formalizes what the fastest reviewers already do. The auto-close component (Recommendation 3, component 3) is a technology project requiring database integration and should be scoped for Phase 2--3.

**Phase 2 (3--6 months): HPD Case Bundling and Auto-Escalation (Recommendation 2)**
The 30-day auto-escalation is a simple rule-based trigger that can be implemented quickly. Bundling requires changes to HPD's case management system to identify co-located complaints and assign them to the same inspector. Address-matching logic in 311 data is non-trivial (inconsistent abbreviations, unit numbers, cross-street formats) and may require address normalization as a prerequisite. Both components require coordination with HPD field operations to ensure inspector capacity can absorb the redirected caseload.

**Phase 3 (6--12 months): DOB Access-Failure Protocol (Recommendation 1)**
The scheduled-access and virtual-triage components require the most significant operational change, including new workflows for complainant/owner contact, a triage decision tree for desk-reviewable cases, and coordination with DOB's legal team on warrant escalation timelines (which depend on court system capacity DOB does not control). The warrant-escalation component (sub-recommendation 3) is the most speculative --- based on only 4 observed cases --- and should be treated as a pilot rather than a guaranteed workflow.

*Why not start with the largest impact?* Recommendation 1 delivers 73% of total hours saved but requires the most operational retooling. Starting with quick wins (Phases 1--2) builds agency buy-in and demonstrates measurable progress while the more complex DOB access-failure protocol is designed and piloted. Decision-makers who prefer an impact-first approach could begin Rec 1 piloting in parallel with Phase 1, accepting a longer ramp-up.

---

## Limitations and Caveats

1. **Sample, not census.** The 2,275 cases in `ops_data.csv` are a stratified sample whose stratification methodology is not documented. Actual citywide volumes are orders of magnitude larger (74,035 DOB complaints alone in the Comptroller's audit period). If the sample overrepresents DOB relative to citywide share, the 496-hour system-wide mean --- and the 33% reduction target --- may not generalize. The within-agency patterns (access failure, phone stall, admin close) should be more robust to sampling design.

2. **Counterfactual assumptions.** The impact model produces ceiling estimates, not forecasts. It assumes every affected case hits the target cap exactly and that all three recommendations are fully implemented. Partial compliance, implementation lag, and edge cases would reduce actual savings. A 20--30% implementation discount is reasonable, yielding an effective reduction of 23--26%.

3. **Mean vs. median.** The 30% target is framed in terms of mean resolution time. Means are sensitive to extreme values --- a small number of very long cases can dominate the average. Median-based targets would be more robust but would require different interventions (the median is already 37 hours, or 1.5 days, driven by fast NYPD closures).

4. **Duplicate requests and Rec 2 validity.** The NYS Comptroller's monitoring tool documents that a single issue can generate 3--5+ separate 311 entries (state-comptroller-monitoring.txt, Data Quality Considerations). This directly affects Recommendation 2: HPD cases from the same building for related conditions --- the exact pattern the bundling recommendation targets --- are the complaint type most likely to include duplicates. If some of the 78 tail cases are duplicates of each other, the savings estimate is inflated and the bundling recommendation is partially redundant with existing duplicate-closure processes. Address-level deduplication analysis is needed before implementation.

5. **Closed-case selection bias.** The dataset includes only closed cases. If the longest-running DOB access-failure cases are still open (plausible, given 87-day medians), the resolution time estimates in this report *understate* the true burden. Conversely, if DOB closes hopeless cases early by advising complainants to refile, the closed-case distribution may not represent actual complainant experience.

6. **Temporal gap.** The Comptroller's audit covers 2022--2023; the operational data covers April--September 2025. DOB may have implemented partial reforms in the intervening 2--3 years. We assume the institutional patterns persist, but this should be verified with DOB before finalizing recommendations.

7. **No headcount assumption.** All three recommendations are designed to work within existing staffing levels. However, if DOB or HPD staff are already at capacity (as the 80% increase in plan review times suggests), process reforms may shuffle the bottleneck rather than eliminate it. Recommendation 2's auto-escalation to inspection would generate additional field dispatches that displace other inspection work. The Mayor's Management Report shows 311 operating with 379 staff against a plan of 396 --- a 4.3% vacancy rate that constrains surge capacity (mmr-311-performance.txt, Agency Resources).

8. **Agency pushback.** DOB may argue that scheduled-access appointments for Illegal Conversion cases tip off violators, undermining enforcement effectiveness. This is a legitimate concern addressed through risk-tiered scheduling in Recommendation 1. HPD may note that phone outreach is a less invasive first step than inspection and that inspector capacity constraints make auto-escalation impractical without reallocation. Both agencies may point out that some admin-close or phone-outreach delays serve operational purposes (monitoring, consolidation) rather than representing pure waste.

9. **Equity implications.** The Comptroller's audit found that DOB penalties fall disproportionately on lower-income and minority communities, with 7 of 10 top penalty districts below the citywide median income (comptroller-audit-findings.txt, Finding 2). Faster enforcement could intensify these disparities if not paired with outreach and compliance assistance. Recommendation 1's scheduled-access component partially addresses this by giving property owners advance notice, but the equity dimension requires ongoing monitoring.

10. **Seasonal effects.** HPD HEAT/HOT WATER complaints are seasonal (October--April). Our sample covers April--September, which may underrepresent heating cases and overrepresent warm-weather complaint types. The HPD bundling recommendation's impact may vary by season.

11. **Building-level co-occurrence is inferred, not proven.** Recommendation 2 assumes that neighborhood-level complaint co-occurrence (documented by the NYS Comptroller) reflects building-level clustering. Our dataset lacks street addresses, so we cannot verify this directly. Address-level analysis from the full 311 dataset should be conducted before investing in building-level bundling infrastructure.

12. **SLA moral hazard.** The 72-hour service standard for DOB admin reviews (Recommendation 3) could incentivize premature closures: if reviewers face a hard deadline, the path of least resistance is to close cases as "no further action necessary" rather than conduct thorough review. This would reduce resolution times on paper while degrading enforcement quality. Any SLA implementation should include a quality-assurance sample audit (e.g., 10% random review of cases closed within 24 hours of the deadline) to detect and correct gaming behavior.
