# SEO Optimization Report
**Article:** InfiniBand vs Ethernet for AI cluster networking: which should you choose?
**File:** `drafts/infiniband-vs-ethernet-ai-cluster-networking-2026-05-04.md`
**Report date:** 2026-05-04
**Auditor:** SEO Optimizer Agent

---

## Pass/Fail Checklist

### 1. Primary Keyword: "InfiniBand vs Ethernet for AI clusters"

| Check | Status | Notes |
|---|---|---|
| Present in H1 | PASS | H1: "InfiniBand vs Ethernet for AI cluster networking: which should you choose?" — near-exact match; "AI clusters" rendered as "AI cluster networking" which is acceptable and more descriptive |
| Present in first 100 words | PASS | Appears in the very first sentence of the article body |
| Present in H2s | PASS | H2: "InfiniBand vs Ethernet: direct comparison" — exact thematic match; also reflected in H2s "InfiniBand for AI clusters" and "Ethernet for AI clusters" |
| Keyword density | PASS | Estimated ~8-10 explicit mentions across ~2,900 words (~0.3-0.35%) — appropriate, not stuffed |

### 2. Secondary Keywords

| Keyword | Status | Notes |
|---|---|---|
| AI cluster networking | PASS | H1, first sentence, ToC, multiple H2s, conclusion — strong presence |
| InfiniBand vs RoCE | PASS | Appears in direct comparison table and throughout body copy |
| High-performance AI networking | PASS | Anchor text in internal link CTA (line 70): "high-performance AI networking architecture" |
| GPU cluster interconnect | FAIL | Not present as a phrase. "GPU-to-GPU communication" used but the keyword phrase is absent |
| RDMA networking for AI | PARTIAL | "RDMA" appears frequently; "RDMA networking for AI" as a combined phrase does not appear explicitly |

**Fix required:** Insert "GPU cluster interconnect" naturally in the "When InfiniBand is the right choice" or "Direct comparison" section. Example: "Choosing the right GPU cluster interconnect at this scale has compounding returns." Add "RDMA networking for AI" once in the Ethernet section where RoCE v2 is introduced.

### 3. Internal Links

| Link | URL | Status | Anchor Text | Placement |
|---|---|---|---|---|
| /private-ai-infrastructure | `https://onesourcecloud.net/private-ai-infrastructure` | PASS | "private AI infrastructure" (para 4 of intro) | PASS — first 2 paragraphs |
| /high-performance-ai-networking | `https://onesourcecloud.net/high-performance-ai-networking` | PASS | "high-performance AI networking architecture" | PASS — mid-article (end of "hidden bottleneck" section) |
| /private-ai-infrastructure | `https://onesourcecloud.net/private-ai-infrastructure` | PASS | "Schedule an architecture review" (x2: OneSource section + Conclusion CTA) | PASS — near CTA |
| /ai-for-healthcare | Required but MISSING | FAIL | No link present | — |

**Fix required:** The required `/ai-for-healthcare` industry link is entirely absent. The article does reference healthcare once ("AI infrastructure for healthcare must meet strict reliability and compliance requirements") in the "How OneSource Cloud designs AI cluster networking" section — this is the ideal placement. Add: `[AI infrastructure for healthcare](https://onesourcecloud.net/ai-for-healthcare)` as the anchor for that phrase. This also satisfies varied anchor text and mid-to-near-CTA placement.

**Note on anchor text variety:** `/private-ai-infrastructure` is used twice with different anchors ("private AI infrastructure" and "Schedule an architecture review") — this is good practice.

### 4. Meta Title and Meta Description

| Element | Value | Length | Status | Notes |
|---|---|---|---|---|
| Meta title | "InfiniBand vs Ethernet for AI Clusters 2026 \| OneSource Cloud" | 61 chars | FAIL | 1 character over the 60-char upper limit. Remove "2026" or shorten brand suffix |
| Meta description | "Compare InfiniBand and Ethernet for AI cluster networking. Latency, bandwidth, cost, and a decision framework for enterprise infrastructure teams." | 145 chars | FAIL | 5 characters under the 150-char lower limit. Needs expansion |

**Fix required:**
- Meta title: Shorten to 60 chars max. Suggested: `InfiniBand vs Ethernet for AI Clusters | OneSource Cloud` (57 chars) — drop "2026".
- Meta description: Expand to 150-160 chars. Suggested: `Compare InfiniBand and Ethernet for AI cluster networking. Latency, bandwidth, cost, and a clear decision framework for enterprise infrastructure and AI teams.` (159 chars).

### 5. Heading Hierarchy

| Check | Status | Notes |
|---|---|---|
| Single H1 | PASS | One H1 at the top of the article |
| H2s present and logical | PASS | 8 H2 sections covering all key angles |
| H3s used appropriately | PASS | H3s appear under H2s only (e.g., "HDR and NDR InfiniBand specifications" under the InfiniBand H2) — hierarchy is clean |
| No heading level skips | PASS | H1 → H2 → H3 progression is correct throughout |

### 6. Key Takeaways Block

| Check | Status | Notes |
|---|---|---|
| Present after intro | PASS | Blockquote Key Takeaways section appears immediately after the intro paragraphs |
| Contains 3+ points | PASS | 5 bullet points covering latency, Ethernet viability, TCO, hybrid architecture, and Ultra Ethernet |

### 7. FAQ Section

| Check | Status | Notes |
|---|---|---|
| FAQ section present | PASS | "Frequently asked questions" H2 present |
| Question count (4-6) | PASS | 6 questions — at the upper end of the target range |
| Questions cover key user intents | PASS | Covers performance, cost, RoCE v1 vs v2, UEC, and inference vs training use cases |
| Questions formatted as bold text | PASS | Each question is bolded within the FAQ section |

### 8. Word Count

| Check | Status | Notes |
|---|---|---|
| Word count | PASS | Front matter declares ~2,900 words. Manual section-by-section estimate aligns with this. Target for competitive AI infrastructure content is typically 2,500-3,500 words — this sits within range |

---

## Summary of Required Fixes

| Priority | Fix | Section |
|---|---|---|
| HIGH | Add `/ai-for-healthcare` internal link | "How OneSource Cloud designs AI cluster networking" — anchor: "AI infrastructure for healthcare" |
| HIGH | Meta description too short (145 chars, need 150-160) | Front matter |
| MEDIUM | Meta title 1 char too long (61 chars, need 50-60) | Front matter |
| MEDIUM | Secondary keyword "GPU cluster interconnect" absent | Add once in "When InfiniBand is the right choice" or comparison table caption |
| LOW | Secondary keyword "RDMA networking for AI" not present as a phrase | Add once in the RoCE v2 section |

---

## Recommended Front Matter Changes

```yaml
meta_title: "InfiniBand vs Ethernet for AI Clusters | OneSource Cloud"
meta_description: "Compare InfiniBand and Ethernet for AI cluster networking. Latency, bandwidth, cost, and a clear decision framework for enterprise infrastructure and AI teams."
```

---

## Overall Assessment

The article is well-structured and largely SEO-sound. The primary keyword is correctly placed in the H1, first sentence, key H2s, and is appropriately distributed. The heading hierarchy, Key Takeaways block, and FAQ section all meet requirements. The main issues are the missing `/ai-for-healthcare` internal link, two minor meta tag length corrections, and two secondary keywords that need a single natural insertion each. Addressing the five fixes above will bring the article to full compliance.
