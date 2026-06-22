import argparse
from rich.console import Console
from rich.table import Table
from rich.text import Text
from auditor.parser import parse_requirements
from auditor.cve_checker import check_cve

console = Console()

def main():
    parser = argparse.ArgumentParser(description="Supply Chain Dependency Auditor")
    parser.add_argument("--file", required=True, help="Path to requirements.txt or package.json")
    parser.add_argument("--output", help="Path to write JSON report")
    parser.add_argument("--format", choices=["table", "json", "html"], default="table")
    parser.add_argument("--ecosystem", choices=["python", "node"], default="python")
    args = parser.parse_args()

    packages = parse_requirements(args.file)

    table = Table(title="Dependency Scan")
    table.add_column("Package", style="cyan")
    table.add_column("Version", style="white")
    table.add_column("CVEs", style="white")

    for p in packages:
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

        table.add_row(p["name"], p["version"] or "unpinned", cve_cell)

    console.print(table)

if __name__ == "__main__":
    main()
