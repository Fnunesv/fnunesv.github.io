#!/usr/bin/env python3
"""Fetch publications from ORCID and write to data/publications.yaml."""

import json
import urllib.request
import yaml
import sys
from pathlib import Path

ORCID_ID = "0000-0001-5107-0461"
OUT_FILE = Path(__file__).parent.parent / "data" / "publications.yaml"


def fetch_works(orcid_id):
    url = f"https://pub.orcid.org/v3.0/{orcid_id}/works"
    req = urllib.request.Request(url, headers={"Accept": "application/orcid+json"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def parse_works(data):
    pubs = []
    for group in data.get("group", []):
        summaries = group.get("work-summary", [])
        if not summaries:
            continue
        work = summaries[0]

        wtype = work.get("type", "")
        if wtype not in ("journal-article", "book-chapter", "preprint"):
            continue

        title = ""
        t = work.get("title", {})
        if t and t.get("title"):
            title = t["title"].get("value", "")

        year = ""
        pd = work.get("publication-date")
        if pd and pd.get("year"):
            year = pd["year"].get("value", "")

        journal = ""
        jt = work.get("journal-title")
        if jt:
            journal = jt.get("value", "")

        doi = ""
        extids = work.get("external-ids", {})
        for eid in extids.get("external-id", []):
            if eid.get("external-id-type") == "doi":
                doi = eid.get("external-id-value", "")
                break

        if title:
            pubs.append({
                "title": title,
                "year": year,
                "journal": journal,
                "doi": doi,
                "type": wtype,
            })

    pubs.sort(key=lambda p: p.get("year", "0"), reverse=True)
    return pubs


if __name__ == "__main__":
    print(f"Fetching ORCID works for {ORCID_ID}...")
    try:
        data = fetch_works(ORCID_ID)
        pubs = parse_works(data)
        OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(OUT_FILE, "w") as f:
            yaml.dump(pubs, f, allow_unicode=True, sort_keys=False)
        print(f"Wrote {len(pubs)} publications to {OUT_FILE}")
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
