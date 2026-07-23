#!/usr/bin/env python3
"""Append newly-indexed publications from OpenAlex to _bibliography/papers.bib.

Matches works by ORCID iD. Only papers whose DOI is not already present in
papers.bib are appended, so hand-curated entries (abbr, selected, etc.) are
never overwritten. Runs weekly via .github/workflows/openalex-sync.yml.
"""

import re
import sys
import json
import urllib.request
import urllib.parse
from pathlib import Path

ORCID = "0000-0001-6607-2312"
MAILTO = "yujin71@gmail.com"  # polite pool; faster, more reliable OpenAlex access
BIB_PATH = Path(__file__).resolve().parent.parent / "_bibliography" / "papers.bib"


def fetch_works():
    works, cursor = [], "*"
    base = "https://api.openalex.org/works"
    while cursor:
        params = urllib.parse.urlencode({
            "filter": f"author.orcid:{ORCID}",
            "per-page": "200",
            "cursor": cursor,
            "mailto": MAILTO,
        })
        with urllib.request.urlopen(f"{base}?{params}", timeout=60) as r:
            data = json.load(r)
        works.extend(data.get("results", []))
        cursor = data.get("meta", {}).get("next_cursor")
    return works


def norm_doi(doi):
    if not doi:
        return None
    return doi.lower().replace("https://doi.org/", "").strip()


def existing_dois(text):
    return {m.lower().strip() for m in re.findall(r"doi\s*=\s*\{([^}]+)\}", text)}


def existing_keys(text):
    return set(re.findall(r"@\w+\{([^,]+),", text))


def to_bibtex_author(authorships):
    names = []
    for a in authorships:
        disp = (a.get("author") or {}).get("display_name") or ""
        disp = disp.strip()
        if not disp:
            continue
        parts = disp.split()
        if len(parts) == 1:
            names.append(parts[0])
        else:
            last = parts[-1]
            first = " ".join(parts[:-1])
            names.append(f"{last}, {first}")
    return " and ".join(names)


def make_key(work, taken):
    auth = work.get("authorships") or []
    last = "anon"
    if auth:
        disp = (auth[0].get("author") or {}).get("display_name") or "anon"
        last = disp.split()[-1].lower()
    year = str(work.get("publication_year") or "")
    title = re.sub(r"[^a-z]", "", (work.get("title") or "x").lower().split(" ")[0]) or "x"
    base = f"{last}{year}{title}"
    key, i = base, 1
    while key in taken:
        i += 1
        key = f"{base}{i}"
    taken.add(key)
    return key


def escape(s):
    return (s or "").replace("&", r"\&").replace("%", r"\%").replace("_", r"\_")


def build_entry(work, key):
    typ = work.get("type") or "article"
    biblio = work.get("biblio") or {}
    loc = (work.get("primary_location") or {}).get("source") or {}
    venue = loc.get("display_name") or ""
    doi = norm_doi(work.get("doi"))
    fields = [
        ("bibtex_show", "true"),
        ("title", escape(work.get("title") or "")),
        ("author", to_bibtex_author(work.get("authorships") or [])),
    ]
    entry_type = "inproceedings" if typ in ("proceedings-article", "proceedings") else "article"
    if entry_type == "inproceedings":
        fields.append(("booktitle", escape(venue)))
    else:
        fields.append(("journal", escape(venue)))
    if work.get("publication_year"):
        fields.append(("year", str(work["publication_year"])))
    if biblio.get("volume"):
        fields.append(("volume", biblio["volume"]))
    if biblio.get("issue"):
        fields.append(("number", biblio["issue"]))
    fp, lp = biblio.get("first_page"), biblio.get("last_page")
    if fp and lp:
        fields.append(("pages", f"{fp}--{lp}"))
    elif fp:
        fields.append(("pages", str(fp)))
    if doi:
        fields.append(("doi", doi))
        fields.append(("html", f"https://doi.org/{doi}"))
    body = ",\n".join(f"  {k:<12}= {{{v}}}" for k, v in fields)
    return f"@{entry_type}{{{key},\n{body}\n}}\n"


def main():
    text = BIB_PATH.read_text()
    have = existing_dois(text)
    keys = existing_keys(text)

    try:
        works = fetch_works()
    except Exception as e:  # noqa
        print(f"OpenAlex fetch failed: {e}", file=sys.stderr)
        return 1

    new_entries = []
    for w in works:
        doi = norm_doi(w.get("doi"))
        if not doi or doi in have:
            continue
        if not w.get("title"):
            continue
        have.add(doi)
        key = make_key(w, keys)
        new_entries.append(build_entry(w, key))

    if not new_entries:
        print("No new publications found.")
        return 0

    with BIB_PATH.open("a") as f:
        f.write("\n" + "\n".join(new_entries))
    print(f"Added {len(new_entries)} new publication(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
