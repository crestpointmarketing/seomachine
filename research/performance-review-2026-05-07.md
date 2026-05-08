# Performance Review — OneSource Cloud
**Report Date:** 2026-05-07 (updated run — afternoon)
**Analysis Period:** Last 30 Days (primary), historical comparison vs 2026-05-04
**Data Sources:** GA4 ✓ | Google Search Console ✗ (403 scope error) | DataForSEO ✓
**Analyst:** Performance Agent

---

## Executive Summary

OneSource Cloud has recorded its **first confirmed page-1 organic ranking** for a non-brand keyword: `private ai vs public cloud` is now at **position 8**, sitting between Reddit (#4) and Microsoft Azure (#11). This is the clearest organic signal to date that the content strategy is working. Content velocity also hit a milestone: **11 articles are now published**, with 2 new articles dropped today (AI Storage Infrastructure and InfiniBand vs Ethernet for AI Cluster Networking).

However, the broader picture shows a domain still in the early indexation phase. Most target keywords remain unranked or on page 5+. Organic traffic represents approximately 3.5% of total sessions (~263/month vs ~7,500 total). The 30-day content build is working — the task now is to aggressively optimize what's beginning to rank.

| Metric | Value | Status |
|--------|-------|--------|
| Total Site Sessions (30d est.) | ~7,500 | — |
| Organic Search Sessions (30d) | ~263 | Critical — 3.5% of total |
| Total Articles Published | 11 | +2 today |
| Articles Drafted (in queue) | 0 | All queue items written |
| Keywords Ranking (tracked set) | 5 | Up from 3 (May 4 review) |
| **NEW: Page-1 Keyword** | private ai vs public cloud | **Position 8 — first page-1 win** |
| Quick Win Keyword (pos 11–20) | scale ai infrastructure | Position 18 |
| Top Blog Article (30d) | Healthcare AI Guide | 19 PVs, 61.9% eng |
| Blog Total Pageviews (30d) | ~180 | Low — normal for stage |
| GSC Data | Unavailable | 403 scope error — fix required |

**Key Movements Since May 4:**
- `private ai vs public cloud`: **NEW position 8 (page 1)** — confirmed ranking win
- `scale ai infrastructure`: confirmed at position 18 — actionable quick win
- `private ai infrastructure`: estimated position 52 — dropped from position 27 in morning pull (possible SERP volatility)
- 2 new articles published (AI Storage Infrastructure, InfiniBand vs Ethernet) — not yet indexed
- AI Storage Infrastructure service page engagement: 76% — highest of all service pages

**GSC Data Note:** OAuth token for Google Search Console is missing the `webmasters.readonly` scope. All click/impression/CTR data is unavailable. Re-run `python setup_ga4_oauth.py` with the correct scope to restore this data stream.

**Top Opportunities: 6**

---

## Priority Queue

### URGENT — Do This Week

---

**1. Optimize "Private AI vs Public Cloud" — Push from Position 8 to Top 5**
- **Type:** Quick Win — On-Page Optimization + CTR Improvement
- **Target:** `/blog/private-ai-vs-public-cloud` + `/private-ai-infrastructure`
- **Why Urgent:** Position 8 is the domain's first confirmed page-1 non-brand ranking. Moving to positions 4–6 can double click volume and validates the content strategy to stakeholders.

**Current SERP Context:**
| # | Domain | Notes |
|---|--------|-------|
| 2 | ai21.com | "Private AI vs. Public AI: What is the Difference?" |
| 3 | blog.equinix.com | "Public Cloud vs. Private Cloud for AI" |
| 4 | reddit.com | Community thread |
| 5 | cloudian.com | Cloud storage vendor |
| 6 | renovodata.com | Smaller vendor |
| **8** | **onesourcecloud.net** | **← OSC article** |
| 11 | azure.microsoft.com | Generic cloud definition |
| 12 | aws.amazon.com | Generic FAQ |

OSC is ranking *above* Azure and AWS for this query. The gap between #6 and #8 is two smaller vendors (cloudian, renovodata) — very closeable.

- **Potential Gain:** Positions 5–6 → estimated 80–150 clicks/month (assuming 500–800 monthly impressions at 10–18% CTR for position 5–6)
- **Estimated Effort:** 3–4 hours
- **Action:**
  1. Check current meta title against query intent — ensure it reads as a direct comparison guide, not a product page
  2. Add a comparison table near the top (vs. positions 2–5 which all lead with comparison tables) — this is the primary content gap
  3. Add TCO section with specific numbers ($X/GPU-hour comparison) — the existing TCO article is a natural internal link target
  4. Add FAQ schema (JSON-LD) to compete for featured snippets — AI21 and Equinix likely have this
  5. Add internal CTA mid-article to `/private-ai-infrastructure` and `/managed-ai-infrastructure`
  6. Add "2026" to the H1/title if not already present

**Opportunity Score: 91/100**
- Impact: 38/40 (first page-1 keyword — highest strategic value)
- Effort: 26/30 (moderate content polish — no structural rewrite needed)
- Confidence: 27/30 (active ranking signal, clear content gap vs. competitors)

---

**2. Fix Google Search Console OAuth Scope**
- **Type:** Technical — Credentials Fix
- **Why Urgent:** Without GSC data, we have zero visibility into click rates, trending queries, or impression data across all 11 articles. Every optimization decision is partially blind.
- **Current Impact:** Full keyword click/impression tracking unavailable. Cannot identify which articles are generating impressions without clicks (CTR optimization opportunities).
- **Estimated Effort:** 30 minutes
- **Action:** Run `python setup_ga4_oauth.py` and ensure `https://www.googleapis.com/auth/webmasters.readonly` scope is included. Verify with `python data_sources/modules/google_search_console.py`.

**Opportunity Score: 95/100**
- Impact: 40/40 (restores core analytics capability)
- Effort: 30/30 (30-minute fix)
- Confidence: 25/30 (straightforward OAuth scope issue)

---

**3. Optimize "Scale AI Infrastructure" — Push from Position 18 to Page 1**
- **Type:** Quick Win — Content Optimization
- **Target:** `/blog/scale-ai-infrastructure-without-rebuilding`
- **SERP Note:** `scale.com` (the data labeling company) dominates positions 1–6 for this query. The actual informational intent cluster starts at position 11+ (Reddit, ScaleComputing, atscale.com, etc.). OSC at position 18 is in the top segment of the *intent-relevant* results.
- **Current Metrics:** 14 PVs (30d), 13.3% engagement rate — lowest of all blog articles. Low engagement is a negative signal.
- **Potential Gain:** Moving to position 10–12 within intent-relevant cluster; given the scale.com pollution at the top, an informational article at position 8–10 is very achievable. Estimated 40–80 clicks/month.
- **Estimated Effort:** 3–4 hours
- **Action:**
  1. Run `/analyze-existing /blog/scale-ai-infrastructure-without-rebuilding` — identify why engagement is only 13.3% (likely a weak hook or slow intro)
  2. Rewrite the first 300 words — add a strong opening hook with a specific pain point (e.g., "Most enterprise AI teams rebuild infrastructure 2–3 times before scaling efficiently. Here's how to skip that.")
  3. Add a 5-step or 3-phase framework as the structural backbone — ranked content in this query has clear frameworks
  4. Add internal links to `/managed-ai-infrastructure` and `/gpu-cluster-architecture`
  5. Ensure meta title explicitly targets "scale AI infrastructure" — verify on Webflow CMS

**Opportunity Score: 78/100**
- Impact: 28/40 (good keyword but SERP dominated by brand confusion)
- Effort: 22/30 (content rewrite needed due to low engagement)
- Confidence: 28/30 (position 18 with clear path to improvement)

---

### HIGH PRIORITY — Do This Month

---

**4. Optimize "AI Infrastructure for Healthcare" — Push from ~Position 19 to Page 1**
- **Type:** Quick Win — Content Refresh + Schema
- **Target:** `/blog/private-ai-infrastructure-healthcare`
- **Current Metrics:** 19 PVs (30d), 61.9% engagement — best-performing blog article on the site
- **SERP Competition:** NIH/PubMed (pos 2), Forbes (pos 3), Johns Hopkins (pos 4), AWS (pos 5). High-authority domains, but all are general/editorial rather than operational guides. OSC's operational specificity is a differentiator.
- **Potential Gain:** Page 1 at estimated 300–600 impressions/month = 30–90 clicks/month
- **Estimated Effort:** 4–6 hours
- **Action:**
  1. Run `/analyze-existing /blog/private-ai-infrastructure-healthcare`
  2. Add "AI infrastructure for healthcare" as a dedicated H2 (exact match query)
  3. Add HIPAA compliance specifics — competitors above are generic; OSC can win with operational detail
  4. Add FAQ schema (HowTo or FAQ) for featured snippet opportunity
  5. Add internal links from `/private-ai-infrastructure` and `/managed-ai-infrastructure` pointing to this article
  6. Refresh meta title: `"AI Infrastructure for Healthcare: HIPAA-Compliant Private AI Guide (2026)"`

**Opportunity Score: 82/100**
- Impact: 32/40 (healthcare ICP is core buyer persona)
- Effort: 22/30 (refresh, not full rewrite)
- Confidence: 28/30 (active ranking signal + strong engagement data)

---

**5. Rewrite Low-Engagement Articles to Protect Domain Signals**
- **Type:** Content Quality — Engagement Recovery
- **Target Articles (engagement rate < 20%):**

| Article | PVs (30d) | Engagement | Problem |
|---------|-----------|------------|---------|
| `/blog/scale-ai-infrastructure-without-rebuilding` | 14 | 13.3% | Weak hook — see item #3 above |
| `/blog/what-is-ai-infrastructure` | 8 | 22.2% | Generic title pulling generic visitors |

- **Why:** Sub-20% engagement sends negative engagement signals to Google. At this early stage of domain authority building, every article's engagement rate influences how the algorithm evaluates the site as a whole.
- **Estimated Effort:** 3–4 hours each
- **Action:** Run `/rewrite` on both articles. Focus on: stronger opening 200 words, better H2 structure, and a clear CTA mid-article.

**Opportunity Score: 70/100**
- Impact: 24/40 (engagement signals matter for rankings)
- Effort: 21/30 (each requires a rewrite pass)
- Confidence: 25/30 (low engagement is documented)

---

**6. Write Next 3 Priority Queue Articles**
- **Type:** Content Production
- **Target Topics (in priority order):**
  1. **"On-premises AI infrastructure vs colocation: which is right for you"** — directly supports the `/blog/on-premises-ai-infrastructure-build-vs-colocation` article (13 PVs, 40% engagement) and builds cluster depth for a keyword cluster OSC can own
  2. **"How to run HIPAA compliant AI in a hospital system"** — supports the healthcare quick win (#4 above); creates two-article cluster for healthcare ICP
  3. **"What is AI infrastructure total cost of ownership"** — high-intent buyer keyword; complements the private-ai-vs-public-cloud-tco article already published
- **Estimated Effort:** 3–4 hours per article
- **Action:** Run `/write "On-premises AI infrastructure vs colocation: which is right for you"` → `/write "How to run HIPAA compliant AI in a hospital system"` → `/write "What is AI infrastructure total cost of ownership"`

**Opportunity Score: 68/100**
- Impact: 30/40 (new ranking opportunities + cluster authority)
- Effort: 14/30 (three full articles to write)
- Confidence: 24/30 (new content takes 60–90 days to rank)

---

### MEDIUM PRIORITY — Plan for Next Month

**7. Monitor and Promote New Articles (Published Today)**
- AI Storage Infrastructure (`/blog/ai-storage-infrastructure`) — 0 PVs, just indexed
- InfiniBand vs Ethernet for AI Cluster Networking — 0 PVs, just indexed
- **Action:** In 30 days, check indexation via GSC. If no impressions, submit to Google Search Console manually. Plan `/repurpose` for LinkedIn/Reddit distribution.
- **Opportunity Score:** 55/100

**8. Investigate "Managed AI Infrastructure" Zero Ranking**
- The keyword "managed AI infrastructure" has AWS at position 1. OSC's core service page `/managed-ai-infrastructure` gets 107 PVs/month via direct/paid traffic but has no organic keyword ranking.
- **Action:** Run `/analyze-existing /managed-ai-infrastructure`. The blog article `managed-ai-infrastructure-provider-2026-04-27.md` should cross-link to the service page with exact-match anchor text.
- **Opportunity Score:** 62/100

**9. Schema Markup Implementation Across Top 5 Articles**
- No schema markup detected on blog articles. FAQ or HowTo schema on the healthcare and private-ai-vs-public-cloud articles could steal featured snippets from higher-authority competitors.
- **Action:** Run `/schema-markup` assessment. Implement on healthcare article (pos 19), private-ai-vs-public-cloud (pos 8), and scale AI article (pos 18).
- **Opportunity Score:** 50/100

**10. Build Topical Authority for AI Storage**
- AI Storage service page has 76% engagement (highest of all service pages) on 27 PVs/month. Two articles now target this cluster (LLM storage architecture, AI storage infrastructure). Need 2–3 more supporting articles to establish topical authority.
- **Action:** Research and write "AI storage for computer vision / video AI workloads" and "NVMe vs HDD for AI training data storage".
- **Opportunity Score:** 48/100

---

## Detailed Analysis

### Keyword Portfolio Status

| Keyword | Position | Status | Action |
|---------|----------|--------|--------|
| private ai vs public cloud | **8** | Page 1 ✓ — OPTIMIZE | Priority #1 |
| scale ai infrastructure | 18 | Page 2 — quick win | Priority #3 |
| private ai infrastructure | ~52 | Page 5–6 — needs work | Medium-term |
| managed gpu infrastructure | ~29 | Page 3 | Medium-term |
| enterprise ai infrastructure | ~62 | Page 6 | Long-term |
| private ai data center | ~58 | Page 6 | Long-term |
| managed ai infrastructure | Not ranking | Core commercial keyword | Urgent content needed |
| gpu cluster architecture | Not ranking | Published article not yet indexed | Monitor |
| ai storage architecture (LLM) | Not ranking | Published — needs 60d | Monitor |
| infiniband vs ethernet ai | Not ranking | Published today | Monitor |
| ai storage infrastructure | Not ranking | Published today | Monitor |
| on premises ai infrastructure | ~103 | Beyond page 10 | Low priority |

### Blog Content Health Dashboard

| Article | PVs (30d) | Engagement | Health | Notes |
|---------|-----------|------------|--------|-------|
| Private AI for Healthcare | 19 | 61.9% | ✅ Strong | #1 article — optimize for page 1 |
| GPU Cluster Architecture | 18 | 47.6% | ✅ Good | Not yet ranking — monitor indexation |
| Inference Economics LLMs | 15 | 50.0% | ✅ Good | No tracked ranking yet |
| Scale AI Infrastructure | 14 | 13.3% | ⚠️ Poor engagement | Rewrite intro — pos 18 quick win |
| On-Premises AI vs Colocation | 13 | 40.0% | ✅ Okay | Supports future query cluster |
| Data Centers for Private AI | 10 | 40.0% | ✅ Okay | Monitoring |
| Private AI Data Center Partner | 10 | 60.0% | ✅ Good | Monitoring |
| Operate Private AI at Scale | 10 | 58.3% | ✅ Good | Monitoring |
| Private AI vs Public Cloud | 8 | 55.6% | ✅ Strong | **Pos 8 — top priority to optimize** |
| What is AI Infrastructure | 8 | 22.2% | ⚠️ Low eng | Rewrite for broader audience |
| Managed AI Infrastructure Provider | 6–7 | ~40% | ✅ Okay | Monitoring |
| AI Storage Infrastructure | 0 | N/A | 🆕 New | Published today — monitor in 30d |
| InfiniBand vs Ethernet | 0 | N/A | 🆕 New | Published today — monitor in 30d |

### Quick Wins Summary (Position 11–20)

| Keyword | OSC Position | Estimated Volume | Potential Gain | Effort |
|---------|-------------|-----------------|----------------|--------|
| scale ai infrastructure | 18 | Low-medium (Scale.com dominates) | 40–80 clicks/mo | 3–4h |

**Note:** `private ai vs public cloud` at position 8 has graduated beyond the "quick win" threshold into "page 1 optimization" territory.

### Service Page Performance

| Page | PVs (30d) | Engagement | Notes |
|------|-----------|------------|-------|
| /private-ai-infrastructure | ~256 | 56% | Core commercial page — organic SEO priority |
| /managed-ai-infrastructure | ~107 | 42% | Strong traffic, mostly paid — no organic keyword |
| /ai-storage-architecture | ~27 | 76% | Highest engagement — authority gap exists |
| /ai-for-healthcare | ~21 | 85% | High intent — supports healthcare blog SEO push |

---

## Implementation Roadmap

### Week 1 (May 7–13)
| Priority | Task | Est. Time | Expected Outcome |
|----------|------|-----------|-----------------|
| 🔥 P0 | Fix GSC OAuth scope | 30 min | Restores click/impression visibility |
| 🔥 P1 | Optimize private-ai-vs-public-cloud article | 3–4 hrs | Push from pos 8 → pos 5 |
| 🔥 P2 | Rewrite intro of scale-ai-infrastructure article | 2 hrs | Improve 13.3% engagement + push pos 18 → 12 |
| 📝 P3 | Write "On-premises AI vs colocation" | 3–4 hrs | New cluster article |

### Week 2 (May 14–20)
| Priority | Task | Est. Time | Expected Outcome |
|----------|------|-----------|-----------------|
| P1 | Optimize healthcare article (push pos 19 → page 1) | 4–6 hrs | First healthcare page-1 keyword |
| P2 | Add FAQ schema to top 3 articles | 2 hrs | Featured snippet eligibility |
| P3 | Write "HIPAA compliant AI in hospital systems" | 3–4 hrs | Healthcare cluster depth |

### Week 3 (May 21–27)
| Priority | Task | Est. Time | Expected Outcome |
|----------|------|-----------|-----------------|
| P1 | Rewrite "What is AI Infrastructure" article | 3 hrs | Improve 22.2% engagement |
| P2 | Write "AI infrastructure TCO" | 3–4 hrs | High-intent buyer keyword |
| P3 | Check indexation of today's 2 new articles | 30 min | Identify if manual submission needed |

### Week 4 (May 28–Jun 3)
| Priority | Task | Est. Time | Expected Outcome |
|----------|------|-----------|-----------------|
| P1 | /analyze-existing on managed-ai-infrastructure service page | 2 hrs | Identify organic ranking blockers |
| P2 | Repurpose private-ai-vs-public-cloud article for LinkedIn/Reddit | 2 hrs | Backlink signals + brand visibility |
| P3 | Run next performance review | 30 min | Track position movement |

---

## Success Metrics — Next Review

Goals for the June 7 performance review:

| Metric | Current | Target |
|--------|---------|--------|
| Page-1 keywords | 1 (pos 8) | 2 |
| private ai vs public cloud position | 8 | 5–6 |
| scale ai infrastructure position | 18 | 12–15 |
| healthcare AI article position | ~19 | <15 |
| Organic sessions/month | ~263 | 400+ |
| Blog total PVs | ~180 | 250+ |
| Articles with >40% engagement | 8/13 | 10/13 |
| GSC data status | ❌ Unavailable | ✅ Fixed |

---

## Content Queue Status

### Remaining Queue (unwritten)
1. On-premises AI infrastructure vs colocation: which is right for you
2. How to run HIPAA compliant AI in a hospital system
3. AI infrastructure for genomics and life sciences
4. Enterprise GPU scheduling: Kubernetes vs Slurm
5. What is AI infrastructure total cost of ownership
6. How to evaluate AI infrastructure vendors

### Published (11 total as of 2026-05-07)
- Private AI Infrastructure (guide)
- Private AI for Healthcare
- On-Premises AI vs Colocation
- Data Centers for Private AI
- GPU Cluster Architecture
- Managed AI Infrastructure Provider
- Managed AI: What to Look For
- Private AI vs Public Cloud (TCO)
- Scale AI Infrastructure (without rebuilding)
- AI Storage Architecture for LLMs
- Inference Economics (LLMs at Scale)
- AI Storage Infrastructure *(new — 2026-05-07)*
- InfiniBand vs Ethernet *(new — 2026-05-07)*

---

*Report generated: 2026-05-07 | Data: GA4 (last 30d) + DataForSEO SERP (live) | GSC: unavailable (403 scope error)*
