#!/usr/bin/env python3
"""Generate dashboard.json from seomachine folder state.

Run this whenever you want to refresh the dashboard:
    python dashboard_data.py

Then open dashboard.html in your browser (via a local server).
"""

import json
import os
import re
from pathlib import Path
from datetime import datetime
from collections import defaultdict

ROOT = Path(__file__).parent
TODAY = datetime.now().strftime("%Y-%m-%d")

AUX_PREFIXES = (
    "seo-report-",
    "meta-options-",
    "keyword-analysis-",
    "link-suggestions-",
    "content-analysis-",
)

CLUSTER_BUCKETS = [
    ("Healthcare & Compliance",   ["healthcare", "hipaa", "hospital", "medical", "genomics", "life-sciences", "life", "sciences"]),
    ("GPU & Compute",             ["gpu", "compute", "processor", "cuda", "tensor"]),
    ("Networking",                ["networking", "infiniband", "ethernet", "network", "bandwidth"]),
    ("Storage",                   ["storage", "nvme", "filesystem", "object-storage"]),
    ("Cost & Economics",          ["cost", "tco", "total-cost", "ownership", "pricing", "budget"]),
    ("Orchestration",             ["kubernetes", "slurm", "scheduling", "orchestration", "k8s"]),
    ("Colocation & On-Premises",  ["colocation", "on-premises", "colo", "data-center", "datacenter"]),
    ("Vendor & Managed Services", ["vendor", "provider", "managed", "evaluation", "partner"]),
    ("Architecture & Infrastructure", ["infrastructure", "architecture", "deployment", "cluster", "private", "public", "cloud"]),
]

REPURPOSE_PLATFORMS = ["linkedin", "medium", "reddit", "quora", "twitter", "newsletter", "email"]


def parse_filename_date(name: str):
    m = re.search(r"^(.*?)-(\d{4}-\d{2}-\d{2})\.md$", name)
    if m:
        return m.group(1), m.group(2)
    return name.replace(".md", ""), None


def slugify_title(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s


def list_md(folder: str):
    p = ROOT / folder
    if not p.exists():
        return []
    return sorted([f.name for f in p.iterdir() if f.suffix == ".md"])


def parse_queue():
    f = ROOT / "topics" / "queue.md"
    if not f.exists():
        return {"pending": [], "in_progress": [], "done": []}
    text = f.read_text(encoding="utf-8", errors="ignore")
    sections = {"pending": [], "in_progress": [], "done": []}
    current = None
    for line in text.splitlines():
        s = line.strip()
        low = s.lower()
        if low.startswith("## pending"):
            current = "pending"
        elif low.startswith("## in progress"):
            current = "in_progress"
        elif low.startswith("## done"):
            current = "done"
        elif current and s.startswith("- ["):
            checked = s.startswith("- [x]")
            text_part = re.sub(r"^- \[[x ]\]\s*", "", s)
            date_match = re.search(r"\((\d{4}-\d{2}-\d{2})\)\s*$", text_part)
            date_val = date_match.group(1) if date_match else None
            title = re.sub(r"\s*\(\d{4}-\d{2}-\d{2}\)\s*$", "", text_part)
            sections[current].append({"title": title, "checked": checked, "date": date_val})
    return sections


def first_heading(filepath: Path):
    try:
        with filepath.open(encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if line.startswith("# "):
                    return line[2:].strip()
        return None
    except Exception:
        return None


def word_count(filepath: Path):
    try:
        return len(filepath.read_text(encoding="utf-8", errors="ignore").split())
    except Exception:
        return 0


def collect_articles():
    articles, aux = [], []
    for name in list_md("drafts"):
        slug, date = parse_filename_date(name)
        path = ROOT / "drafts" / name
        item = {
            "filename": name,
            "slug": slug,
            "date": date,
            "title": first_heading(path) or slug.replace("-", " ").title(),
            "words": word_count(path),
            "is_aux": name.startswith(AUX_PREFIXES),
            "linked": [],
        }
        (aux if item["is_aux"] else articles).append(item)
    articles.sort(key=lambda x: x["date"] or "", reverse=True)
    aux.sort(key=lambda x: x["date"] or "", reverse=True)
    return articles, aux


def link_aux_to_articles(articles, aux_list):
    """Match each aux file to its closest parent article by date + slug overlap."""
    linked_map = {a["slug"]: [] for a in articles}
    aux_prefix_to_type = {
        "seo-report": "seo-report",
        "keyword-analysis": "keyword-analysis",
        "meta-options": "meta-options",
        "link-suggestions": "link-suggestions",
        "content-analysis": "content-analysis",
    }

    for aux_item in aux_list:
        aux_type = "other"
        core_slug = aux_item["slug"]
        for prefix, atype in aux_prefix_to_type.items():
            if core_slug.startswith(prefix + "-"):
                aux_type = atype
                core_slug = core_slug[len(prefix) + 1:]
                break

        stop_words = {"a", "the", "for", "of", "in", "and", "to", "is", "vs", "how"}
        core_words = set(core_slug.split("-")) - stop_words

        best, best_score = None, -1
        for a in articles:
            score = 0
            if a["date"] and aux_item["date"] and a["date"] == aux_item["date"]:
                score += 5
            article_words = set(a["slug"].split("-")) - stop_words
            score += len(core_words & article_words)
            if score > best_score:
                best_score, best = score, a

        if best and best_score > 0:
            linked_map[best["slug"]].append({
                "type": aux_type,
                "filename": aux_item["filename"],
                "title": aux_item["title"],
                "words": aux_item["words"],
            })

    for a in articles:
        a["linked"] = linked_map.get(a["slug"], [])
    return articles


def collect_briefs():
    briefs = []
    for name in list_md("research"):
        path = ROOT / "research" / name
        slug, date = parse_filename_date(name)
        briefs.append({
            "filename": name,
            "slug": slug.replace("brief-", ""),
            "date": date,
            "title": first_heading(path) or name,
            "words": word_count(path),
        })
    briefs.sort(key=lambda x: x["date"] or "", reverse=True)
    return briefs


def collect_repurposed():
    """Scan repurposed/ for platform-specific versions of articles."""
    items = []
    folder = ROOT / "repurposed"
    if not folder.exists():
        return items
    for f in sorted(folder.iterdir()):
        if f.suffix != ".md":
            continue
        slug, date = parse_filename_date(f.name)
        platform = "other"
        fname_lower = f.name.lower()
        for p in REPURPOSE_PLATFORMS:
            if p in fname_lower:
                platform = p
                break
        items.append({
            "filename": f.name,
            "slug": slug,
            "date": date,
            "platform": platform,
            "title": first_heading(f) or slug.replace("-", " ").title(),
        })
    return items


def attach_repurposed_to_articles(articles, repurposed):
    """Add repurposed platform list to each article."""
    for a in articles:
        platforms = []
        for r in repurposed:
            # Match if article slug appears in repurposed slug
            if a["slug"][:20] in r["slug"] or r["slug"][:20] in a["slug"]:
                platforms.append(r["platform"])
        a["repurposed_platforms"] = platforms
    return articles


def check_data_sources():
    env_file = ROOT / "data_sources" / "config" / ".env"
    creds = ROOT / "credentials"
    sources = {"dataforseo": False, "ga4": False, "gsc": False, "webflow": False}
    if env_file.exists():
        text = env_file.read_text(encoding="utf-8", errors="ignore")
        if re.search(r"DATAFORSEO_LOGIN\s*=\s*\S+", text) and "your_email" not in text:
            sources["dataforseo"] = True
        if re.search(r"GA4_PROPERTY_ID\s*=\s*\d+", text):
            sources["ga4"] = True
        if "GSC_SITE_URL" in text and "yoursite.com" not in text:
            oauth_token = ROOT / "credentials" / "ga4-token.json"
            gsc_creds = ROOT / "credentials" / "gsc-credentials.json"
            if oauth_token.exists() or gsc_creds.exists():
                sources["gsc"] = True
        if re.search(r"WEBFLOW_API_TOKEN\s*=\s*\S+", text):
            sources["webflow"] = True
    if creds.exists() and any(creds.iterdir()):
        sources["ga4"] = True
    if os.environ.get("WEBFLOW_API_TOKEN"):
        sources["webflow"] = True
    # Webflow is connected via Claude MCP — manual publishing works
    sources["webflow"] = True
    return sources


def collect_published():
    items = []
    for name in list_md("published"):
        path = ROOT / "published" / name
        slug, date = parse_filename_date(name)
        items.append({
            "filename": name,
            "slug": slug,
            "date": date,
            "title": first_heading(path) or slug.replace("-", " ").title(),
        })
    items.sort(key=lambda x: x["date"] or "", reverse=True)
    return items


def build_pipeline_view(queue, articles, published):
    published_slugs = {p["slug"] for p in published}
    pending_count = sum(1 for q in queue["pending"] if not q["checked"])
    drafted_count = len(articles)
    published_count = len(published)
    unpublished = [
        a for a in articles
        if not any(a["slug"].startswith(p) or p.startswith(a["slug"]) for p in published_slugs)
    ]
    return {
        "pending": pending_count,
        "drafted": drafted_count,
        "published": published_count,
        "unpublished_count": len(unpublished),
        "unpublished": unpublished[:5],
    }


def build_calendar_data(articles, queue, published):
    """Organize content by month for calendar view."""
    months = defaultdict(lambda: {"drafted": [], "published": [], "planned": []})

    for a in articles:
        if a["date"]:
            months[a["date"][:7]]["drafted"].append({
                "title": a["title"], "date": a["date"],
                "words": a["words"], "slug": a["slug"],
            })

    for p in published:
        if p["date"]:
            months[p["date"][:7]]["published"].append({
                "title": p["title"], "date": p["date"], "slug": p["slug"],
            })

    for q in queue["pending"]:
        if q["date"] and q["checked"]:
            months[q["date"][:7]]["planned"].append({"title": q["title"], "date": q["date"]})

    unscheduled = [q for q in queue["pending"] if not q["date"] and not q["checked"]]

    return {
        "months": {k: dict(v) for k, v in sorted(months.items(), reverse=True)},
        "unscheduled": unscheduled,
    }


def build_clusters(articles):
    """Group articles into topic clusters by keyword matching."""
    clustered = defaultdict(list)
    assigned = set()

    for bucket_name, keywords in CLUSTER_BUCKETS:
        for a in articles:
            if a["slug"] in assigned:
                continue
            slug_words = set(a["slug"].split("-"))
            if any(kw.replace("-", " ") in a["title"].lower() or
                   any(part in slug_words for part in kw.split("-"))
                   for kw in keywords):
                clustered[bucket_name].append({
                    "title": a["title"],
                    "slug": a["slug"],
                    "date": a["date"],
                    "words": a["words"],
                })
                assigned.add(a["slug"])

    unclustered = [a for a in articles if a["slug"] not in assigned]
    if unclustered:
        clustered["Other"] = [{"title": a["title"], "slug": a["slug"],
                               "date": a["date"], "words": a["words"]} for a in unclustered]

    return [{"name": k, "articles": v} for k, v in clustered.items() if v]


def collect_performance_report():
    """Find and parse the latest performance review report."""
    research_dir = ROOT / "research"
    if not research_dir.exists():
        return None
    reports = sorted(
        [f for f in research_dir.iterdir() if f.name.startswith("performance-review-") and f.suffix == ".md"],
        key=lambda f: f.name,
        reverse=True,
    )
    if not reports:
        return None
    latest = reports[0]
    content = latest.read_text(encoding="utf-8", errors="ignore")

    # Extract key metrics from the report — flexible patterns to handle format variations
    metrics = {}

    def find_num(patterns, text):
        """Try multiple regex patterns, return first int match (strips ~, commas)."""
        for pat in patterns:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                raw = m.group(1).replace(",", "").replace("~", "").strip()
                try:
                    return int(float(raw))
                except ValueError:
                    pass
        return None

    def find_pct(patterns, text):
        """Try multiple regex patterns, return first float percentage match."""
        for pat in patterns:
            m = re.search(pat, text, re.IGNORECASE)
            if m:
                try:
                    return float(m.group(1))
                except ValueError:
                    pass
        return None

    total = find_num([
        r"Total Sessions.*?\|\s*~?([\d,]+)",
        r"Total Site Sessions.*?\|\s*~?([\d,]+)",
        r"Total.*?Sessions.*?\|\s*~?([\d,]+)",
    ], content)
    if total:
        metrics["total_sessions"] = total

    organic = find_num([
        r"Organic Search Sessions.*?\|\s*~?([\d,]+)",
        r"Organic Sessions.*?\|\s*~?([\d,]+)",
    ], content)
    if organic and total:
        metrics["organic_sessions"] = organic
        metrics["organic_pct"] = round(organic / total * 100, 1)

    # Organic % may also be written explicitly
    pct = find_pct([
        r"Organic Search Sessions.*?\(([0-9.]+)%\)",
        r"organic.*?([0-9.]+)%\s+of total",
        r"([0-9.]+)%\s+of total.*?traffic",
    ], content)
    if pct and "organic_pct" not in metrics:
        metrics["organic_pct"] = pct

    keywords = find_num([
        r"Non-brand Keywords Ranking\s*\|\s*~?([\d,]+)",
        r"Total Organic Keywords Ranking\s*\|\s*~?([\d,]+)",
        r"Organic Keywords.*?\|\s*~?([\d,]+)",
        r"Non-?brand.*?[Kk]eywords.*?\|\s*~?([\d,]+)",
    ], content)
    if keywords is not None:
        metrics["total_keywords"] = keywords

    clicks = find_num([
        r"Non-brand Clicks\s*\|\s*~?([\d,]+)",
        r"Non-?brand.*?[Cc]licks.*?\|\s*~?([\d,]+)",
        r"Organic Clicks.*?\|\s*~?([\d,]+)",
    ], content)
    if clicks is not None:
        metrics["non_brand_clicks"] = clicks

    # Count action items
    action_items = len(re.findall(r"^- \[ \]", content, re.MULTILINE))

    _, date_str = parse_filename_date(latest.name)
    return {
        "filename": latest.name,
        "date": date_str,
        "metrics": metrics,
        "action_items": action_items,
        "content": content,
    }


def main():
    articles, aux = collect_articles()
    articles = link_aux_to_articles(articles, aux)

    briefs = collect_briefs()
    queue = parse_queue()
    published = collect_published()
    repurposed = collect_repurposed()
    articles = attach_repurposed_to_articles(articles, repurposed)
    sources = check_data_sources()
    pipeline = build_pipeline_view(queue, articles, published)
    calendar = build_calendar_data(articles, queue, published)
    clusters = build_clusters(articles)
    performance = collect_performance_report()

    data = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "today": TODAY,
        "totals": {
            "queue_pending": pipeline["pending"],
            "queue_done": sum(1 for q in queue["pending"] if q["checked"]) + len(queue["done"]),
            "drafts": len(articles),
            "drafts_aux": len(aux),
            "research_briefs": len(briefs),
            "published": pipeline["published"],
            "unpublished": pipeline["unpublished_count"],
        },
        "pipeline": pipeline,
        "queue": queue,
        "articles": articles,
        "aux": aux,
        "briefs": briefs,
        "published": published,
        "repurposed": repurposed,
        "calendar": calendar,
        "clusters": clusters,
        "data_sources": sources,
        "performance": performance,
    }

    out = ROOT / "dashboard.json"
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[OK] Wrote {out}")
    print(f"  - {data['totals']['drafts']} drafts, "
          f"{data['totals']['published']} published, "
          f"{data['totals']['queue_pending']} pending in queue, "
          f"{len(clusters)} topic clusters")


if __name__ == "__main__":
    main()
