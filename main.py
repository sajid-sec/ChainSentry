import argparse
from rich.console import Console
from rich.table import Table
from auditor.parser import parse_requirements

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

    for p in packages:
        table.add_row(p["name"], p["version"] or "unpinned")

    console.print(table)

if __name__ == "__main__":
    main()
