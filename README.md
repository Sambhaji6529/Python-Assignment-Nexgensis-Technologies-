# Mystery Delivery System — FastBox

Python solution for the Nexgensis Technologies assignment.

## Requirements

- Python 3.10+ recommended
- No third-party packages are required.

## Run the base case

From the project root:

```bash
python main.py
```

This reads `data/base_case.json` and creates `report.json`.

You can also specify another input and output file:

```bash
python main.py data/test_case_1.json -o reports/test_case_1_report.json
```

## Run all supplied test cases

```bash
python run_all_tests.py
```

This executes all ten supplied `test_case_*.json` files and verifies that the
number of packages delivered equals the number of input packages.

## Run unit tests

```bash
python -m unittest discover -s tests -v
```

## Implementation assumptions

1. **Nearest-agent assignment:** A package is assigned to the agent with the
   smallest Euclidean distance from the agent's initial location to that
   package's warehouse.
2. **Tie-breaking:** If two agents have exactly the same distance, the
   lexicographically smaller agent ID is selected. This keeps the result
   deterministic because the assignment does not define tie-breaking.
3. **Multi-package routing:** Each package is treated as an independent trip:
   `agent → warehouse → destination`. An agent's position is not updated after
   a package because the assignment does not define route optimization or
   multi-stop routing.
4. **Efficiency:** `total_distance / packages_delivered`. Agents with zero
   deliveries have efficiency `0.0`.
5. **Best agent:** The agent with the lowest average distance per delivered
   package is selected. Agents with zero deliveries are excluded. Ties use
   agent ID order.
6. **Input-format discrepancy:** The supplied `base_case.json` uses arrays of
   objects (`[{"id": "W1", "location": [0, 0]}]`) and `warehouse_id`, while the
   ten test cases use dictionaries (`{"W1": [0, 0]}`) and `warehouse`. The
   parser accepts both formats so the provided files can be tested without
   manual editing.
## Implementation assumptions

1. **Nearest-agent assignment:** A package is assigned to the agent with the
   smallest Euclidean distance from the agent's initial location to that
   package's warehouse.

2. **Tie-breaking:** If two agents have exactly the same distance, the
   lexicographically smaller agent ID is selected.

3. **Multi-package routing:** Each package is treated as an independent trip:
   `agent → warehouse → destination`.

4. **Efficiency:** `total_distance / packages_delivered`.
   Agents with zero deliveries have efficiency `0.0`.

5. **Best agent:** The agent with the lowest average distance per delivered
   package is selected. Agents with zero deliveries are excluded.

6. **Input-format discrepancy:** The supplied input files use different
   structures, so the parser accepts both supported formats.

7. **Sample-report discrepancy:** The numeric sample report provided in the
   PDF does not match the Euclidean-distance calculation described in the
   task when applied to the supplied base input. This implementation follows
   the explicit task rules rather than hard-coding the sample values.

## Project structure

```text
mystery_delivery_solution/
├── data/
│   ├── base_case.json
│   ├── test_case_1.json ... test_case_10.json
├── src/
│   ├── assignment.py
│   ├── delivery.py
│   ├── distance.py
│   ├── parser.py
│   └── report.py
├── tests/
│   └── test_delivery.py
├── main.py
├── run_all_tests.py
├── README.md
└── requirements.txt
```
