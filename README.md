# ChainSentry

ChainSentry audits your Python project's direct dependencies for known CVEs,
typosquatting attacks, and package staleness — giving each package a
`HIGH / MEDIUM / LOW` risk score from a single CLI command.

**[▶ Watch terminal demo](https://asciinema.org/a/2ogy3ejtHEyUWGjM)**

---

## What it checks

| Signal | Source | Flags as |
|---|---|---|
| Known CVEs | OSV.dev API | HIGH if any found |
| Typosquatting | Levenshtein distance vs known packages | HIGH if similar name detected |
| Staleness | PyPI last upload date | MEDIUM if 2+ years |
| Unpinned version | No version specifier | MEDIUM (can't verify) |

---

## Install

```bash
git clone https://github.com/sajid-sec/ChainSentry.git
cd ChainSentry
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

Requires Python 3.10+. Tested on Ubuntu 24.04 LTS.

---

## Usage

```bash
# Scan a requirements.txt
python main.py --file requirements.txt

# Export full report to JSON
python main.py --file requirements.txt --output report.json
```

**Sample output:**

```
ChainSentry — Dependency Scan

 Package   Version   CVEs   Typosquatting   Last Updated   Risk
 django    4.2.0     82     clean           20d            HIGH
 flask     2.0.0     3      clean           125d           HIGH
 numpy     1.26.0    0      clean           2d             LOW
 click     unpinned  UNVE   clean           33d            MEDIUM

Scanned 4 packages — 2 HIGH, 1 MEDIUM, 1 LOW
```

## How scoring works

ChainSentry evaluates three independent signals per package:

1. **CVE check** — queries OSV.dev with the exact pinned version. Any returned vulnerability → `HIGH`
2. **Typosquatting check** — computes Levenshtein edit distance against a curated list of known packages. Distance ≤ 2 → `HIGH`
3. **Staleness check** — fetches last upload date from PyPI. Over 2 years → `MEDIUM`. Over 4 years → `MEDIUM` (abandoned)

Priority: typosquatting overrides everything, then CVEs, then staleness.
Unpinned packages are always `MEDIUM` — CVEs can't be verified without a fixed version.

---

## Limitations

- **Direct dependencies only** — transitive (nested) dependencies are not scanned
- **Curated reference list** — typosquatting checks ~143 well-known packages, not all of PyPI
- **Short names excluded** — names under 6 characters skipped to avoid false positives
- **OSV.dev coverage** — a clean result means no known OSV-tracked CVEs, not zero vulnerabilities
- **Environment markers stripped** — platform conditions like `; sys_platform == 'win32'` are ignored

---

## Tech stack

Python 3.12 · requests · rich · python-Levenshtein · pytest · OSV.dev API · PyPI JSON API

---

*Built by [Sajid](https://github.com/sajid-sec) — B.Tech-M.Tech CSE-Cybersecurity, UPSIFS Lucknow*
