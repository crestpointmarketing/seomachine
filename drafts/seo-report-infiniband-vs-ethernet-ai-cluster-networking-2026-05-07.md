# SEO Audit Report: InfiniBand vs Ethernet for AI Cluster Networking

**File:** `drafts/infiniband-vs-ethernet-ai-cluster-networking-2026-05-07.md`
**Date:** 2026-05-07
**Auditor:** SEO Optimizer Agent

---

## Overall SEO Score: 81 / 100

| Category | Score | Max |
|---|---|---|
| Keyword Optimization | 17 | 20 |
| Content Quality & Depth | 19 | 20 |
| Heading Structure | 16 | 20 |
| Meta Elements | 12 | 15 |
| Link Profile | 9 | 15 |
| Readability | 8 | 10 |
| **Total** | **81** | **100** |

---

## 1. Keyword Density Analysis

**Primary keyword:** `InfiniBand vs Ethernet for AI cluster networking`
**Word count:** ~3,100 words

| Term / Phrase | Est. Occurrences | Density | Status |
|---|---|---|---|
| InfiniBand | ~50 | ~1.6% | ✅ In range |
| Ethernet | ~38 | ~1.2% | ✅ In range |
| AI cluster / AI clusters | ~16 | ~0.5% | ✅ Adequate |
| RDMA | ~13 | ~0.4% | ✅ Good |
| RoCEv2 | ~19 | ~0.6% | ✅ Good |
| networking | ~26 | ~0.8% | ✅ Natural |
| full primary phrase (exact) | ~3 | ~0.1% | ⚠️ Low (expected for 7-word phrase) |
| "InfiniBand vs Ethernet" (partial) | ~7 | ~0.2% | ✅ Acceptable |

**Assessment:** Individual keyword components are well-distributed at 1.2–1.6%, which is healthy for a technical article. The full 7-word phrase appears three times, which is appropriate — forcing exact-phrase repetition at this length would create unnatural copy. No stuffing detected.

**Recommendation:** Ensure the exact phrase `InfiniBand vs Ethernet for AI cluster networking` appears at least once more in the Conclusion section (currently it appears in the intro and two H2 headings). One additional natural placement in the conclusion would reinforce signal without stuffing.

---

## 2. Heading Structure

### Structure Map

```
H1: InfiniBand vs Ethernet for AI cluster networking: 2026 guide ✅
  H2: Why AI cluster networking is different ✅
    H3: The all-reduce bottleneck ✅
    H3: GPU-to-GPU communication requirements ✅
  H2: InfiniBand vs Ethernet: core technical differences ✅
    H3: Bandwidth and latency ✅
    H3: RDMA and CPU bypass ✅
    H3: Congestion control ✅
  H2: When InfiniBand is the right choice ✅
    H3: Large-scale LLM training ✅
    H3: HPC and distributed simulations ✅
    H3: Clusters above 128-256 GPUs ✅
  H2: When Ethernet (and RoCEv2) works ✅
    H3: Inference-heavy deployments ✅
    H3: Smaller clusters under 128 GPUs ✅
    H3: Hybrid or cloud-adjacent architectures ✅
  H2: Total cost of ownership: more than the cable ✅
    H3: Hardware and switch costs ✅
    H3: Operational complexity ✅
    H3: The management overhead calculation ✅
  H2: InfiniBand vs Ethernet: decision framework ✅
  H2: How OneSource Cloud approaches AI cluster networking ✅
  H2: FAQ ✅
  H2: Conclusion ✅
  H2: Meta elements ⚠️ (internal working section — must be removed before publish)
  H2: SEO checklist ⚠️ (internal working section — must be removed before publish)
  H2: Engagement checklist ⚠️ (internal working section — must be removed before publish)
```

### Heading Audit Findings

| Check | Result |
|---|---|
| Single H1 | ✅ Pass |
| Primary keyword in H1 | ✅ Pass |
| Primary keyword variant in 2+ H2s | ✅ Pass (2 H2s contain "InfiniBand vs Ethernet") |
| Logical H2 → H3 hierarchy | ✅ Pass |
| No skipped heading levels | ✅ Pass |
| H2s describe distinct sections | ✅ Pass |
| Internal working sections in heading tree | ⚠️ 3 H2s at bottom must be stripped before publishing |

**Score: 16/20**

**Issue:** Three internal working H2 sections (`Meta elements`, `SEO checklist`, `Engagement checklist`) are present at the end of the file. These must be removed from the published article. They should not appear in the live HTML. Removing them is required before any CMS import or web publish.

---

## 3. Link Audit

### Internal Links

| Anchor Text | Destination | Placement |
|---|---|---|
| high-performance AI networking architecture | https://onesourcecloud.net/high-performance-ai-networking | Section 2, CTA blockquote |
| Book an architecture review with OneSource Cloud | https://onesourcecloud.net/private-ai-infrastructure | Section 4, CTA blockquote |
| private AI infrastructure | https://onesourcecloud.net/private-ai-infrastructure | Section 7, body |
| AI infrastructure for healthcare | https://onesourcecloud.net/ai-for-healthcare | Section 7, body |
| Book an architecture review with OneSource Cloud | https://onesourcecloud.net/private-ai-infrastructure | Conclusion CTA |

**Internal link count:** 5 (3 unique destinations)
**Recommended for 3,100 words:** 6–8 internal links
**Status:** ⚠️ Slightly under-linked. At 3,100 words, one additional internal link (to a pillar page or related cluster article) would improve crawlability and topical authority signals.

### External Links

| Reference | Status |
|---|---|
| NVIDIA InfiniBand documentation | ⚠️ Referenced in meta block only — not hyperlinked in article body |
| MLCommons benchmark results | ⚠️ Referenced in meta block only — not hyperlinked in article body |
| IEEE RDMA standards | ⚠️ Referenced in meta block only — not hyperlinked in article body |

**Issue:** Three external authority sources are listed in the meta block but are not linked within the article body. External links to high-authority domains (nvidia.com, mlcommons.org, ieee.org) improve topical authority signals and user trust for technical content. At minimum, one external citation should be hyperlinked in the body — ideally in Section 2 (technical comparison) or the FAQ.

**Link Score: 9/15**

---

## 4. Meta Elements

### Meta Title

| | Value |
|---|---|
| **Current** | `InfiniBand vs Ethernet for AI Clusters: 2026 Guide \| OneSource Cloud` |
| **Character count** | ~68 characters |
| **Target range** | 50–60 characters |
| **Status** | ⚠️ Over limit by ~8 characters |

The current meta title exceeds the recommended 50–60 character range. Google typically truncates at ~60 characters in SERPs, which risks cutting off ` | OneSource Cloud`. The primary keyword is present and well-placed, but the brand suffix pushes it over. See `meta-options` file for trimmed alternatives.

### Meta Description

| | Value |
|---|---|
| **Current** | `Compare InfiniBand and Ethernet for AI cluster networking. Understand latency, bandwidth, RDMA, and TCO to choose the right fabric for your workloads.` |
| **Character count** | ~150 characters |
| **Target range** | 150–160 characters |
| **Status** | ✅ Pass (low end of range) |

The description is clear and includes the primary keyword, key topic signals (RDMA, TCO, latency, bandwidth), and a clear value proposition. Could add a benefit phrase to reach 155–158 characters.

### URL Slug

| | Value |
|---|---|
| **Slug** | `/blog/infiniband-vs-ethernet-ai-cluster-networking` |
| **Status** | ✅ Pass |

Clean, keyword-rich, lowercase, hyphenated. No stop words. No date or session tokens. Good.

**Meta Score: 12/15**

---

## 5. Readability Assessment

| Metric | Estimate | Notes |
|---|---|---|
| Flesch Reading Ease | ~42–50 | Technical content, appropriate for CTO/CIO audience |
| Flesch-Kincaid Grade Level | ~Grade 14–15 | College-graduate level — correct for enterprise B2B |
| Average sentence length | ~18–22 words | Acceptable, no run-on sentences detected |
| Average paragraph length | 2–4 sentences | ✅ Meets stated 4-sentence max rule |
| Use of tables | 2 tables | ✅ Aids comprehension |
| Use of lists | Multiple | ✅ Decision framework, operational complexity bullets |
| Use of callout blocks | 3 CTA blocks + 1 Key Takeaways | ✅ Breaks visual monotony |
| First CTA placement | Section 2 (after comparison table) | ✅ Within first 500 words of body content |
| Jargon density | High (RDMA, DCQCN, PFC, ECN, HCA, UFM) | ✅ All terms are defined inline |
| Active voice ratio | ~75% | ✅ Mostly active |

**Assessment:** Readability is appropriate for the target audience (infrastructure-focused CTO/CIO/VP Engineering). Jargon is consistently defined at first use. Sentence variety is good. No paragraph exceeds four sentences.

**Readability Score: 8/10**

---

## 6. Content Depth & Coverage

| Signal | Status |
|---|---|
| Word count (~3,100) | ✅ Exceeds recommended 2,000+ for competitive keyword |
| Topic fully covered | ✅ Technical specs, use cases, TCO, decision framework, FAQ |
| FAQ section | ✅ 6 questions |
| Comparison table | ✅ Present in Section 2 |
| Decision matrix | ✅ Present in Section 6 |
| Named entities / specifics | ✅ GPU models (H100, H200, A100), switch specs (HDR, NDR), latency figures |
| Original narrative examples | ✅ Financial services firm story, Dr. Anika Patel case |
| CTA presence | ✅ 3 contextual CTAs + 1 conclusion CTA |
| Key Takeaways block | ✅ Present above fold |
| Table of contents | ✅ Linked TOC present |
| Published date in title | ✅ "2026 guide" establishes freshness |

**Content Score: 19/20**

---

## 7. Image Optimization

| Image | Alt Text | Status |
|---|---|---|
| Pexels photo 4716292 | "Blue plastic wires with white tips connected to server..." | ⚠️ Descriptive but not keyword-optimized |
| Pexels photo 2881227 | "Detailed view of a network switch featuring multiple ethernet ports..." | ⚠️ Descriptive but no keyword signal |
| Pexels photo 2881232 | "Detailed view of blue ethernet cables connected to a network switch..." | ⚠️ Descriptive but no keyword signal |
| Pexels photo 2881224 | "Close-up image of ethernet cables plugged into a network switch..." | ⚠️ Descriptive but no keyword signal |

**Recommendation:** Alt text should include target keywords where naturally fitting. Example rewrite for the hero image: `"InfiniBand network cables and server connections for AI cluster infrastructure"`. This is a moderate signal but simple to fix.

---

## 8. Schema Markup Opportunities

| Schema Type | Status | Recommendation |
|---|---|---|
| FAQPage schema | ❌ Missing | The 6-question FAQ section is ideal for FAQ schema. This can generate rich FAQ result snippets in SERPs, significantly improving CTR for this article. |
| Article schema | ❌ Missing | Basic Article/TechArticle schema with author, datePublished, headline |
| BreadcrumbList | ❌ Missing | If site uses breadcrumbs, add structured breadcrumb schema |

**These are not present in the current file and must be implemented at the CMS/template level.**

---

## Priority Action Items

| Priority | Issue | Impact |
|---|---|---|
| 🔴 High | Remove 3 internal working sections (Meta elements, SEO checklist, Engagement checklist) before publishing | Prevents internal content from appearing in live HTML |
| 🔴 High | Shorten meta title to 50–60 characters | Prevents SERP truncation; brand name at risk of being cut |
| 🟡 Medium | Hyperlink at least one external authority source in article body | Improves topical authority signal and user credibility |
| 🟡 Medium | Optimize image alt text with keyword-relevant descriptions | Moderate SEO signal improvement |
| 🟡 Medium | Add one additional internal link to a cluster article | Improves crawlability and internal PageRank flow |
| 🟢 Low | Add FAQ schema markup at CMS level | Can generate rich SERP snippets and improve CTR |
| 🟢 Low | Extend meta description to 155–158 characters | Currently at low end of range; minor opportunity |
