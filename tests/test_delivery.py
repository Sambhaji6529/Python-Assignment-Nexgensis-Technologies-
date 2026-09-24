import math
import unittest

from src.assignment import assign_packages
from src.distance import euclidean_distance
from src.parser import normalize_input
from src.report import build_report


class DeliverySystemTests(unittest.TestCase):
    def test_euclidean_distance(self):
        self.assertAlmostEqual(euclidean_distance([0, 0], [3, 4]), 5.0)

    def test_nearest_agent(self):
        data = normalize_input(
            {
                "warehouses": {"W1": [0, 0]},
                "agents": {"A1": [3, 4], "A2": [20, 20]},
                "packages": [
                    {"id": "P1", "warehouse": "W1", "destination": [1, 1]}
                ],
            }
        )
        assignments = assign_packages(data)
        self.assertEqual(assignments[0]["agent"], "A1")

    def test_report_best_agent(self):
        stats = {
            "A1": {"packages_delivered": 1, "total_distance": 10.0},
            "A2": {"packages_delivered": 2, "total_distance": 30.0},
        }
        report = build_report(stats, package_count=3)
        self.assertEqual(report["A1"]["efficiency"], 10.0)
        self.assertEqual(report["A2"]["efficiency"], 15.0)
        self.assertEqual(report["best_agent"], "A1")


if __name__ == "__main__":
    unittest.main()
