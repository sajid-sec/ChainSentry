# ChainSentry

A Python CLI tool that audits direct dependencies for CVEs, typosquatting,
and package staleness using OSV.dev and PyPI metadata APIs.

## Install

git clone https://github.com/sajid-sec/ChainSentry.git
cd ChainSentry
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

## Usage

python main.py --file requirements.txt
python main.py --file requirements.txt --output report.json

## How scoring works

Each package is checked against three signals:
- CVEs via OSV.dev API
- Typosquatting via Levenshtein distance against known packages
- Staleness via PyPI last-upload date

Risk is HIGH if CVEs found or typosquatting detected, MEDIUM if unpinned
or stale (2+ years), LOW if all signals are clean.

## Limitations

- Scans direct dependencies only — transitive deps not covered
- Typosquatting detection uses a curated list of ~143 packages, not all of PyPI
- Short package names (under 6 chars) skipped to avoid false positives
- OSV.dev coverage is not exhaustive — absence of CVEs is not a clean bill
- Environment markers in version specifiers are stripped, not evaluated
