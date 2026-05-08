#!/usr/bin/env python3
"""Publish the latest draft article to Webflow CMS as a draft item."""

import os
import re
import sys
import glob
import requests
import markdown as md_lib
from pathlib import Path

WEBFLOW_API_TOKEN = os.environ.get("WEBFLOW_API_TOKEN", "")
COLLECTION_ID = "6983857d3bc6d04385b552d9"
CATEGORY_PRIVATE_AI = "59ba2e06808b61979eeaedc3ff9f1a69"

EXCLUDE_PREFIXES = [
    "seo-report-",
    "meta-options-",
    "keyword-analysis-",
    "link-suggestions-",
    "content-analysis-",
]

STOP_MARKERS = [
    "## Meta elements",
    "## SEO checklist",
    "## AI search optimization",
    "## Engagement checklist",
]


def find_latest_draft():
    files = []
    for f in glob.glob("drafts/*.md"):
        name = Path(f).name
        if name == ".gitkeep":
            continue
        if any(name.startswith(p) for p in EXCLUDE_PREFIXES):
            continue
        files.append(f)

    if not files:
        print("No draft files found.")
        sys.exit(0)

    return max(files, key=os.path.getmtime)


def parse_frontmatter(content):
    meta = {}
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            for line in content[3:end].strip().splitlines():
                if ":" in line:
                    key, _, val = line.partition(":")
                    # Store both original and lowercase keys for flexible lookup
                    k = key.strip()
                    v = val.strip().strip('"')
                    meta[k] = v
                    meta[k.lower()] = v
                    meta[k.lower().replace(" ", "_")] = v
            content = content[end + 3:].strip()
    return meta, content


def extract_first_image(body):
    """Extract first image URL and alt text from markdown body."""
    match = re.search(r'!\[([^\]]*)\]\((https?://[^\)]+)\)', body)
    if match:
        return {"url": match.group(2), "alt": match.group(1)}
    return None


def md_to_html(body):
    for marker in STOP_MARKERS:
        idx = body.find(marker)
        if idx != -1:
            body = body[:idx]

    # Remove the table of contents block
    body = re.sub(r"\n\*\*In this guide:\*\*\n(- \[.*?\]\(.*?\)\n)+", "\n", body)

    return md_lib.markdown(
        body.strip(),
        extensions=["tables", "fenced_code", "nl2br"],
    )


def estimate_read_time(body):
    words = len(body.split())
    minutes = max(1, round(words / 200))
    return f"{minutes} min read"


def publish_to_webflow(title, slug, description, author, html_content, read_time, thumbnail=None):
    if not WEBFLOW_API_TOKEN:
        print("Error: WEBFLOW_API_TOKEN is not set.")
        sys.exit(1)

    headers = {
        "Authorization": f"Bearer {WEBFLOW_API_TOKEN}",
        "Content-Type": "application/json",
        "accept-version": "2.0.0",
    }

    # Clean slug: remove /blog/ prefix if present
    clean_slug = slug.lstrip("/").removeprefix("blog/")

    field_data = {
        "name": title,
        "slug": clean_slug,
        "description": description,
        "author": author or "OneSource Cloud",
        "read-time": read_time,
        "category": CATEGORY_PRIVATE_AI,
        "featured": False,
        "content": html_content,
    }

    # Set thumbnail and main image if available
    if thumbnail:
        field_data["image"] = thumbnail
        field_data["main-image"] = thumbnail
        print(f"  Thumbnail: {thumbnail['url'][:60]}…")

    payload = {
        "isArchived": False,
        "isDraft": True,
        "fieldData": field_data,
    }

    url = f"https://api.webflow.com/v2/collections/{COLLECTION_ID}/items"
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code in (200, 201, 202):
        data = response.json()
        print(f"Published to Webflow as draft.")
        print(f"  Item ID : {data.get('id', 'unknown')}")
        print(f"  Slug    : {clean_slug}")
    else:
        print(f"Webflow API error {response.status_code}: {response.text}")
        sys.exit(1)


def main():
    # Accept specific file via CLI arg or DRAFT_FILE env var
    if len(sys.argv) > 1:
        draft_file = sys.argv[1]
    elif os.environ.get("DRAFT_FILE"):
        draft_file = os.environ["DRAFT_FILE"]
    else:
        draft_file = find_latest_draft()
    print(f"Publishing: {draft_file}")

    with open(draft_file, encoding="utf-8") as f:
        content = f.read()

    meta, body = parse_frontmatter(content)

    raw_title = (meta.get("title") or meta.get("meta_title") or meta.get("Meta Title", ""))
    title = raw_title.replace(" | OneSource Cloud", "").strip() or "Untitled"
    slug = (meta.get("url_slug") or meta.get("URL Slug") or meta.get("url slug")
            or Path(draft_file).stem)
    description = meta.get("meta_description") or meta.get("Meta Description", "")
    author = meta.get("author") or meta.get("Author", "OneSource Cloud")
    read_time = estimate_read_time(body)
    thumbnail = extract_first_image(body)

    html = md_to_html(body)
    publish_to_webflow(title, slug, description, author, html, read_time, thumbnail)


if __name__ == "__main__":
    main()
