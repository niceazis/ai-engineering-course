#!/usr/bin/env python3
"""Build or compare the upstream AI Engineering course manifest."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

UPSTREAM_REPO = "amitshekhariitbhu/ai-engineering-course"
UPSTREAM_BRANCH = "main"
README_URL = f"https://raw.githubusercontent.com/{UPSTREAM_REPO}/{UPSTREAM_BRANCH}/README.md"
COMMIT_URL = f"https://api.github.com/repos/{UPSTREAM_REPO}/commits/{UPSTREAM_BRANCH}"
MODULE_RE = re.compile(r"^## Module (\d+): (.+)$", re.MULTILINE)
LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")


def fetch_text(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "ai-engineering-course-sync"})
    with urllib.request.urlopen(req, timeout=30) as response:
        return response.read().decode("utf-8")


def normalize_url(url: str) -> str:
    return url.rstrip("/")


def classify(url: str) -> str:
    if "outcomeschool.com/blog/" in url:
        return "blog"
    if "youtube.com/watch" in url or "youtu.be/" in url:
        return "video"
    return "external"


def parse_modules(readme: str) -> list[dict]:
    modules = []
    for match in MODULE_RE.finditer(readme):
        number = int(match.group(1))
        title = match.group(2).strip()
        rest = readme[match.end():]
        next_h2 = re.search(r"^## (?!#)", rest, re.MULTILINE)
        section = rest[:next_h2.start()] if next_h2 else rest

        lessons = []
        seen = set()
        for link in LINK_RE.finditer(section):
            url = normalize_url(link.group(2))
            if url in seen:
                continue
            seen.add(url)
            lessons.append(
                {
                    "type": classify(url),
                    "title": link.group(1).strip(),
                    "url": url,
                }
            )

        modules.append({"number": number, "title": title, "lessons": lessons})

    return modules


def build_manifest() -> dict:
    readme = fetch_text(README_URL)
    commit = json.loads(fetch_text(COMMIT_URL))
    return {
        "schema_version": 1,
        "source_repository": UPSTREAM_REPO,
        "source_branch": UPSTREAM_BRANCH,
        "source_commit": commit["sha"],
        "source_commit_date": commit["commit"]["committer"]["date"],
        "modules": parse_modules(readme),
    }


def lesson_map(manifest: dict) -> dict:
    result = {}
    for module in manifest.get("modules", []):
        number = int(module["number"])
        for lesson in module.get("lessons", []):
            result[(number, lesson["type"], normalize_url(lesson["url"]))] = lesson
    return result


def module_titles(manifest: dict) -> dict:
    return {int(m["number"]): m["title"] for m in manifest.get("modules", [])}


def print_diff(old: dict, new: dict) -> None:
    old_lessons = lesson_map(old)
    new_lessons = lesson_map(new)
    old_keys = set(old_lessons)
    new_keys = set(new_lessons)

    for key in sorted(new_keys - old_keys):
        module, kind, url = key
        print(f"+ Module {module:02d} [{kind}] {new_lessons[key]['title']} :: {url}")

    for key in sorted(old_keys - new_keys):
        module, kind, url = key
        print(f"- Module {module:02d} [{kind}] {old_lessons[key]['title']} :: {url}")

    for key in sorted(old_keys & new_keys):
        before = old_lessons[key]["title"]
        after = new_lessons[key]["title"]
        if before != after:
            module, kind, url = key
            print(f"~ Module {module:02d} [{kind}] title: {before!r} -> {after!r} :: {url}")

    old_titles = module_titles(old)
    new_titles = module_titles(new)
    for number in sorted(set(old_titles) | set(new_titles)):
        if number not in old_titles:
            print(f"+ Module {number:02d}: {new_titles[number]}")
        elif number not in new_titles:
            print(f"- Module {number:02d}: {old_titles[number]}")
        elif old_titles[number] != new_titles[number]:
            print(f"~ Module {number:02d} title: {old_titles[number]!r} -> {new_titles[number]!r}")


def comparable(manifest: dict) -> dict:
    return {
        "schema_version": manifest.get("schema_version"),
        "source_repository": manifest.get("source_repository"),
        "source_branch": manifest.get("source_branch"),
        "source_commit": manifest.get("source_commit"),
        "modules": manifest.get("modules", []),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--write", metavar="PATH", help="write the live upstream manifest")
    group.add_argument("--check", metavar="PATH", help="compare live upstream with a committed manifest")
    args = parser.parse_args()

    live = build_manifest()

    if args.write:
        path = Path(args.write)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(live, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {path} at upstream {live['source_commit']}")
        return 0

    path = Path(args.check)
    committed = json.loads(path.read_text(encoding="utf-8"))
    if comparable(committed) == comparable(live):
        print(f"Upstream is unchanged: {live['source_commit']}")
        return 0

    print("Upstream course changed.")
    print(f"Processed: {committed.get('source_commit')}")
    print(f"Current:   {live.get('source_commit')}")
    print_diff(committed, live)
    return 2


if __name__ == "__main__":
    sys.exit(main())
