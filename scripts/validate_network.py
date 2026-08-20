"""Validate the released representative Alaska network using only stdlib.

This validates the positive-flow topology in data/processed.
"""

from __future__ import annotations

import csv
import json
import math
from collections import defaultdict, deque
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"
RULES = json.loads((ROOT / "config" / "domain_rules.json").read_text())

EXPECTED = {
    "suppliers": 16,
    "refineries": 5,
    "import_hubs": 11,
    "selected_terminals": 52,
    "selected_physical_terminals": 51,
    "eligible_physical_terminals": 56,
    "customers": 931,
    "arcs": 1022,
    "upstream_arcs": 61,
    "downstream_arcs": 961,
    "component_sizes": [993, 3, 3],
}


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def num(value: str, label: str) -> float:
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise AssertionError(f"{label}: expected number, found {value!r}") from exc
    assert math.isfinite(result), f"{label}: nonfinite number"
    return result


def close(actual: float, expected: float, label: str, tolerance: float = 1e-4):
    assert abs(actual - expected) <= tolerance, (
        f"{label}: {actual:.10f} != {expected:.10f} "
        f"(|difference|={abs(actual - expected):.3e})"
    )


def connected_component_sizes(arcs):
    adjacency = defaultdict(set)
    for row in arcs:
        origin, destination = row["origin_id"], row["destination_id"]
        adjacency[origin].add(destination)
        adjacency[destination].add(origin)
    seen, sizes = set(), []
    for start in adjacency:
        if start in seen:
            continue
        queue, size = deque([start]), 0
        seen.add(start)
        while queue:
            node = queue.popleft()
            size += 1
            for neighbor in adjacency[node]:
                if neighbor not in seen:
                    seen.add(neighbor)
                    queue.append(neighbor)
        sizes.append(size)
    return sorted(sizes, reverse=True)


def main():
    refineries = read_csv("refineries.csv")
    import_hubs = read_csv("marine_import_hubs.csv")
    terminals = read_csv("distribution_terminals.csv")
    customers = read_csv("last_mile_locations.csv")
    arcs = read_csv("network_arcs.csv")

    assert len(refineries) == EXPECTED["refineries"]
    assert len(import_hubs) == EXPECTED["import_hubs"]
    assert len(customers) == EXPECTED["customers"]
    assert len(arcs) == EXPECTED["arcs"]

    refinery_ids = {row["refinery_id"] for row in refineries}
    import_hub_ids = {row["hub_id"] for row in import_hubs}
    supplier_ids = refinery_ids | import_hub_ids
    customer_ids = {row["cluster_id"] for row in customers}
    assert len(supplier_ids) == EXPECTED["suppliers"]
    assert len(customer_ids) == len(customers), "duplicate customer IDs"

    eligible_terminal_ids = {
        row["TERM_ID"]
        for row in terminals
        if num(row["refined_capacity_weight_barrels"], row["TERM_ID"]) > 0
    }
    assert len(eligible_terminal_ids) == EXPECTED["eligible_physical_terminals"]

    upstream = [row for row in arcs if row["arc_stage"] in {"R-D", "P-D"}]
    downstream = [row for row in arcs if row["arc_stage"] == "D-L"]
    assert len(upstream) == EXPECTED["upstream_arcs"]
    assert len(downstream) == EXPECTED["downstream_arcs"]
    assert len(upstream) + len(downstream) == len(arcs)

    selected_suppliers = {row["origin_id"] for row in upstream}
    selected_terminals = (
        {row["destination_id"] for row in upstream}
        | {row["origin_id"] for row in downstream}
    )
    selected_customers = {row["destination_id"] for row in downstream}
    physical_selected = selected_terminals - {"D_KUPARUK_LOCAL"}

    assert selected_suppliers == supplier_ids
    assert selected_customers == customer_ids
    assert len(selected_terminals) == EXPECTED["selected_terminals"]
    assert len(physical_selected) == EXPECTED["selected_physical_terminals"]
    assert physical_selected <= eligible_terminal_ids
    assert "D_KUPARUK_LOCAL" in selected_terminals

    seen_arcs = set()
    tolerance = float(RULES["flow_tolerance_barrels"])
    for row in arcs:
        key = (row["arc_stage"], row["origin_id"], row["destination_id"])
        assert key not in seen_arcs, f"duplicate arc {key}"
        seen_arcs.add(key)
        assert row["origin_id"] != row["destination_id"], f"self-loop {key}"
        assert num(row["flow_barrels"], f"flow {key}") > tolerance
        assert num(row["distance_km"], f"distance {key}") >= 0
        if row["arc_stage"] in {"R-D", "P-D"}:
            assert row["origin_id"] in supplier_ids
            assert row["destination_id"] in selected_terminals
        else:
            assert row["origin_id"] in selected_terminals
            assert row["destination_id"] in customer_ids

    upstream_out, upstream_in = defaultdict(set), defaultdict(set)
    downstream_out, downstream_in = defaultdict(set), defaultdict(set)
    for row in upstream:
        upstream_out[row["origin_id"]].add(row["destination_id"])
        upstream_in[row["destination_id"]].add(row["origin_id"])
    for row in downstream:
        downstream_out[row["origin_id"]].add(row["destination_id"])
        downstream_in[row["destination_id"]].add(row["origin_id"])

    for rule in RULES["local_three_tier_chains"]:
        s, t, c = rule["supplier"], rule["terminal"], rule["customer"]
        assert upstream_out[s] == {t}, f"{rule['rule_id']}: supplier not local"
        assert upstream_in[t] == {s}, f"{rule['rule_id']}: terminal inflow not local"
        assert downstream_out[t] == {c}, f"{rule['rule_id']}: terminal outflow not local"
        assert downstream_in[c] == {t}, f"{rule['rule_id']}: customer inflow not local"

    for rule in RULES["exclusive_terminal_customer_pairs"]:
        t, c = rule["terminal"], rule["customer"]
        assert downstream_out[t] == {c}, f"{rule['rule_id']}: terminal not exclusive"
        assert downstream_in[c] == {t}, f"{rule['rule_id']}: customer not exclusive"

    for rule in RULES["excluded_terminals"]:
        assert rule["terminal"] not in selected_terminals, rule["rule_id"]
    for rule in RULES["forbidden_supply_terminal_arcs"]:
        key = ("R-D", rule["origin"], rule["destination"])
        assert key not in seen_arcs, rule["rule_id"]

    for terminal, radius in RULES["terminal_service_radius_km"].items():
        for row in downstream:
            if row["origin_id"] == terminal:
                assert num(row["distance_km"], terminal) <= float(radius) + 1e-6

    for rule in RULES["required_group_connections"]:
        flow = sum(
            num(row["flow_barrels"], rule["rule_id"])
            for row in upstream
            if row["origin_id"] == rule["origin"]
            and row["destination_id"] in set(rule["destinations"])
        )
        assert flow + tolerance >= float(rule["minimum_aggregate_flow_barrels"])

    demand = {
        row["cluster_id"]: num(row["model_capacity"], row["cluster_id"])
        for row in customers
    }
    delivered = defaultdict(float)
    for row in downstream:
        delivered[row["destination_id"]] += num(row["flow_barrels"], row["arc_id"])
    for customer_id, expected in demand.items():
        close(delivered[customer_id], expected, f"customer balance {customer_id}")

    total_demand = sum(demand.values())
    total_upstream = sum(num(row["flow_barrels"], row["arc_id"]) for row in upstream)
    total_downstream = sum(num(row["flow_barrels"], row["arc_id"]) for row in downstream)
    close(total_upstream, total_demand, "total upstream flow", tolerance=0.01)
    close(total_downstream, total_demand, "total downstream flow", tolerance=0.01)

    supplier_capacity = sum(
        num(row["model_capacity"], "supplier capacity")
        for row in refineries + import_hubs
    )
    close(
        supplier_capacity,
        RULES["construction_capacity_ratios"]["supplier_to_demand"] * total_demand,
        "supplier construction capacity",
        tolerance=0.01,
    )

    physical_terminal_capacity = sum(
        num(row["model_capacity"], row["TERM_ID"]) for row in terminals
    )
    kuparuk_demand = demand["L_KUPARUK_INDUSTRIAL_OPERATIONS"]
    terminal_ratio = RULES["construction_capacity_ratios"]["terminal_to_demand"]
    synthetic_kuparuk_capacity = terminal_ratio * kuparuk_demand
    close(
        physical_terminal_capacity + synthetic_kuparuk_capacity,
        terminal_ratio * total_demand,
        "terminal construction capacity",
        tolerance=0.01,
    )

    components = connected_component_sizes(arcs)
    assert components == EXPECTED["component_sizes"], components

    unused = sorted(eligible_terminal_ids - physical_selected)
    print("Representative network validation passed")
    print(f"  suppliers: {len(selected_suppliers)}")
    print(f"  selected terminals: {len(selected_terminals)} "
          f"({len(physical_selected)} physical + 1 synthetic)")
    print(f"  demand nodes: {len(selected_customers)}")
    print(f"  arcs: {len(arcs)} ({len(upstream)} upstream + {len(downstream)} downstream)")
    print(f"  total demand proxy: {total_demand:,.6f} barrels")
    print(f"  connected-component sizes: {components}")
    print(f"  eligible physical terminals unused in selected topology: {unused}")


if __name__ == "__main__":
    main()
