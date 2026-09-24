"""Input loading and normalization for the Mystery Delivery System."""

import json
from pathlib import Path
from typing import Any


def load_json(path: str | Path) -> dict[str, Any]:
    """Load and parse a JSON object from *path*."""
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("The JSON root must be an object.")
    return data


def _normalize_locations(value: Any, field_name: str) -> dict[str, list[float]]:
    """Normalize either mapping or list-of-records location formats."""
    if isinstance(value, dict):
        result = value
    elif isinstance(value, list):
        result = {}
        for item in value:
            if not isinstance(item, dict) or "id" not in item:
                raise ValueError(
                    f"Each item in '{field_name}' must contain an 'id' and a location."
                )
            location = item.get("location")
            if location is None:
                raise ValueError(f"Missing location for {field_name} '{item['id']}'.")
            result[str(item["id"])] = location
    else:
        raise ValueError(f"'{field_name}' must be an object or a list of objects.")

    normalized: dict[str, list[float]] = {}
    for identifier, location in result.items():
        if not isinstance(location, (list, tuple)) or len(location) != 2:
            raise ValueError(
                f"Location for '{identifier}' must be a 2-D coordinate like [x, y]."
            )
        normalized[str(identifier)] = [float(location[0]), float(location[1])]
    return normalized


def normalize_input(data: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalize supported assignment input formats.

    The supplied base_case.json uses list records and `warehouse_id`, while the
    ten supplied test cases use dictionaries and `warehouse`. Both are accepted
    so the program is robust to the two formats provided with the assignment.
    """
    warehouses = _normalize_locations(data.get("warehouses"), "warehouses")
    agents = _normalize_locations(data.get("agents"), "agents")

    packages = data.get("packages")
    if not isinstance(packages, list):
        raise ValueError("'packages' must be a list.")

    normalized_packages: list[dict[str, Any]] = []
    seen_package_ids: set[str] = set()

    for index, package in enumerate(packages, start=1):
        if not isinstance(package, dict):
            raise ValueError(f"Package #{index} must be an object.")

        package_id = package.get("id")
        warehouse_id = package.get("warehouse", package.get("warehouse_id"))
        destination = package.get("destination")

        if package_id is None:
            raise ValueError(f"Package #{index} is missing 'id'.")
        if warehouse_id is None:
            raise ValueError(f"Package '{package_id}' is missing 'warehouse'.")
        if destination is None:
            raise ValueError(f"Package '{package_id}' is missing 'destination'.")
        if warehouse_id not in warehouses:
            raise ValueError(
                f"Package '{package_id}' references unknown warehouse '{warehouse_id}'."
            )
        if not isinstance(destination, (list, tuple)) or len(destination) != 2:
            raise ValueError(
                f"Destination for package '{package_id}' must be [x, y]."
            )

        package_id = str(package_id)
        if package_id in seen_package_ids:
            raise ValueError(f"Duplicate package id: '{package_id}'.")
        seen_package_ids.add(package_id)

        normalized_packages.append(
            {
                "id": package_id,
                "warehouse": str(warehouse_id),
                "destination": [float(destination[0]), float(destination[1])],
            }
        )

    if not warehouses:
        raise ValueError("At least one warehouse is required.")
    if not agents:
        raise ValueError("At least one delivery agent is required.")

    return {
        "warehouses": warehouses,
        "agents": agents,
        "packages": normalized_packages,
    }
