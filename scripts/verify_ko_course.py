#!/usr/bin/env python3
"""Validate the maintained Korean edition against the committed course manifest."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/ko/course-manifest.json"
STATE = ROOT / ".sync/upstream-state.json"
README_KO = ROOT / "README.ko.md"
ZERO_WIDTH_RE = re.compile(r"[\u200B-\u200D\uFEFF]")
HEADING_RE = re.compile(r"^(#{1,6})\s+", re.MULTILINE)
LINK_RE = re.compile(r"!?(?:\[[^\]]*\])\(([^)]+)\)")
VIDEO_LINK_RE = re.compile(r"\((videos/module-\d{2}/[^)#]+\.md)(?:#[^)]+)?\)")
VIDEO_NOTE_EXEMPT_MODULES = {0}


def normalize_url(url: str) -> str:
    return url.rstrip("/")


def blog_slug(url: str) -> str:
    return Path(urlparse(url).path.rstrip("/")).name


def markdown_issues(path: Path, text: str) -> list[str]:
    issues = []
    if ZERO_WIDTH_RE.search(text):
        issues.append("contains zero-width characters")
    if "\t" in text:
        issues.append("contains tab characters")
    if len(re.findall(r"^```", text, re.MULTILINE)) % 2:
        issues.append("has unbalanced fenced code blocks")
    if path.name != "README.ko.md":
        levels = [len(m.group(1)) for m in HEADING_RE.finditer(text)]
        for before, after in zip(levels, levels[1:]):
            if after > before + 1:
                issues.append(f"heading jump H{before}->H{after}")
                break
    return issues


def relative_link_issues(path: Path, text: str) -> list[str]:
    issues = []
    for match in LINK_RE.finditer(text):
        raw = match.group(1).strip()
        if not raw or raw.startswith(("#", "http://", "https://", "mailto:", "tel:")):
            continue
        target = raw.split()[0].strip("<>")
        target = unquote(target.split("#", 1)[0])
        if not target:
            continue
        resolved = (path.parent / target).resolve()
        try:
            resolved.relative_to(ROOT.resolve())
        except ValueError:
            issues.append(f"relative link escapes repository: {raw}")
            continue
        if not resolved.exists():
            issues.append(f"broken relative link: {raw}")
    return issues


def main() -> int:
    errors = []
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    state = json.loads(STATE.read_text(encoding="utf-8"))
    readme_ko = README_KO.read_text(encoding="utf-8")

    if manifest.get("source_commit") != state.get("last_processed_commit"):
        errors.append("course-manifest source_commit does not match .sync/upstream-state.json last_processed_commit")

    expected_blog_notes = 0
    expected_video_notes = 0
    checked_modules = 0

    for module in manifest.get("modules", []):
        number = int(module["number"])
        module_path = ROOT / f"docs/ko/module-{number:02d}.md"
        if not module_path.exists():
            errors.append(f"missing module index: {module_path.relative_to(ROOT)}")
            continue
        checked_modules += 1
        module_text = module_path.read_text(encoding="utf-8")

        for lesson in module.get("lessons", []):
            kind = lesson["type"]
            url = normalize_url(lesson["url"])
            if kind in {"blog", "video"}:
                if url not in module_text and url + "/" not in module_text:
                    errors.append(f"Module {number:02d}: source URL missing from module index: {url}")
                if url not in readme_ko and url + "/" not in readme_ko:
                    errors.append(f"Module {number:02d}: source URL missing from README.ko.md: {url}")

            if kind == "blog":
                expected_blog_notes += 1
                note = ROOT / f"docs/ko/blogs/module-{number:02d}/{blog_slug(url)}.md"
                if not note.exists():
                    errors.append(f"Module {number:02d}: missing Korean blog note: {note.relative_to(ROOT)}")
                else:
                    note_text = note.read_text(encoding="utf-8")
                    if url not in note_text and url + "/" not in note_text:
                        errors.append(f"{note.relative_to(ROOT)}: original source URL not recorded")

            elif kind == "video" and number not in VIDEO_NOTE_EXEMPT_MODULES:
                expected_video_notes += 1
                pos = module_text.find(url)
                if pos < 0:
                    pos = module_text.find(url + "/")
                nearby = module_text[max(0, pos - 300):pos + 1000] if pos >= 0 else ""
                match = VIDEO_LINK_RE.search(nearby)
                if not match:
                    errors.append(f"Module {number:02d}: detailed Korean video note is not linked near {url}")
                else:
                    note = ROOT / "docs/ko" / match.group(1)
                    if not note.exists():
                        errors.append(f"Module {number:02d}: missing Korean video note: {note.relative_to(ROOT)}")
                    else:
                        note_text = note.read_text(encoding="utf-8")
                        if url not in note_text:
                            errors.append(f"{note.relative_to(ROOT)}: original video URL not recorded")

    markdown_files = [README_KO]
    markdown_files.extend(sorted((ROOT / "docs/ko").rglob("*.md")))
    for path in markdown_files:
        text = path.read_text(encoding="utf-8")
        for issue in markdown_issues(path, text):
            errors.append(f"{path.relative_to(ROOT)}: {issue}")
        for issue in relative_link_issues(path, text):
            errors.append(f"{path.relative_to(ROOT)}: {issue}")

    print(f"Modules checked: {checked_modules}")
    print(f"Expected Korean blog notes: {expected_blog_notes}")
    print(f"Expected detailed video notes: {expected_video_notes} (Module 0 intro video exempt)")
    print(f"Errors: {len(errors)}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
