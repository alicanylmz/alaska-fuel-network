# Last-mile public source exports

This folder preserves contemporary public exports from the three main
facility sources used to support the processed last-mile demand-proxy table.
These snapshots provide public-source traceability.

## Alaska ADEC underground storage tanks

- Publisher: Alaska Department of Environmental Conservation
- Dataset: Underground Storage Tank Database Search/export
- URL: https://dec.alaska.gov/Applications/SPAR/PublicUST/USTSearch/
- Retrieval date: 2026-08-20
- Preserved file: `AllFacilitiesTanksOwners_2026-08-20.xls`
- SHA-256: `696b3e7708119005972a52f40570a303ffb226a5a1a0e2803e5effb6319a8ca9`

The export contains facility, tank, owner, coordinate, capacity, substance,
status, and regulatory fields.

## EPA UST Finder

- Publisher: U.S. Environmental Protection Agency
- Dataset/application: UST Finder
- Application URL: https://experience.arcgis.com/experience/d3a227fc71c04f90bfdce2ca84f79620
- Retrieval date: 2026-08-20
- Facilities file: `EPA_UST_Finder_facilities_2026-08-20.csv`
- Facility rows: 2,648
- Facilities SHA-256: `5db4965b35f0d4a28ebc651c27de9734d870f362fbe21c7c2e9314ee722ac289`
- Tanks file: `EPA_UST_Finder_tanks_2026-08-20.csv`
- Tank rows: 6,870
- Tanks SHA-256: `882d74be5b1f43a0d1aa9245b9ae070af8010c9ea104a6290d844cc82c493323`

The facility and tank layers join through facility identifier
(`Facility ID` in the facility export and `Facility_ID` in the tank export).

## OpenStreetMap fuel facilities

- Publisher/contributors: OpenStreetMap contributors
- Extraction tool: Overpass Turbo
- Overpass Turbo URL: https://overpass-turbo.eu/
- Snapshot timestamp recorded in the GeoJSON: 2026-08-20T19:46:13Z
- Preserved file: `OSM_Alaska_fuel_facilities_2026-08-20.geojson`
- Features: 322
- SHA-256: `acde229a94c4878ed2bb6e462f2b3d1431de19b8731688d9ed5e538553704097`
- License: Open Data Commons Open Database License (ODbL)
- Attribution: © OpenStreetMap contributors

The extraction selected Alaska objects tagged `amenity=fuel` or `shop=fuel`
and exported nodes plus the center points of qualifying ways and relations.
The corresponding Overpass query is:

```overpass
[out:json][timeout:180];
area["ISO3166-2"="US-AK"][admin_level=4]->.searchArea;
(
  nwr["amenity"="fuel"](area.searchArea);
  nwr["shop"="fuel"](area.searchArea);
);
out center tags;
```

OpenStreetMap is a continuously edited database. The timestamped GeoJSON—not a
future re-run of the query—is the source snapshot preserved for this release.

