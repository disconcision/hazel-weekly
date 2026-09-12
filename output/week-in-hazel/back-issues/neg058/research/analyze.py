#!/usr/bin/env python3
"""Reproduce Issue -058 cutoff-dev metrics from a separate Hazel checkout."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

START = datetime.fromisoformat("2025-07-18T00:00:00+00:00")
END = datetime.fromisoformat("2025-07-25T00:00:00+00:00")
HISTORICAL_HEAD = "790b84e568197eb668591c4b05903aaeb6de20a9"


def utc(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("hazel_repo", type=Path)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()

    def git(*git_args: str) -> str:
        return subprocess.check_output(
            ["git", "-C", str(args.hazel_repo), *git_args], text=True
        )

    git("cat-file", "-e", f"{HISTORICAL_HEAD}^{{commit}}")
    rows = []
    for line in git("log", HISTORICAL_HEAD, "--format=%H%x09%cI%x09%an%x09%P%x09%s").splitlines():
        parts = line.split("\t", 4)
        if START <= utc(parts[1]) < END:
            rows.append(parts)

    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "period-dev-commits.tsv").write_text(
        "\n".join("\t".join(row) for row in rows) + "\n"
    )

    daily = Counter()
    authors = Counter()
    signature_daily = Counter()
    agent_daily = Counter()
    agent_shas = {key: [] for key in ("claude", "copilot", "openai", "codex", "chatgpt")}
    signature_shas = []
    for sha, when, author, parents, subject in rows:
        day = utc(when).date().isoformat()
        daily[day] += 1
        authors[author] += 1
        raw = git("cat-file", "commit", sha)
        header, body = raw.split("\n\n", 1)
        if re.search(r"^gpgsig(?:-sha256)? ", header, re.M):
            signature_daily[day] += 1
            signature_shas.append(sha)
        trailers = "\n".join(
            line for line in body.splitlines() if re.match(r"(?i)^co-authored-by:", line)
        )
        for key in agent_shas:
            if re.search(rf"(?i)\b{key}\b", trailers):
                agent_shas[key].append(sha)
        if sha in agent_shas["claude"]:
            agent_daily[day] += 1

    metrics = {
        "issue": "-058",
        "start_utc": START.isoformat(),
        "end_exclusive_utc": END.isoformat(),
        "period_head": HISTORICAL_HEAD,
        "commits": len(rows),
        "nonmerge": sum(len(row[3].split()) <= 1 for row in rows),
        "merges": sum(len(row[3].split()) > 1 for row in rows),
        "authors": dict(authors),
        "daily": dict(sorted(daily.items())),
        "daily_signature_headers": dict(sorted(signature_daily.items())),
        "daily_claude_credits": dict(sorted(agent_daily.items())),
        "agent_credit_objects": {key: len(value) for key, value in agent_shas.items()},
        "agent_credit_shas": agent_shas,
        "signature_headers": len(signature_shas),
        "signature_header_shas": signature_shas,
        "prs_opened": 12,
        "prs_merged": 11,
        "dev_merges": 11,
        "issues_opened": 12,
        "scope": (
            "UTC committer dates inside the week, reachable from the historical "
            "week-end dev head; signature presence only; exact Co-authored-by trailers. "
            "PR and issue flow comes from the 2026-09-12 authenticated GitHub search snapshot."
        ),
    }
    (args.output / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
