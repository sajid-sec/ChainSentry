# ChainSentry

ChainSentry audits your Python project's direct dependencies for known CVEs,
typosquatting attacks, and package staleness — giving each package a
`HIGH / MEDIUM / LOW` risk score from a single CLI command.

[![asciicast](https://asciinema.org/a/2ogy3ejtHEyUWGjM.svg)](https://asciinema.org/a/2ogy3ejtHEyUWGjM)
---

## What it checks

| Signal | Source | Flags as |
|---|---|---|
| Known CVEs | OSV.dev API | HIGH if any found |
| Typosquatting | Levenshtein distance vs known packages | HIGH if similar name detected |
| Staleness | PyPI last upload date | MEDIUM if 2+ years, MEDIUM if abandoned |
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

**Scan a requirements.txt:**
```bash
python main.py --file requirements.txt
```

**Export full report to JSON:**
```bash
python main.py --file requirements.txt --output report.json
```

**Sample output:**
ChainSentry — Dependency Scan
┏━━━━━━━━━━┳━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━┳━━━━━━━━┓

┃ Package  ┃ Version ┃ CVEs ┃ Typosquatting ┃ Last Updated ┃ Risk   ┃

┡━━━━━━━━━━╇━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━╇━━━━━━━━┩

│ django   │ 4.2.0   │ 82   │ clean         │ 20d          │ HIGH   │

│ flask    │ 2.0.0   │ 3    │ clean         │ 125d         │ HIGH   │

│ numpy    │ 1.26.0  │ 0    │ clean         │ 2d           │ LOW    │

│ click    │ unpinned│ UNVE │ clean         │ 33d          │ MEDIUM │

└──────────┴─────────┴──────┴───────────────┴──────────────┴────────┘
Scanned 4 packages — 2 HIGH, 1 MEDIUM, 1 LOW
---

## How scoring works

ChainSentry evaluates three independent signals per package and combines
them into a single risk score:

1. **CVE check** — queries OSV.dev with the exact pinned version.
   Any returned vulnerability → HIGH.

2. **Typosquatting check** — computes Levenshtein edit distance between
   the package name and a curated list of known packages. Distance ≤ 2
   from a known package name → HIGH.

3. **Staleness check** — fetches the last upload date from PyPI.
   Over 2 years → MEDIUM. Over 4 years → MEDIUM (abandoned).

Priority order: typosquatting overrides everything, then CVEs, then
staleness. Unpinned packages are always MEDIUM since CVEs can't be
verified without a fixed version.

---

## Limitations

- **Direct dependencies only** — transitive (nested) dependencies are
  not scanned. A vulnerable transitive dep will not appear in results.
- **Curated reference list** — typosquatting checks against ~143
  well-known packages, not all of PyPI. Obscure typosquats may be missed.
- **Short names excluded** — package names under 6 characters are skipped
  to avoid false positives (edit distance on short strings is unreliable).
- **OSV.dev coverage** — not every CVE is in OSV. A clean result means
  no known OSV-tracked vulnerabilities, not no vulnerabilities at all.
- **Environment markers stripped** — version specifiers with platform
  conditions (e.g. `; sys_platform == 'win32'`) are parsed but markers
  are ignored. The version is scanned as-is.

---

## Tech stack

Python 3.12 · requests · rich · python-Levenshtein · pytest · OSV.dev API · PyPI JSON API

---

*Built by [Sajid Ali](https://github.com/sajid-sec) — B.Tech CSE-Cybersecurity, UPSIFS Lucknow*
