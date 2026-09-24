from typing import Any
def build_report(stats: dict[str, dict[str, Any]], package_count: int) -> dict[str, Any]:
    """Build the required report with rounded numeric values."""
    report: dict[str, Any] = {}

    active_agents = []

    for agent_id in sorted(stats):
        delivered = stats[agent_id]["packages_delivered"]
        total_distance = stats[agent_id]["total_distance"]

        raw_efficiency = total_distance / delivered if delivered else 0.0

        if delivered > 0:
            active_agents.append((raw_efficiency, agent_id))

        report[agent_id] = {
            "packages_delivered": delivered,
            "total_distance": round(total_distance, 2),
            "efficiency": round(raw_efficiency, 2),
        }

    report["best_agent"] = (
        min(active_agents, key=lambda item: (item[0], item[1]))[1]
        if active_agents
        else None
    )

    delivered_total = sum(
        details["packages_delivered"]
        for details in stats.values()
    )

    if delivered_total != package_count:
        raise RuntimeError(
            f"Package count mismatch: delivered={delivered_total}, input={package_count}"
        )

    return report