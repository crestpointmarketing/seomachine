#!/usr/bin/env python3
"""Local dashboard server with API support.

Serves static files on port 8080 and handles script triggers.

Usage:
    python server.py
"""

import http.server
import json
import os
import shutil
import subprocess
import threading
from pathlib import Path

PORT = 8080
ROOT = Path(__file__).parent
CLAUDE = shutil.which("claude") or r"C:\Users\Vivian\.local\bin\claude.exe"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def log_message(self, format, *args):
        pass  # Suppress request logs

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        return json.loads(self.rfile.read(length)) if length else {}

    def do_POST(self):
        if self.path == "/api/run-performance-review":
            self._run_task(
                ["python", "dashboard_data.py"],
                after_cmd=[CLAUDE, "-p", "--dangerously-skip-permissions",
                           "Run /performance-review and save the report. Then run: python dashboard_data.py"],
            )
        elif self.path == "/api/refresh-data":
            self._run_script(["python", "dashboard_data.py"])

        elif self.path == "/api/approve":
            body = self._read_body()
            filename = body.get("filename", "")
            self._approve(filename)

        elif self.path == "/api/update":
            body = self._read_body()
            filename = body.get("filename", "")
            feedback = body.get("feedback", "")
            self._update(filename, feedback)

        elif self.path == "/api/deny":
            body = self._read_body()
            filename = body.get("filename", "")
            self._deny(filename)

        elif self.path == "/api/optimize":
            body = self._read_body()
            self._optimize(body.get("filename", ""))

        elif self.path == "/api/add-topic":
            body = self._read_body()
            self._add_topic(body.get("topic", ""))

        elif self.path == "/api/generate-article":
            body = self._read_body()
            self._generate_article(body.get("topic", ""))

        elif self.path == "/api/research-topic":
            body = self._read_body()
            self._research_topic(body.get("topic", ""))

        elif self.path == "/api/suggest-topics":
            self._suggest_topics()

        else:
            self.send_error(404)

    def _approve(self, filename):
        if not filename:
            return self._json({"ok": False, "output": "No filename provided"})
        draft_path = ROOT / "drafts" / filename
        if not draft_path.exists():
            return self._json({"ok": False, "output": f"File not found: {filename}"})
        # Load WEBFLOW_API_TOKEN from .env
        env = os.environ.copy()
        env_file = ROOT / "data_sources" / "config" / ".env"
        if env_file.exists():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                if "=" in line and not line.strip().startswith("#"):
                    k, _, v = line.partition("=")
                    env.setdefault(k.strip(), v.strip())
        # Optimistically copy to published/ immediately for fast UI refresh
        published_dir = ROOT / "published"
        published_dir.mkdir(exist_ok=True)
        shutil.copy2(str(draft_path), str(published_dir / filename))
        subprocess.run(["python", "dashboard_data.py"], cwd=str(ROOT), capture_output=True)
        def bg():
            subprocess.run(
                ["python", "scripts/publish_to_webflow.py", str(draft_path)],
                cwd=str(ROOT), env=env
            )
        threading.Thread(target=bg, daemon=True).start()
        self._json({"ok": True, "output": f"Publishing {filename}…"})

    def _update(self, filename, feedback):
        if not filename or not feedback:
            return self._json({"ok": False, "output": "Missing filename or feedback"})
        draft_path = ROOT / "drafts" / filename
        if not draft_path.exists():
            return self._json({"ok": False, "output": f"File not found: {filename}"})
        prompt = (
            f"Update the article at drafts/{filename} based on this feedback:\n\n"
            f"{feedback}\n\n"
            f"Make the changes directly to the file. Preserve the article structure and SEO elements."
        )
        def bg():
            subprocess.run(
                [CLAUDE, "-p", "--dangerously-skip-permissions", prompt],
                cwd=str(ROOT)
            )
            subprocess.run(["python", "dashboard_data.py"], cwd=str(ROOT))
        threading.Thread(target=bg, daemon=True).start()
        self._json({"ok": True, "output": f"Updating {filename} with your feedback…"})

    def _optimize(self, filename):
        if not filename:
            return self._json({"ok": False, "output": "No filename provided"})
        draft_path = ROOT / "drafts" / filename
        if not draft_path.exists():
            return self._json({"ok": False, "output": f"File not found: {filename}"})
        slug = Path(filename).stem
        date_str = slug[-10:] if len(slug) >= 10 else "2026-05-04"
        prompt = (
            f"Read the article at drafts/{filename}. Then create these 3 files in drafts/:\n\n"
            f"1. drafts/seo-report-{slug}.md — SEO audit: keyword density, heading structure, internal/external links, meta elements, readability, SEO score 0-100\n"
            f"2. drafts/keyword-analysis-{slug}.md — Primary keyword, LSI keywords, density analysis, placement map, recommendations\n"
            f"3. drafts/meta-options-{slug}.md — 5 meta title options (50-60 chars each), 5 meta description options (150-160 chars each), recommended URL slug\n\n"
            f"Write each file with full markdown content. Do not skip any file."
        )
        def bg():
            subprocess.run(["python", "scripts/add_images.py", str(draft_path)], cwd=str(ROOT))
            subprocess.run([CLAUDE, "-p", "--dangerously-skip-permissions", prompt], cwd=str(ROOT))
            subprocess.run(["python", "dashboard_data.py"], cwd=str(ROOT))
        threading.Thread(target=bg, daemon=True).start()
        self._json({"ok": True, "output": f"Optimizing {filename}…"})

    def _add_topic(self, topic):
        if not topic:
            return self._json({"ok": False, "output": "No topic provided"})
        queue_file = ROOT / "topics" / "queue.md"
        queue_file.parent.mkdir(exist_ok=True)
        text = queue_file.read_text(encoding="utf-8") if queue_file.exists() else "## Pending\n\n## In Progress\n\n## Done\n"
        # Insert under ## Pending
        if "## Pending" in text:
            text = text.replace("## Pending\n", f"## Pending\n- [ ] {topic}\n", 1)
        else:
            text = f"## Pending\n- [ ] {topic}\n\n" + text
        queue_file.write_text(text, encoding="utf-8")
        subprocess.run(["python", "dashboard_data.py"], cwd=str(ROOT))
        self._json({"ok": True, "output": f"Added: {topic}"})

    def _generate_article(self, topic):
        if not topic:
            return self._json({"ok": False, "output": "No topic provided"})
        write_prompt = (
            f"You are running an automated content generation task for OneSource Cloud.\n\n"
            f"Topic to write about: {topic}\n\n"
            f"Steps:\n"
            f"1. Run /research for this topic\n"
            f"2. Run /write for this topic — saves draft to drafts/\n"
            f"3. Do NOT publish to Webflow\n\n"
            f"Follow all brand guidelines in context/ files.\n\n"
            f"When done, print the exact filename you saved to drafts/ on a line starting with 'SAVED: '"
        )
        def bg():
            import glob, re
            from datetime import datetime
            # Snapshot drafts before
            before = set(glob.glob(str(ROOT / "drafts" / "*.md")))
            result = subprocess.run(
                [CLAUDE, "-p", "--dangerously-skip-permissions", write_prompt],
                cwd=str(ROOT), capture_output=True, text=True
            )
            # Find newly created article file
            after = set(glob.glob(str(ROOT / "drafts" / "*.md")))
            new_files = [f for f in (after - before)
                         if not any(Path(f).name.startswith(p) for p in
                                    ["seo-report-", "keyword-analysis-", "meta-options-"])]
            if new_files:
                draft_path = new_files[0]
                slug = Path(draft_path).stem
                # Add Pexels images
                subprocess.run(
                    ["python", "scripts/add_images.py", draft_path],
                    cwd=str(ROOT)
                )
                # Generate SEO files
                seo_prompt = (
                    f"Read the article at {draft_path}. Create these 3 files in drafts/:\n\n"
                    f"1. drafts/seo-report-{slug}.md — SEO audit: keyword density, heading structure, links, meta elements, readability, score 0-100\n"
                    f"2. drafts/keyword-analysis-{slug}.md — Primary keyword, LSI keywords, density analysis, placement map\n"
                    f"3. drafts/meta-options-{slug}.md — 5 meta title options (50-60 chars), 5 meta description options (150-160 chars), recommended URL slug\n\n"
                    f"Write full markdown content for each file."
                )
                subprocess.run(
                    [CLAUDE, "-p", "--dangerously-skip-permissions", seo_prompt],
                    cwd=str(ROOT)
                )
            # Mark topic as done in queue
            queue_file = ROOT / "topics" / "queue.md"
            if queue_file.exists():
                today = datetime.now().strftime("%Y-%m-%d")
                text = queue_file.read_text(encoding="utf-8")
                text = text.replace(f"- [ ] {topic}\n", f"- [x] {topic} ({today})\n", 1)
                queue_file.write_text(text, encoding="utf-8")
            subprocess.run(["python", "dashboard_data.py"], cwd=str(ROOT))
        threading.Thread(target=bg, daemon=True).start()
        self._json({"ok": True, "output": f"Generating article for: {topic}"})

    def _suggest_topics(self):
        import json as _json
        import glob as _glob

        # Gather context: existing articles
        existing = []
        for f in _glob.glob(str(ROOT / "drafts" / "*.md")):
            name = Path(f).name
            if not any(name.startswith(p) for p in ["seo-report-", "keyword-analysis-", "meta-options-", "keyword-"]):
                existing.append(name.replace(".md", ""))

        # Queue topics already pending
        queue_file = ROOT / "topics" / "queue.md"
        queue_text = queue_file.read_text(encoding="utf-8") if queue_file.exists() else ""

        # Latest performance report summary (first 3000 chars)
        perf_summary = ""
        research_dir = ROOT / "research"
        if research_dir.exists():
            reports = sorted(
                [f for f in research_dir.iterdir() if f.name.startswith("performance-review-")],
                key=lambda f: f.name, reverse=True
            )
            if reports:
                perf_summary = reports[0].read_text(encoding="utf-8", errors="ignore")[:3000]

        prompt = f"""You are an SEO content strategist for OneSource Cloud, a managed private AI infrastructure company.

Based on the context below, suggest exactly 10 blog article topics that would:
1. Target keywords with good search volume and moderate competition
2. Fill gaps not covered by existing articles
3. Support the company's positioning in private/managed AI infrastructure

EXISTING ARTICLES:
{chr(10).join(existing)}

QUEUE (already planned):
{queue_text[:1000]}

PERFORMANCE DATA SUMMARY:
{perf_summary}

Output ONLY a valid JSON array of 10 topic strings. No explanation, no markdown, no extra text.
Example format: ["Topic one", "Topic two", "Topic three"]"""

        try:
            result = subprocess.run(
                [CLAUDE, "-p", "--dangerously-skip-permissions", prompt],
                cwd=str(ROOT), capture_output=True, text=True, timeout=120
            )
            output = result.stdout.strip()
            # Extract JSON array from output
            import re as _re
            match = _re.search(r'\[[\s\S]*?\]', output)
            if match:
                topics = _json.loads(match.group(0))
                self._json({"ok": True, "topics": topics})
            else:
                self._json({"ok": False, "output": "Could not parse suggestions", "raw": output[:500]})
        except subprocess.TimeoutExpired:
            self._json({"ok": False, "output": "Timed out after 2 minutes"})
        except Exception as e:
            self._json({"ok": False, "output": str(e)})

    def _research_topic(self, topic):
        if not topic:
            return self._json({"ok": False, "output": "No topic provided"})
        prompt = f"Run /research {topic} and save the research brief to research/. Follow brand guidelines in context/ files."
        def bg():
            subprocess.run(
                [CLAUDE, "-p", "--dangerously-skip-permissions", prompt],
                cwd=str(ROOT)
            )
            subprocess.run(["python", "dashboard_data.py"], cwd=str(ROOT))
        threading.Thread(target=bg, daemon=True).start()
        self._json({"ok": True, "output": f"Researching: {topic}"})

    def _deny(self, filename):
        if not filename:
            return self._json({"ok": False, "output": "No filename provided"})
        draft_path = ROOT / "drafts" / filename
        if not draft_path.exists():
            return self._json({"ok": False, "output": f"File not found: {filename}"})
        trash_dir = ROOT / "trash"
        trash_dir.mkdir(exist_ok=True)
        shutil.move(str(draft_path), str(trash_dir / filename))
        # Also move linked aux files
        for aux in (ROOT / "drafts").glob("*.md"):
            stem = filename.replace(".md", "")
            if aux.name != filename and stem in aux.name:
                shutil.move(str(aux), str(trash_dir / aux.name))
        subprocess.run(["python", "dashboard_data.py"], cwd=str(ROOT))
        self._json({"ok": True, "output": f"Moved {filename} to trash"})

    def _run_script(self, cmd):
        try:
            result = subprocess.run(
                cmd, cwd=str(ROOT), capture_output=True, text=True, timeout=60
            )
            ok = result.returncode == 0
            self._json({"ok": ok, "output": result.stdout or result.stderr})
        except Exception as e:
            self._json({"ok": False, "output": str(e)})

    def _run_task(self, refresh_cmd, after_cmd=None):
        """Run refresh first (fast), return immediately, then run full analysis in background."""
        try:
            subprocess.run(refresh_cmd, cwd=str(ROOT), capture_output=True, timeout=30)
            self._json({"ok": True, "output": "Started — this takes 1–2 minutes. Refresh the page when done."})
            if after_cmd:
                def bg():
                    subprocess.run(after_cmd, cwd=str(ROOT))
                    subprocess.run(refresh_cmd, cwd=str(ROOT))
                threading.Thread(target=bg, daemon=True).start()
        except Exception as e:
            self._json({"ok": False, "output": str(e)})

    def _json(self, data):
        body = json.dumps(data).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.end_headers()


if __name__ == "__main__":
    os.chdir(ROOT)
    server = http.server.HTTPServer(("", PORT), Handler)
    print(f"[OK] Dashboard running at http://localhost:{PORT}")
    print(f"     Press Ctrl+C to stop")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
