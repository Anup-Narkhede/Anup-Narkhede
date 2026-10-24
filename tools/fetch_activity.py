"""Fetch the public contribution calendar for the Signal plate.

    GITHUB_TOKEN=... python tools/fetch_activity.py [login]

Writes tools/data/contributions.json. Uses only the standard library so the
GitHub Action needs nothing beyond Python.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

LOGIN = sys.argv[1] if len(sys.argv) > 1 else "Anup-Narkhede"
OUT = Path(__file__).resolve().parent / "data" / "contributions.json"
QUERY = """query($login:String!){user(login:$login){contributionsCollection{contributionCalendar{
totalContributions weeks{contributionDays{date contributionCount}}}}}}"""


def main() -> None:
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        sys.exit("GITHUB_TOKEN is required")
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:  # noqa: S310 - fixed https endpoint
        data = json.load(r)
    if "errors" in data:
        sys.exit(f"GraphQL error: {data['errors']}")
    cal = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
    days = [d for w in cal["weeks"] for d in w["contributionDays"]]
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({
        "login": LOGIN,
        "fetched": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "total": cal["totalContributions"],
        "days": [[d["date"], d["contributionCount"]] for d in days],
    }, indent=0) + "\n")
    print(f"{OUT.name}: {cal['totalContributions']} contributions over {len(days)} days")


if __name__ == "__main__":
    main()
