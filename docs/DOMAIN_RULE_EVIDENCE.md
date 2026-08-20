# Domain-rule evidence audit

This document identifies what each rule in `config/domain_rules.json` is based
on and, critically, whether the source states the rule directly or merely
  supports a manually selected modeling restriction.

## Evidence categories

- **Direct operational evidence**: the source expressly describes the relevant
  facility, movement, or service relationship.
- **Evidence-informed modeling restriction**: the source establishes the
  operating context, but the exclusivity or prohibited arc is a deliberate
  network-construction assumption.
- **Manually selected parameter**: the numerical value is not reported by a
  source.

## Rule-by-rule audit

### `LOCAL_KUPARUK`

- Classification: evidence-informed modeling restriction.
- Source context: ADEC identifies ConocoPhillips' Kuparuk Central Processing
  Facility 1, and EIA lists the ConocoPhillips Alaska refinery/topping capacity
  in the Prudhoe Bay area. The processed refinery table links the EIA filing to
  CPF-1 using operator identity and the ADEC facility record.
- ADEC facility record:
  https://dec.alaska.gov/Applications/SPAR/PublicMVC/CSP/SiteReport/267
- ADEC attachment previously cited in the configuration:
  https://dec.alaska.gov/Applications/Air/airtoolsweb/Home/ViewAttachment/16608649/YQlno6vJE2ZMsAuri7Zc0g2
- EIA Table 3: https://www.eia.gov/petroleum/refinerycapacity/table3.pdf


### `LOCAL_PRUDHOE`

- Classification: evidence-informed modeling restriction.
- Source context: EIA lists Hilcorp North Slope LLC refinery/topping capacity
  at Prudhoe Bay. The processed refinery table identifies ADEC Operating Permit
  `AQ0265TVP04`, “Crude Oil Topping Unit,” as the facility-level source.
- EIA Table 3: https://www.eia.gov/petroleum/refinerycapacity/table3.pdf
- ADEC permit attachment cited by the processed refinery table:
  https://dec.alaska.gov/Applications/Air/airtoolsweb/Home/ViewAttachment/17167453/TSiW3-CldfSS4X-635tr2g2
- ADEC attachment previously cited in the configuration:
  https://dec.alaska.gov/Applications/Air/airtoolsweb/Home/ViewAttachment/17167454/z86QqXiAhMckqqY3fZ4hxw2



### `LOCAL_ADAK`

- Classification: evidence-informed modeling restriction.
- Source: *Alaska Barge Landing System Design Study, Phase 2*, Section 6.3.1,
  “Adak,” printed pages 53-54.
- Report URL:
  https://dot.alaska.gov/stwddes/desbridge/assets/grant/southcoast/ak_COE_AlaskaBargeReport_2010_FINAL.pdf
- Supporting public inventory:
  https://maps.commerce.alaska.gov/server/rest/services/Services/CDO_Utilities/MapServer/48
- Exact support: the report describes Adak as an Aleutian island community
  1,300 miles southwest of Anchorage, with deep-water docks, fueling facilities,
  and extensive fuel tanks. The state inventory identifies the Adak community
  bulk-fuel facility used for the demand proxy.


### `LOCAL_ST_GEORGE`

- Classification: evidence-informed modeling restriction.
- Source: *Alaska Barge Landing System Design Study, Phase 2*, Section 6.3.13,
  “Saint George,” printed pages 66-67.
- Report URL:
  https://dot.alaska.gov/stwddes/desbridge/assets/grant/southcoast/ak_COE_AlaskaBargeReport_2010_FINAL.pdf
- Exact support: the report states that St. George is accessible only by air
  and sea, that most freight and supplies arrive by ship, and that fuel is
  delivered by barge through a fuel header at the City Dock.


### `LOCAL_ST_PAUL`

- Classification: evidence-informed modeling restriction.
- Source: *Alaska Barge Landing System Design Study, Phase 2*, Section 6.3.14,
  “Saint Paul,” printed pages 67-68.
- Report URL:
  https://dot.alaska.gov/stwddes/desbridge/assets/grant/southcoast/ak_COE_AlaskaBargeReport_2010_FINAL.pdf
- Exact support: the report places St. Paul 300 miles west of the Alaska
  mainland, describes sea and air access, states that most supplies and freight
  arrive by ship, and reports recurring fuel deliveries by barge.


### `EXCLUDE_RED_DOG_MINE_PORT`

- Classification: direct operational evidence with a modeling implication.
- Source: *Northwest Alaska Transportation Plan: Marine and Riverine
  Transportation: Conditions, Issues, and Trends*.
- Report URL:
  https://dot.alaska.gov/nreg/nwatp/files/nwatpMarineRiverineConditions.pdf
- Exact locations:
  - Section 1.2.1, “Fuel Delivery Methods,” printed page 4: Delta Western
    supports the Red Dog Mine development on a contract basis.
  - Section 1.4.3, “Red Dog Port Existing Conditions,” printed page 24: the port
    supports Red Dog Mine operations, exports zinc and lead ore, and imports
    mine equipment, fuel, and cargo.


### `NO_NORTH_POLE_TO_KOTZEBUE`

- Classification: evidence-informed modeling restriction; not a directly
  reported prohibition.
- Northwest Alaska report locations:
  - Section 1.2.1, “Fuel Delivery Methods,” printed page 4: Crowley and Vitus
    are described as the principal Northwest Alaska fuel suppliers; fuel is
    delivered through Nome/Kotzebue tank farms or offshore tanker-to-barge
    transfers.
  - Section 1.3.1, printed pages 13-15: Northwest delivery is described as a
    marine/lightering system centered on Nome, Kotzebue, and direct coastal or
    river delivery.
- Report URL:
  https://dot.alaska.gov/nreg/nwatp/files/nwatpMarineRiverineConditions.pdf
- Petro Star context: the current official locations page describes the North
  Pole refinery as an Interior facility and identifies Fairbanks/Interior
  distribution operations.
- Petro Star URL: https://petrostar.com/locations/


### `terminal_service_radius_km`

- Classification: manually-selected parameters.
- Parameters: Kotzebue 300 km; three Nome terminals 250 km; Fort Yukon 250 km;
  Galena 250 km.
- Contextual source: the Northwest Alaska report identifies Nome and Kotzebue
  as regional marine hubs and describes lightering to smaller coastal and river
  communities on printed pages 4 and 13-15. It describes Galena's fuel landing
  in Table 9 on printed page 46.
- Source limitation: the report does not provide 250 km or 300 km 
  radii, and it does not substantiate a 250 km Fort Yukon radius. Those values
  were chosen to prevent unrealistic long-distance geodesic assignments while
  retaining regional coverage. They should not be presented as reported facts.

### `VALDEZ_TO_ALEUTIANS`

- Classification: direct operational evidence for the regional relationship;
  minimal-flow implementation is a modeling device.
- Source: Petro Star's current official “Locations” page, entry “Valdez
  Petroleum Terminal.”
- URL: https://petrostar.com/locations/
- Exact support: Petro Star states that two barges frequent its 230,000-barrel
  Valdez terminal to transship ultra-low-sulfur diesel, gasoline, and jet fuel
  between the Valdez refinery, Anchorage, and the Aleutian Islands.



