import argparse
import json
from rich.console import Console
from rich.table import Table
from rich.text import Text
from auditor.parser import parse_requirements
from auditor.cve_checker import check_cve
from auditor.typo_checker import load_known_packages, check_typosquatting
from auditor.meta_checker import get_pypi_metadata
from auditor.scorer import calculate_risk

console = Console()

def main():
    parser = argparse.ArgumentParser(description="ChainSentry - Supply Chain Dependency Auditor")
    parser.add_argument("--file", required=True, help="Path to requirements.txt")
    parser.add_argument("--output", help="Path to write JSON report")
    parser.add_argument("--ecosystem", choices=["python", "node"], default="python")
    args = parser.parse_args()

    packages = parse_requirements(args.file)
    known_packages = load_known_packages()

    table = Table(title="ChainSentry — Dependency Scan")
    table.add_column("Package", style="cyan")
    table.add_column("Version", style="white")
    table.add_column("CVEs", style="white")
    table.add_column("Typosquatting", style="white")
    table.add_column("Last Updated", style="white")
    table.add_column("Risk", style="white")

    results = []

    for p in packages:
        console.print(f"  Scanning {p['name']}...", end="\r")

        cves = check_cve(p["name"], p["version"])
        typo = check_typosquatting(p["name"], known_packages)
        meta = get_pypi_metadata(p["name"])
        risk = calculate_risk(cves, typo, meta)

        results.append({
            "name": p["name"],
            "version": p["version"],
            "cves": cves,
            "typosquatting": typo,
            "metadata": meta,
            "risk": risk
        })

        # CVE cell
        if isinstance(cves, list) and cves:
            cve_cell = Text(str(len(cves)), style="red")
        elif cves == "UNVERIFIED":
            cve_cell = Text("UNVERIFIED", style="yellow")
        else:
            cve_cell = Text("0", style="green")

        # Typo cell
        typo_cell = Text(f"~{typo['similar_to']}", style="red") if typo else Text("clean", style="green")

        # Staleness cell
        days = meta.get("days_since_update")
        if days is None:
            staleness = Text("unknown", style="yellow")
        elif days > 1460:
            staleness = Text(f"{days}d (abandoned)", style="red")
        elif days > 730:
            staleness = Text(f"{days}d (stale)", style="yellow")
        else:
            staleness = Text(f"{days}d", style="green")

        # Risk cell
        risk_styles = {"HIGH": "red", "MEDIUM": "yellow", "LOW": "green"}
        risk_cell = Text(risk, style=risk_styles[risk])

        table.add_row(p["name"], p["version"] or "unpinned",
                      cve_cell, typo_cell, staleness, risk_cell)

    console.print(table)

    # Summary line
    high = sum(1 for r in results if r["risk"] == "HIGH")
    med  = sum(1 for r in results if r["risk"] == "MEDIUM")
    low  = sum(1 for r in results if r["risk"] == "LOW")
    console.print(f"\n  Scanned {len(results)} packages — "
                  f"[red]{high} HIGH[/red], [yellow]{med} MEDIUM[/yellow], [green]{low} LOW[/green]")

    # JSON export
    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2, default=str)
        console.print(f"  Report saved to [cyan]{args.output}[/cyan]")

if __name__ == "__main__":
    main()

