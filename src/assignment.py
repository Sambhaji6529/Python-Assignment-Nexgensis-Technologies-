"""Package-to-agent assignment logic."""

from typing import Any

from .distance import euclidean_distance


def assign_packages(data: dict[str, Any]) -> list[dict[str, Any]]:
    """Assign each package to its nearest agent.

    Distance is measured from the agent's initial location to the package's
    warehouse, exactly as specified in the assignment.

    Tie-breaking assumption: when two agents are at exactly the same distance,
    the lexicographically smaller agent ID is selected. This makes the result
    deterministic because the assignment does not define a tie-breaking rule.
    """
    warehouses = data["warehouses"]
    agents = data["agents"]
    assignments: list[dict[str, Any]] = []

    for package in data["packages"]:
        warehouse_id = package["warehouse"]
        warehouse_location = warehouses[warehouse_id]

        candidates = [
            (
                euclidean_distance(agent_location, warehouse_location),
                agent_id,
            )
            for agent_id, agent_location in agents.items()
        ]
        distance_to_warehouse, agent_id = min(candidates, key=lambda item: (item[0], item[1]))

        assignments.append(
            {
                "package_id": package["id"],
                "warehouse": warehouse_id,
                "destination": package["destination"],
                "agent": agent_id,
                "agent_to_warehouse": distance_to_warehouse,
            }
        )

    return assignments
