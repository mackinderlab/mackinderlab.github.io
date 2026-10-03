"""Fill in missing publication details from DOIs before the site builds.

Editors can add a paper to _data/publications.yml with only a DOI. This script
looks up any entry that is missing a title, authors, journal or year on Crossref
and fills the gaps. Fields an editor has typed are never overwritten.

It runs in the GitHub Actions build (see .github/workflows/pages.yml), so the
filled-in details appear on the site without being written back to the repo.
If Crossref cannot be reached, the build carries on with what is there.
"""

import json
import sys
import urllib.request
from pathlib import Path

import yaml

DATA = Path(__file__).resolve().parent.parent / "_data" / "publications.yml"
FIELDS = ("title", "authors", "journal", "year")
CROSSREF = "https://api.crossref.org/works/"


def lookup(doi):
    req = urllib.request.Request(
        CROSSREF + urllib.request.quote(doi),
        headers={"User-Agent": "mackinderlab-website (mailto:luke.mackinder@york.ac.uk)"},
    )
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.load(resp)["message"]


def format_authors(people):
    names = []
    for p in people:
        family = p.get("family")
        if not family:
            if p.get("name"):
                names.append(p["name"])
            continue
        initials = "".join(part[0] for part in p.get("given", "").replace("-", " ").split() if part)
        names.append(f"{family} {initials}".strip())
    return ", ".join(names)


def details_from(msg):
    year = None
    for key in ("published-print", "published-online", "issued", "posted"):
        parts = msg.get(key, {}).get("date-parts", [[None]])
        if parts and parts[0] and parts[0][0]:
            year = parts[0][0]
            break
    journal = (msg.get("container-title") or [None])[0]
    if not journal and msg.get("type") == "posted-content":
        journal = msg.get("institution", [{}])[0].get("name") or "Preprint"
    return {
        "title": (msg.get("title") or [None])[0],
        "authors": format_authors(msg.get("author", [])),
        "journal": journal,
        "year": year,
    }


def main():
    raw = DATA.read_text(encoding="utf-8")
    entries = yaml.safe_load(raw) or []
    filled = 0
    for entry in entries:
        doi = str(entry.get("doi") or "").strip()
        for prefix in ("https://doi.org/", "http://doi.org/", "https://dx.doi.org/", "http://dx.doi.org/", "doi:"):
            if doi.lower().startswith(prefix):
                doi = doi[len(prefix):]
        if not doi or all(entry.get(f) for f in FIELDS):
            continue
        try:
            found = details_from(lookup(doi))
        except Exception as exc:  # network or bad DOI: keep building
            print(f"warning: could not look up {doi}: {exc}", file=sys.stderr)
            continue
        for field in FIELDS:
            if not entry.get(field) and found.get(field):
                entry[field] = found[field]
        if found.get("journal", "").lower().startswith(("biorxiv", "cold spring harbor")):
            entry.setdefault("preprint", True)
        filled += 1
        print(f"filled {doi}: {entry.get('title')}")

    if filled:
        entries.sort(key=lambda e: -(int(e.get("year") or 0)))
        header_lines = []
        for line in raw.splitlines(keepends=True):
            if not line.startswith("#"):
                break
            header_lines.append(line)
        header = "".join(header_lines)
        DATA.write_text(header + yaml.safe_dump(entries, allow_unicode=True, sort_keys=False, width=1000), encoding="utf-8")
    print(f"{filled} publication(s) filled from DOIs")


if __name__ == "__main__":
    main()
