"""Run the supplied test cases and verify package-count conservation."""

import json
from pathlib import Path

from main import run


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
REPORT_DIR = ROOT / "reports"


def main() -> None:
    REPORT_DIR.mkdir(exist_ok=True)
    test_files = sorted(DATA_DIR.glob("test_case_*.json"))

    if not test_files:
        raise SystemExit("No test_case_*.json files found in data/")

    passed = 0
    for input_file in test_files:
        output_file = REPORT_DIR / f"{input_file.stem}_report.json"
        report = run(str(input_file), str(output_file))
        with input_file.open("r", encoding="utf-8") as file:
            input_data = json.load(file)

        expected = len(input_data["packages"])
        actual = sum(
            value["packages_delivered"]
            for key, value in report.items()
            if key != "best_agent"
        )

        if expected != actual:
            raise AssertionError(
                f"{input_file.name}: expected {expected} packages, got {actual}"
            )

        passed += 1
        print(f"PASS  {input_file.name}: {actual} packages delivered")

    print(f"\nAll tests passed: {passed}/{len(test_files)}")


if __name__ == "__main__":
    main()
