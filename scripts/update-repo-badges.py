#!/usr/bin/env python3
"""Render repository counters using authenticated GitHub metadata, even when private."""
import argparse
from datetime import datetime, timezone
from html import escape
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/images/readme"
COUNTERS = [
    ("stars", "Stars", "stargazers_count", "#b7791f"),
    ("forks", "Forks", "forks_count", "#2878a3"),
    ("watchers", "Watchers", "subscribers_count", "#608445"),
]


def badge(label, count, color):
    value = f"{count:,}"
    left, right = len(label) * 7 + 18, len(value) * 7 + 18
    width = left + right
    title = escape(f"{label}: {value}")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="20" role="img" aria-label="{title}">
<title>{title}</title>
<clipPath id="edge"><rect width="{width}" height="20" rx="3"/></clipPath>
<g clip-path="url(#edge)"><path fill="#555" d="M0 0h{left}v20H0z"/><path fill="{color}" d="M{left} 0h{right}v20H{left}z"/></g>
<g fill="#fff" text-anchor="middle" font-family="Verdana,DejaVu Sans,sans-serif" font-size="11">
<text x="{left / 2}" y="14">{escape(label)}</text><text x="{left + right / 2}" y="14">{value}</text>
</g></svg>
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default="JYS1025/paper-figure")
    args = parser.parse_args()
    if not re.fullmatch(r"[\w.-]+/[\w.-]+", args.repo):
        parser.error("Expected owner/repository")
    result = subprocess.run(
        ["gh", "api", f"repos/{args.repo}"],
        check=True, capture_output=True, text=True, timeout=60,
    )
    data = json.loads(result.stdout)
    if data.get("full_name", "").lower() != args.repo.lower():
        raise ValueError("GitHub returned a different repository")
    counts = {}
    for key, _, field, _ in COUNTERS:
        value = data.get(field)
        if type(value) is not int or value < 0:
            raise ValueError(f"Missing or invalid GitHub field: {field}")
        counts[key] = value
    path = OUT / "github-stats.json"
    old = json.loads(path.read_text()) if path.exists() else {}
    traffic = old.get("traffic")
    traffic_result = subprocess.run(
        ["gh", "api", f"repos/{args.repo}/traffic/views"],
        capture_output=True, text=True, timeout=60,
    )
    if traffic_result.returncode == 0:
        views = json.loads(traffic_result.stdout)
        for field in ("count", "uniques"):
            if type(views.get(field)) is not int or views[field] < 0:
                raise ValueError(f"Missing or invalid traffic field: {field}")
        traffic = {
            "views14d": views["count"],
            "uniqueVisitors14d": views["uniques"],
            "observedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
    elif "HTTP 403" in traffic_result.stderr or "HTTP 404" in traffic_result.stderr:
        print("Traffic access unavailable; preserving the dated snapshot. See docs/repository-badges.md.")
    else:
        raise RuntimeError("GitHub traffic request failed; previous snapshot preserved")
    # Validate the entire response before replacing any previous snapshot.
    OUT.mkdir(parents=True, exist_ok=True)
    for key, label, _, color in COUNTERS:
        (OUT / f"badge-{key}.svg").write_text(badge(label, counts[key], color))
    record = {"repository": data["full_name"], "counts": counts}
    record["observedAt"] = old.get("observedAt")
    if old.get("repository") != record["repository"] or old.get("counts") != counts or not record["observedAt"]:
        record["observedAt"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    if traffic:
        record["traffic"] = traffic
        dated_label = f"Views 14d ({traffic['observedAt'][:10]})"
        (OUT / "badge-views.svg").write_text(badge(dated_label, traffic["views14d"], "#6b7280"))
    path.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(record))


if __name__ == "__main__":
    main()
