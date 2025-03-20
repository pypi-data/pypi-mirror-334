from hestia_earth.schema import TermTermType

from hestia_earth.models.utils.term import get_lookup_value
from . import MODEL

IPCC_LAND_USE_CATEGORY_ANNUAL = "Annual crops"
IPCC_LAND_USE_CATEGORY_PERENNIAL = "Perennial crops"
TOTAL_CROPLAND = "Cropland"
ANNUAL_CROPLAND = "Arable land"
FOREST_LAND = "Forest land"
OTHER_LAND = "Other land"
PERMANENT_CROPLAND = "Permanent crops"
PERMANENT_PASTURE = "Permanent meadows and pastures"
TOTAL_AGRICULTURAL_CHANGE = "Total agricultural change"
ALL_LAND_USE_TERMS = [
    FOREST_LAND,
    TOTAL_CROPLAND,
    ANNUAL_CROPLAND,
    PERMANENT_CROPLAND,
    PERMANENT_PASTURE,
    OTHER_LAND
]

# Mapping from Land use terms to Management node terms.
# land use term: (@id, name)
LAND_USE_TERMS_FOR_TRANSFORMATION = {
    FOREST_LAND: ("forest", "Forest"),
    ANNUAL_CROPLAND: ("annualCropland", "Annual cropland"),
    PERMANENT_CROPLAND: ("permanentCropland", "Permanent cropland"),
    PERMANENT_PASTURE: ("permanentPasture", "Permanent pasture"),
    OTHER_LAND: ("otherLand", OTHER_LAND)  # Not used yet
}


def crop_ipcc_land_use_category(
    crop_term_id: str,
    lookup_term_type: str = TermTermType.LANDCOVER.value
) -> str:
    """
    Looks up the crop in the lookup.
    Returns the IPCC_LAND_USE_CATEGORY.
    """
    return get_lookup_value(
        lookup_term={"@id": crop_term_id, "type": "Term", "termType": lookup_term_type},
        column='IPCC_LAND_USE_CATEGORY',
        model=MODEL
    )
