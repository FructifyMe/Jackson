# SavATree Satellite Lead Generation — Project Plan

**Project:** Proactive Lead Generation via Satellite Canopy Analysis
**Client/User:** Mike Fructify (project lead)
**End User:** Jackson Fructify — Arborist / Sales PM, SavATree Middleton branch
**Company:** [SavATree](https://www.savatree.com/) (Middleton, MA branch)
**Working Folder:** `C:\Users\MikeF\Desktop\Cassidy\Claude CoWork Jackson`
**Created:** March 3, 2026
**Status:** Phase 1 — Research & Tool Building

---

## Company Profile

- **Full Name:** SavATree (www.savatree.com)
- **Branch:** Middleton, Massachusetts (12 years in operation)
- **Coverage:** Northern MA, Essex County, Middlesex County
- **Certifications:** ISA Certified Arborists, ISA Tree Risk Assessment Qualified (TRAQ), ASCA Registered Consulting Arborists, ISA Board Certified Master Arborists
- **Standards:** ANSI A300 Part 9 (Probability x Consequences = Risk)
- **Consulting Group:** SavATree Consulting Group — tree risk assessments, inventories, appraisals, expert witness, preservation planning
- **Services:** Tree removal, pruning, fertilization, disease treatment, plant health care, pest control, lawn care, organic services, ArborHealth treatments
- **Key differentiator for this project:** ISA TRAQ-qualified consultants performing industry-standard risk assessments

## Problem Statement

SavATree Middleton currently relies on **inbound leads only** — form fills, Facebook ads, Facebook messages, and phone calls. There is no proactive outbound lead generation. This project creates a system that uses satellite/aerial imagery to detect tree canopy decline, then targets property owners who likely need arborist services — **before they know they need them**.

## Target Territory

Six towns north of Boston within the Middleton branch service area:

| Town | County | Why Selected |
|------|--------|-------------|
| Melrose | Middlesex | Dense residential + commercial, mature tree canopy |
| Stoneham | Middlesex | Mixed residential/commercial, suburban canopy |
| Wilmington | Middlesex | Growing town, newer developments + mature areas |
| Wakefield | Middlesex | Lake Quannapowitt area, established neighborhoods |
| Reading | Middlesex | High-value residential, town center commercial |
| North Reading | Middlesex | Mix of residential + Route 28 commercial corridor |

## Strategy: Who We Target (Priority Order)

Based on the Lead Qualification Framework, we target in this order:

1. **S-Tier: HOA / Condo Communities** (Score 9.5/10) — Largest canopy footprint, legal obligation to maintain, board fiduciary duty, recurring contract potential $5K–$50K+/year
2. **S-Tier: Commercial Properties** (Score 9.0/10) — Liability exposure, insurance premium reduction (~12%), dedicated facility budgets
3. **A-Tier: Municipal / Institutional** (Score 8.0/10) — Public safety mandate, budget cycles, large tree inventories
4. **A-Tier: Multifamily Rental** (Score 8.0/10) — Tenant safety, landlord liability, property management companies as decision-makers
5. **B-Tier: High-value Residential ($750K+)** (Score 5.0/10) — Curb appeal, insurance, property value (trees add 7-15%)
6. **C-Tier: Standard Residential** (Score 3.0/10) — One-time service, small contract value

## Technical Approach

### Detection Methods
- **Primary:** NDVI (Normalized Difference Vegetation Index) change detection via Sentinel-2 (10m, free, 5-day revisit)
- **Confirmation:** NAIP aerial imagery (0.6m resolution, free, RGBNIR)
- **Platform:** Google Earth Engine (Python API, free)
- **Parcel Data:** MassGIS (free, includes land use codes for property classification)
- **Supporting:** NBR for storm damage, NDWI for moisture stress, Red Edge for early chlorophyll issues

### Lead Scoring Model (4 Factors, Weighted)
| Factor | Weight | Source |
|--------|--------|--------|
| Canopy Decline Severity | 30% | NDVI change detection |
| Property Classification | 30% | MassGIS land use codes |
| Liability Exposure | 25% | ISA risk rating + proximity + urgency |
| Property Value & Scale | 15% | Assessor data + tree count |

### Pipeline Tools
- **Apollo** — Decision-maker identification (HOA board presidents, property managers, facility managers)
- **Clay** — Contact enrichment and research
- **Gmail** — Outreach execution
- **Google Calendar** — Meeting scheduling
- **Smartsheet** — Pipeline tracking and lead management
- **Google Drive** — Document storage and collaboration

## MVP Phases

### Phase 1: HOA & Commercial (Weeks 1–2)
- [ ] Identify all HOA/condo communities in 6 towns via MassGIS land use data
- [ ] Identify commercial properties with significant tree canopy
- [ ] Run Sentinel-2 NDVI change detection (summer 2023 vs summer 2025)
- [ ] Cross-reference with NAIP for property-level confirmation
- [ ] Score and rank top 20–30 flagged properties
- [ ] Use Apollo/Clay to find decision-makers
- [ ] Generate personalized outreach materials with satellite imagery

### Phase 2: Multifamily & Institutional (Weeks 3–4)
- [ ] Expand to multifamily and municipal/institutional properties
- [ ] Refine scoring model based on Phase 1 conversion data
- [ ] Build Smartsheet pipeline tracker
- [ ] Create email sequences for different property types

### Phase 3: High-value Residential (Weeks 5–6)
- [ ] Target residential properties $750K+ with detectable canopy decline
- [ ] Lighter-touch outreach (door hangers, direct mail with satellite images)
- [ ] Measure ROI and refine approach

## Deliverables Created

| File | Description | Status |
|------|-------------|--------|
| `savatree-canopy-lead-gen-feasibility.html` | Feasibility study — detection methods, data sources, MVP architecture | Complete |
| `savatree-lead-qualification-framework.html` | Lead qualification — tier rankings, urgency drivers, scoring model, pitch language | Complete |
| `savatree-isa-digital-assessment.html` | Interactive ISA form with NDVI pre-fill, auto-risk calculation, and Lead Score tab | Complete |
| `ISA-Basic-Tree-Risk-Form-fillable.pdf` | Official ISA form (uploaded by Mike) | Reference doc |
| `PROJECT.md` | This file — project plan and overview | Current |
| `MEMORY.md` | Compaction recovery — key decisions, context, and state | Current |
| `CHANGELOG.md` | Session-by-session log of what was done | Current |
| `SATELLITE-TEST-GUIDE.md` | Setup and usage guide for running satellite analysis | Current |
| `gee-ndvi-wakefield-test.js` | GEE JavaScript — paste into code.earthengine.google.com for instant NDVI map | Ready to test |
| `ndvi_change_detection.py` | Python pipeline — local automated analysis with PNG/JSON/CSV output | Ready to test |

## Budget Approach

MVP/free tier first. Only discuss paid tools if the approach generates real qualified leads. Current stack is entirely free:
- Sentinel-2: Free (ESA Copernicus)
- NAIP: Free (USDA)
- Google Earth Engine: Free (research/non-commercial)
- MassGIS: Free (state government)
- Apollo/Clay/Smartsheet: Existing subscriptions

## Key Contacts & Roles

| Person | Role | Notes |
|--------|------|-------|
| Mike Fructify | Project Lead | Building the system, technical decisions |
| Jackson Fructify | End User — Arborist/Sales PM | Will use the tools in the field, SavATree Middleton |
| SavATree Middleton branch | Employer | ISA-certified, TRAQ-qualified, 12 years in northern MA |

## References

- [SavATree Homepage](https://www.savatree.com/)
- [SavATree Tree Risk Assessment](https://www.savatree.com/consulting/tree-risk-assessment-mitigation/)
- [SavATree Middleton Branch](https://www.savatree.com/locations/middleton-massachusetts/)
- [SavATree Consulting Group](https://www.savatree.com/consulting/)
- ISA TRAQ Standards (ANSI A300 Part 9)
