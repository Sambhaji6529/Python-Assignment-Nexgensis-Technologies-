"""Delivery simulation and statistics."""

from typing import Any

from .distance import euclidean_distance


def simulate_deliveries(
    data: dict[str, Any], assignments: list[dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    """Calculate delivery distance and aggregate statistics per agent.

    Assumption for undefined multi-package routing: each package is treated as
    an independent delivery trip from the agent's initial location to the
    package warehouse and then to the package destination. The agent's position
    is not updated between packages because the assignment does not define a
    route-optimization or multi-stop routing policy.
    """
    warehouses = data["warehouses"]
    agents = data["agents"]

    stats = {
        agent_id: {
            "packages_delivered": 0,
            "total_distance": 0.0,
            "package_details": [],
        }
        for agent_id in agents
    }

    for assignment in assignments:
        agent_id = assignment["agent"]
        warehouse_location = warehouses[assignment["warehouse"]]
        agent_location = agents[agent_id]
        destination = assignment["destination"]

        agent_to_warehouse = euclidean_distance(agent_location, warehouse_location)
        warehouse_to_destination = euclidean_distance(warehouse_location, destination)
        total_distance = agent_to_warehouse + warehouse_to_destination

        stats[agent_id]["packages_delivered"] += 1
        stats[agent_id]["total_distance"] += total_distance
        stats[agent_id]["package_details"].append(
            {
                "package_id": assignment["package_id"],
                "warehouse": assignment["warehouse"],
                "agent_to_warehouse": agent_to_warehouse,
                "warehouse_to_destination": warehouse_to_destination,
                "distance": total_distance,
            }
        )

    return stats
