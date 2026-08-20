# Data dictionary

## `refineries.csv`

- `refinery_id`: stable research identifier.
- `acdu_operating_bpcd`, `acdu_operating_bpsd`: EIA atmospheric
  crude-distillation capacity.
- `model_capacity`: normalized supplier capacity used in network construction.
- Operator, coordinate, and source fields retain facility-level provenance.

## `marine_import_hubs.csv`

- `hub_id`, `hub_name`: stable identifier and display name.
- `usace_nav_unit_*`, `usace_waterway_*`: USACE facility and waterway matches.
- `overseas_import_short_tons`, `canadian_import_short_tons`: external receipt
  components.
- `foreign_*_short_tons`: inbound refined-fuel quantities by commodity.
- `coastwise_receipts_short_tons`: domestic receipts retained for accounting
  but excluded from external supply.
- `external_import_supply_short_tons_2023`: external-supply allocation weight.
- `model_capacity`: normalized supplier capacity used in network construction.

## `distribution_terminals.csv`

- `TERM_ID`, `NAME`: HIFLD terminal identifier and name.
- `CAPACITY`: raw reported storage capacity in barrels.
- `refined_capacity_weight_barrels`: refined-product allocation weight; zero
  indicates an ineligible terminal.
- `model_capacity`: normalized terminal capacity after local and regional rules.

## `last_mile_locations.csv`

- `cluster_id`, `Name`: stable clustered-location identifier and name.
- `capacity_gallons_total`: observed, imputed, or analog storage volume.
- `model_capacity`: demand proxy in barrels.
- `capacity_value_status`, `capacity_estimation_method`,
  `capacity_source_reference`, `nearest_observed_distance_km`: audit fields.

## `network_arcs.csv`

- `arc_stage`: `R-D`, `P-D`, or `D-L`, where `D` denotes distribution
  terminals and `L` denotes last-mile locations.
- `flow_barrels`: flow in the network-construction solution, not observed
  shipment volume.
- `distance_km`: WGS84 ellipsoidal origin-destination distance.
- `unit_cost`: distance-based construction coefficient.
- `arc_cost_barrel_km`: `flow_barrels * distance_km`.
- `geometry_wkt`: densified display line, not a physical route.

`supplier_to_terminal_arcs.csv` and `terminal_to_last_mile_arcs.csv` contain the
same records separated by network layer.
