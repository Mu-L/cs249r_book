from .types import GridProfile, RackProfile, Datacenter, CoolingProfile
from ..core.provenance import sourced
from ..core.registry import Registry
from ..core.types import Metadata
from ..core import provenance_catalog as pc

# --- Facility cooling tiers (PUE / WUE anchors for appendices) ---
PUE_LIQUID_COOLED = sourced(1.06, pc.UPTIME_PUE_2022, name="PUE (Liquid-Cooled)", description="Best-in-class liquid-cooled AI datacenter PUE.")
PUE_BEST_AIR = sourced(1.12, pc.UPTIME_PUE_2022, name="PUE (Best Air-Cooled)", description="Best-in-class air-cooled hyperscale datacenter PUE.")
PUE_TYPICAL = sourced(1.40, pc.UPTIME_PUE_2022, name="PUE (Industry Average)", description="Industry average traditional datacenter PUE.")
PUE_LEGACY = sourced(1.58, pc.UPTIME_PUE_2022, name="PUE (Legacy Air-Cooled)", description="Older enterprise datacenter PUE tier.")
PUE_STATE_OF_ART = sourced(1.10, pc.UPTIME_PUE_2022, name="PUE (state of art)", description="Highly optimized modern datacenter PUE benchmark.")
WUE_AIR_COOLED = sourced(0.5, pc.BOOK_WUE_ANCHORS, name="WUE (air-cooled)", description="Water usage effectiveness for air-cooled facilities.")
WUE_EVAPORATIVE = sourced(1.8, pc.BOOK_WUE_ANCHORS, name="WUE (evaporative)", description="Water usage effectiveness for evaporative cooling.")
WUE_LIQUID = sourced(0.0, pc.BOOK_WUE_ANCHORS, name="WUE (liquid-cooled)", description="Closed-loop liquid cooling (near-zero WUE).")

RACK_POWER_TRADITIONAL_KW = sourced(12, pc.BOOK_RACK_POWER, name="Rack power (traditional)", description="Traditional enterprise rack power (kW).")
RACK_POWER_AI_TYPICAL_KW = sourced(70, pc.BOOK_RACK_POWER, name="Rack power (AI typical)", description="Typical AI cluster rack power (kW).")
RACK_POWER_AI_HIGH_KW = sourced(100, pc.BOOK_RACK_POWER, name="Rack power (AI high)", description="High-density AI rack power (kW).")
AIR_COOLING_LIMIT_KW = sourced(30, pc.BOOK_RACK_POWER, name="Air cooling limit (kW)", description="Approximate rack power where air cooling becomes impractical.")


class FacilityCooling(Registry):
    """Datacenter cooling efficiency tiers (not regional grids)."""
    LiquidCooled = CoolingProfile(name="Liquid-Cooled", pue=PUE_LIQUID_COOLED, wue=WUE_LIQUID, metadata=Metadata(provenance=pc.UPTIME_PUE_2022))
    BestAir = CoolingProfile(name="Best Air-Cooled", pue=PUE_BEST_AIR, wue=WUE_EVAPORATIVE, metadata=Metadata(provenance=pc.UPTIME_PUE_2022))
    Typical = CoolingProfile(name="Industry Average", pue=PUE_TYPICAL, wue=WUE_EVAPORATIVE, metadata=Metadata(provenance=pc.UPTIME_PUE_2022))
    Legacy = CoolingProfile(name="Legacy Air-Cooled", pue=PUE_LEGACY, wue=WUE_EVAPORATIVE, metadata=Metadata(provenance=pc.UPTIME_PUE_2022))
    StateOfArt = CoolingProfile(name="State of Art", pue=PUE_STATE_OF_ART, wue=WUE_EVAPORATIVE, metadata=Metadata(provenance=pc.UPTIME_PUE_2022))


class Grids(Registry):
    """Regional grid carbon intensity (gCO2/kWh) with typical facility PUE/WUE."""
    Quebec = GridProfile(
        name="Quebec (Hydro)",
        carbon_intensity_g_kwh=sourced(20, pc.IEA_WEO_2023, name="Carbon Intensity (Quebec)", description="Quebec grid carbon intensity in gCO2/kWh."),
        pue=PUE_LIQUID_COOLED,
        wue=WUE_LIQUID,
        primary_source="hydro",
        lat=52.9399,
        lon=-73.5491,
        renewable_pct=99.0,
        metadata=Metadata(provenance=pc.HYDRO_QUEBEC_GRID),
    )
    Norway = GridProfile(
        name="Norway (Hydro)",
        carbon_intensity_g_kwh=sourced(10, pc.IEA_WEO_2023, name="Carbon Intensity (Norway)", description="Norway grid carbon intensity in gCO2/kWh."),
        pue=PUE_LIQUID_COOLED,
        wue=WUE_LIQUID,
        primary_source="hydro",
        lat=60.472,
        lon=8.4689,
        renewable_pct=98.0,
        metadata=Metadata(provenance=pc.IEA_WEO_2023),
    )
    US_Avg = GridProfile(
        name="US Average",
        carbon_intensity_g_kwh=sourced(429, pc.IEA_WEO_2023, name="Carbon Intensity (US Average)", description="US national average grid carbon intensity in gCO2/kWh."),
        pue=PUE_BEST_AIR,
        wue=WUE_EVAPORATIVE,
        primary_source="mixed",
        lat=39.8283,
        lon=-98.5795,
        renewable_pct=21.0,
        metadata=Metadata(provenance=pc.IEA_WEO_2023),
    )
    EU_Avg = GridProfile(
        name="EU Average",
        carbon_intensity_g_kwh=sourced(270, pc.IEA_WEO_2023, name="Carbon Intensity (EU Average)", description="EU average grid carbon intensity in gCO2/kWh."),
        pue=PUE_BEST_AIR,
        wue=WUE_EVAPORATIVE,
        primary_source="mixed",
        metadata=Metadata(provenance=pc.IEA_WEO_2023),
    )
    France = GridProfile(
        name="France (Nuclear)",
        carbon_intensity_g_kwh=sourced(50, pc.IEA_WEO_2023, name="Carbon Intensity (France)", description="France grid carbon intensity in gCO2/kWh."),
        pue=PUE_BEST_AIR,
        wue=WUE_EVAPORATIVE,
        primary_source="nuclear",
        metadata=Metadata(provenance=pc.IEA_WEO_2023),
    )
    Iowa = GridProfile(
        name="Iowa (Coal/Gas Reference)",
        carbon_intensity_g_kwh=sourced(680, pc.BOOK_ILLUSTRATIVE_IOWA_CARBON, name="Carbon Intensity (Iowa reference)", description="High-carbon US grid mix for tutorial contrast."),
        pue=PUE_BEST_AIR,
        wue=WUE_EVAPORATIVE,
        primary_source="coal_gas",
        lat=42.0329,
        lon=-93.5815,
        renewable_pct=12.0,
        metadata=Metadata(provenance=pc.BOOK_ILLUSTRATIVE_IOWA_CARBON),
    )
    Poland = GridProfile(
        name="Poland (Coal)",
        carbon_intensity_g_kwh=sourced(820, pc.IEA_WEO_2023, name="Carbon Intensity (Poland)", description="Poland grid carbon intensity in gCO2/kWh."),
        pue=PUE_LEGACY,
        wue=WUE_EVAPORATIVE,
        primary_source="coal",
        lat=51.9194,
        lon=19.1451,
        renewable_pct=17.0,
        metadata=Metadata(provenance=pc.IEA_WEO_2023),
    )
    Iceland = GridProfile(
        name="Iceland (Geothermal)",
        carbon_intensity_g_kwh=sourced(28, pc.IEA_WEO_2023, name="Carbon Intensity (Iceland)", description="Iceland grid carbon intensity in gCO2/kWh."),
        pue=PUE_LIQUID_COOLED,
        wue=WUE_LIQUID,
        primary_source="geothermal",
        lat=64.9631,
        lon=-19.0208,
        renewable_pct=100.0,
        metadata=Metadata(provenance=pc.IEA_WEO_2023),
    )
    Texas = GridProfile(
        name="Texas (ERCOT)",
        carbon_intensity_g_kwh=sourced(400, pc.IEA_WEO_2023, name="Carbon Intensity (Texas)", description="Texas grid carbon intensity in gCO2/kWh (EPA eGRID South Central)."),
        pue=PUE_BEST_AIR,
        wue=WUE_EVAPORATIVE,
        primary_source="mixed",
        lat=31.9686,
        lon=-99.9018,
        renewable_pct=28.0,
        metadata=Metadata(provenance=pc.IEA_WEO_2023),
    )
    Germany = GridProfile(
        name="Germany (Coal+Wind)",
        carbon_intensity_g_kwh=sourced(385, pc.IEA_WEO_2023, name="Carbon Intensity (Germany)", description="Germany grid carbon intensity in gCO2/kWh."),
        pue=PUE_BEST_AIR,
        wue=WUE_EVAPORATIVE,
        primary_source="mixed",
        lat=51.1657,
        lon=10.4515,
        renewable_pct=46.0,
        metadata=Metadata(provenance=pc.IEA_WEO_2023),
    )
    China_Avg = GridProfile(
        name="China Average",
        carbon_intensity_g_kwh=sourced(555, pc.IEA_WEO_2023, name="Carbon Intensity (China Average)", description="China national average grid carbon intensity in gCO2/kWh."),
        pue=PUE_TYPICAL,
        wue=WUE_EVAPORATIVE,
        primary_source="coal",
        lat=35.8617,
        lon=104.1954,
        renewable_pct=30.0,
        metadata=Metadata(provenance=pc.IEA_WEO_2023),
    )
    India_Avg = GridProfile(
        name="India Average",
        carbon_intensity_g_kwh=sourced(720, pc.IEA_WEO_2023, name="Carbon Intensity (India Average)", description="India national average grid carbon intensity in gCO2/kWh."),
        pue=PUE_LEGACY,
        wue=WUE_EVAPORATIVE,
        primary_source="coal",
        lat=20.5937,
        lon=78.9629,
        renewable_pct=22.0,
        metadata=Metadata(provenance=pc.IEA_WEO_2023),
    )


class Datacenters(Registry):
    """Registry namespace for Datacenters."""
    Quebec_Hydro = Datacenter(name="Quebec Hydro Campus", grid=Grids.Quebec)
    Norway_Hydro = Datacenter(name="Norway Hydro Campus", grid=Grids.Norway)
    US_Hyperscale = Datacenter(name="US Hyperscale Region", grid=Grids.US_Avg)
    EU_Average = Datacenter(name="EU Average Region", grid=Grids.EU_Avg)
    France_Nuclear = Datacenter(name="France Nuclear Region", grid=Grids.France)
    Iowa_Reference = Datacenter(name="Iowa Reference Site", grid=Grids.Iowa)
    Poland_Coal = Datacenter(name="Poland Coal Region", grid=Grids.Poland)


class Racks(Registry):
    """Registry namespace for Racks."""
    Traditional = RackProfile(
        name="Traditional Enterprise",
        power_kw=RACK_POWER_TRADITIONAL_KW,
        cooling_type="air",
        metadata=Metadata(provenance=pc.BOOK_RACK_POWER),
    )
    AI_Standard = RackProfile(
        name="AI Cluster (Standard)",
        power_kw=RACK_POWER_AI_TYPICAL_KW,
        cooling_type="liquid",
        metadata=Metadata(provenance=pc.BOOK_RACK_POWER),
    )
    AI_High = RackProfile(
        name="AI Cluster (High Density)",
        power_kw=RACK_POWER_AI_HIGH_KW,
        cooling_type="liquid",
        metadata=Metadata(provenance=pc.BOOK_RACK_POWER),
    )


from .pricing import Pricing
from .capacity import Capacity


class Infrastructure(Registry):
    """Registry namespace for Infrastructure."""
    Grids = Grids
    Datacenters = Datacenters
    Racks = Racks
    FacilityCooling = FacilityCooling
    Pricing = Pricing
    Capacity = Capacity
    AIR_COOLING_LIMIT_KW = AIR_COOLING_LIMIT_KW
