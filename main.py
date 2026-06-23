import argparse
from rich.console import Console
from rich.table import Table
from rich.text import Text
from auditor.parser import parse_requirements
from auditor.cve_checker import check_cve
from auditor.typo_checker import load_known_packages, check_typosquatting

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Supply Chain Dependency Auditor")
    parser.add_argument("--file", required=True, help="Path to requirements.txt")
    parser.add_argument("--output", help="Path to write JSON report")
    parser.add_argument("--ecosystem", choices=["python", "node"], default="python")
    args = parser.parse_args()

    packages = parse_requirements(args.file)
    known_packages = load_known_packages()          # ← BEFORE the loop, loaded once

    table = Table(title="Dependency Scan")
    table.add_column("Package", style="cyan")
    table.add_column("Version", style="white")
    table.add_column("CVEs", style="white")
    table.add_column("Typosquatting", style="white")

    for p in packages:                              # ← THIS is the loop
        console.print(f"Checking {p['name']}...", end="\r")

        cves = check_cve(p["name"], p["version"])
        if isinstance(cves, list) and cves:
            cve_cell = Text(str(len(cves)), style="red")
        elif cves == "UNVERIFIED":
            cve_cell = Text("UNVERIFIED", style="yellow")
        elif cves == "ERROR":
            cve_cell = Text("ERROR", style="yellow")
        else:
            cve_cell = Text("0", style="green")

        typo = check_typosquatting(p["name"], known_packages)
        if typo:
            typo_cell = Text(f"⚠ ~{typo['similar_to']}", style="red")
        else:
            typo_cell = Text("clean", style="green")

        table.add_row(p["name"], p["version"] or "unpinned", cve_cell, typo_cell)

    console.print(table)

if __name__ == "__main__":
    main()
