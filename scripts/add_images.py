#!/usr/bin/env python3
"""Generate a single 16:9 hero image for a draft article using DALL-E 3.
Falls back to Pexels if OpenAI is unavailable."""

import os
import sys
import requests
from pathlib import Path

ROOT = Path(__file__).parent.parent
IMAGES_DIR = ROOT / "assets" / "images"


def load_env():
    env = {}
    env_file = ROOT / "data_sources" / "config" / ".env"
    if env_file.exists():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            if "=" in line and not line.strip().startswith("#"):
                k, _, v = line.partition("=")
                env[k.strip()] = v.strip()
    return env


def parse_frontmatter(content):
    meta = {}
    body = content
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            for line in content[3:end].strip().splitlines():
                if ":" in line:
                    k, _, v = line.partition(":")
                    meta[k.strip()] = v.strip().strip('"')
            body = content[end + 3:].strip()
    return meta, body


def generate_dalle(prompt, api_key, slug):
    """Generate image with DALL-E 3 and save locally. Returns local file path."""
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1792x1024",
        "quality": "standard",
        "response_format": "url",
    }
    try:
        r = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers=headers, json=payload, timeout=60
        )
        if r.status_code == 200:
            image_url = r.json()["data"][0]["url"]
            # Download and save locally
            img_data = requests.get(image_url, timeout=30).content
            local_path = IMAGES_DIR / f"{slug}.jpg"
            local_path.write_bytes(img_data)
            print(f"DALL-E 3 image saved: {local_path.name}")
            return str(local_path), image_url
        else:
            print(f"DALL-E 3 error {r.status_code}: {r.text[:200]}")
    except Exception as e:
        print(f"DALL-E 3 error: {e}")
    return None, None


def search_pexels(query, api_key):
    """Fallback: fetch one landscape image from Pexels."""
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": api_key}
    params = {"query": query, "per_page": 3, "orientation": "landscape"}
    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        if r.status_code == 200:
            photos = r.json().get("photos", [])
            if photos:
                p = photos[0]
                return p["src"]["landscape"], p["alt"] or query
    except Exception as e:
        print(f"Pexels error: {e}")
    return None, None


def add_images(file_path, openai_key=None, pexels_key=None):
    path = Path(file_path)
    content = path.read_text(encoding="utf-8")

    if "![" in content:
        print(f"Already has image: {path.name}")
        return False

    meta, body = parse_frontmatter(content)
    title = (
        meta.get("title")
        or meta.get("meta_title", "")
        or path.stem.replace("-", " ")
    )
    keyword = (
        meta.get("primary_keyword")
        or meta.get("Primary Keyword")
        or title
    )
    slug = meta.get("url_slug", path.stem).strip("/").replace("/blog/", "").replace("/", "-")

    image_url = None
    alt_text = keyword

    # Try DALL-E 3 first
    if openai_key:
        dalle_prompt = (
            f"A professional, high-quality photograph for a B2B technology blog article titled: \"{title}\". "
            f"Topic: {keyword}. "
            f"Style: clean, modern, corporate. No text, no logos. Photorealistic. Wide landscape shot."
        )
        local_path, image_url = generate_dalle(dalle_prompt, openai_key, slug)
        if local_path:
            # Use local file path in markdown — permanent, never expires
            image_url = "/" + Path(local_path).relative_to(ROOT).as_posix()

    # Fallback to Pexels
    if not image_url and pexels_key:
        print("Falling back to Pexels…")
        image_url, alt_text = search_pexels(keyword[:60], pexels_key)
        if not image_url:
            image_url, alt_text = search_pexels("cloud computing technology server", pexels_key)

    if not image_url:
        print(f"No image found for: {path.name}")
        return False

    # Insert hero image after first long paragraph
    lines = body.split("\n")
    new_lines = []
    inserted = False

    for line in lines:
        new_lines.append(line)
        if (
            not inserted
            and line.strip()
            and not line.startswith("#")
            and not line.startswith(">")
            and not line.startswith("-")
            and not line.startswith("*")
            and not line.startswith("|")
            and len(line.strip()) > 80
        ):
            new_lines.append(f"\n![{alt_text}]({image_url})\n")
            inserted = True

    new_body = "\n".join(new_lines)

    # Reconstruct with frontmatter
    if content.startswith("---"):
        end = content.find("---", 3)
        fm = content[:end + 3]
        new_content = fm + "\n\n" + new_body
    else:
        new_content = new_body

    path.write_text(new_content, encoding="utf-8")
    print(f"Added 1 hero image (16:9) to: {path.name}")
    return True


def main():
    env = load_env()
    openai_key = env.get("OPENAI_API_KEY") or os.environ.get("OPENAI_API_KEY", "")
    pexels_key = env.get("PEXELS_API_KEY") or os.environ.get("PEXELS_API_KEY", "")

    if not openai_key and not pexels_key:
        print("Error: No image API key configured (OPENAI_API_KEY or PEXELS_API_KEY)")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage: python scripts/add_images.py <draft_file>")
        sys.exit(1)

    add_images(sys.argv[1], openai_key=openai_key, pexels_key=pexels_key)


if __name__ == "__main__":
    main()
