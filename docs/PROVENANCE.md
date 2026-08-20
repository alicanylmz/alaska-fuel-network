# Provenance and transformation record

## Scope

This repository ends with construction of the representative Alaska
refined-fuel network. It distinguishes public-source fields, deterministic
transformations, modeling assumptions, and arcs selected by the
network-construction model.

| Network element | Principal public sources | Released table |
|---|---|---|
| Refineries | EIA-820 Refinery Capacity Report; ADEC and operator records | `refineries.csv` |
| Marine import hubs | USACE Navigation Facilities and 2023 Waterborne Commerce Statistics | `marine_import_hubs.csv` |
| Distribution terminals | Former DHS HIFLD Petroleum Terminals layer; ADEC and operator checks | `distribution_terminals.csv` |
| Last-mile locations | ADEC UST, EPA UST Finder, OpenStreetMap, and Alaska Bulk Fuel Inventory | `last_mile_locations.csv` |
| Constructed arcs | Processed node tables and documented domain rules | `network_arcs.csv` |

Source URLs, retrieval dates, and checksums are recorded in the corresponding
`data/raw/*/SOURCE.md` files. Rule-level evidence is recorded in
`docs/DOMAIN_RULE_EVIDENCE.md`.

## Refineries and marine import hubs

The refinery table uses atmospheric crude-distillation capacity from the EIA
Refinery Capacity Report dated January 1, 2026. Annual refinery weights equal
$365\times\mathrm{ACDU}_{i}$. Company identity and ADEC permits distinguish the
ConocoPhillips Kuparuk and Hilcorp Prudhoe Bay topping facilities, which share
the EIA site label `PRUDHOE BAY`.

Marine import hubs are matched to USACE navigation facilities and 2023
Waterborne Commerce Statistics. Inbound commodity codes 2211, 2221, 2330, and
2340 represent gasoline, kerosene, distillate fuel oil, and residual fuel oil.
External supply includes overseas and Canadian imports but excludes coastwise
receipts, which can include movements from Alaska refineries. Foreign short
tons are converted at 6.7 barrels per short ton as an aggregate mixed-product
factor.

The refinery and marine-import weights are normalized so total supplier
capacity equals 110% of aggregate last-mile demand proxy.

## Distribution terminals

The terminal source is the preserved 73-row Alaska extract of the former HIFLD
Petroleum Terminals layer. HIFLD Open was discontinued in August 2025; the
archived snapshot is therefore the reproduction source.

Eligible terminals are in service, have valid coordinates and positive
capacity, are not crude-system facilities, and show refined-product handling in
their commodity or product fields. Red Dog is excluded as a specialized mine
port. Kenai terminal `ANLTK02042` and Petro Star Valdez terminal `ANLTK02070`
use documented refined-product storage values instead of broader mixed-product
capacity values.

Physical and representative terminal capacities are normalized to 150% of
aggregate last-mile demand proxy. Local terminals are paired with local demand,
and selected western and Yukon River terminals receive documented service-area
limits. Remaining capacity is allocated in proportion to the refined-product
storage weight.

## Last-mile locations

ADEC, EPA UST Finder, and OpenStreetMap facility records were clustered through
25 m connected components. Gallons are converted to barrels using 42 gallons
per barrel. For overlapping ADEC and EPA product records, the larger source
total is retained to avoid double counting likely duplicate tanks.

Missing capacities use five-nearest-neighbor inverse-distance weighting,
clipped to the observed 10th--90th percentile. Four imputed OSM locations more
than 300 km from an observed facility were removed. Adak uses the Alaska Bulk
Fuel Inventory; St. Paul and St. George use an Adak gallons-per-resident analog;
and the Kuparuk and Prudhoe Bay/Deadhorse industrial nodes are documented
scenario values.

The preserved contemporary public exports establish traceability. The
versioned processed table is the reproduction input because the exact
historical snapshots used in the initial integration are unavailable.

## Network construction

All candidate supplier-to-terminal and terminal-to-last-mile pairs receive
WGS84 ellipsoidal distance costs. A continuous minimum-cost flow model enforces
supplier balance, terminal capacity and flow conservation, complete last-mile
demand satisfaction, and the rules in `config/domain_rules.json`. Arcs carrying
more than $10^{-6}$ barrels are retained.

The resulting representative network contains 16 suppliers, 52 distribution
terminals, 931 last-mile locations, and 1,022 arcs. The selected arc set is not
observed and can be sensitive to capacity calibration, distance proxies, solver
tolerances, and alternative optimal flows.
