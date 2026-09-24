"""CLI entry point for the Mystery Delivery System assignment."""

import argparse
import json
from pathlib import Path

from src.assignment import assign_packages
from src.delivery import simulate_deliveries
from src.parser import load_json, normalize_input
from src.report import build_report


def run(input_path: str, output_path: str) -> dict:
    raw_data = load_json(input_path)
    data = normalize_input(raw_data)
    assignments = assign_packages(data)
    stats = simulate_deliveries(data, assignments)
    report = build_report(stats, package_count=len(data["packages"]))

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)
        file.write("\n")

    return report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Simulate FastBox package assignment and delivery."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="data/base_case.json",
        help="Path to input JSON (default: data/base_case.json)",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="report.json",
        help="Path for generated report (default: report.json)",
    )
    args = parser.parse_args()

    try:
        report = run(args.input, args.output)
    except (OSError, ValueError, RuntimeError, json.JSONDecodeError) as exc:
        parser.error(str(exc))

    print(f"Report written to: {args.output}")
    print(json.dumps(report, indent=4))


if __name__ == "__main__":
    main()
