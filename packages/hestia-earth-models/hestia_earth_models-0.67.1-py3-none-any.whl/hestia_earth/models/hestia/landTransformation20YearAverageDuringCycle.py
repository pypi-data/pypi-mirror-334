"""
Creates an [emissionsResourceUse](https://hestia.earth/schema/Emission) for every landCover land transformation.
contained within the [ImpactAssesment.cycle](https://hestia.earth/schema/ImpactAssessment#cycle), averaged over the last
20 years.

It does this by multiplying the land occupation during the cycle by the
[Site](https://hestia.earth/schema/Site) area 20 years ago and dividing by 20.

Land transformation from [land type] 20 years =
(Land occupation, during Cycle * Site Percentage Area 20 years ago [land type] / 100) / 20
"""
from .resourceUse_utils import run_resource_use

REQUIREMENTS = {
    "ImpactAssessment": {
        "Site": {
            "management": [{"@type": "Management", "value": ">=0", "term.termType": "landCover", "endDate": ""}]
        },
        "emissionsResourceUse": [
            {
                "@type": "Indicator",
                "term.@id": "landOccupationDuringCycle",
                "landCover": {
                    "@type": "Term",
                    "termType": "landCover"
                },
                "value": ">=0"
            }
        ],
        "endDate": ""
    }
}
RETURNS = {
    "Indicator": [{
        "value": "",
        "landCover": "",
        "previousLandCover": ""
    }]
}
TERM_ID = 'landTransformation20YearAverageDuringCycle'
_HISTORIC_DATE_OFFSET = 20


def run(impact_assessment: dict):
    return run_resource_use(
        impact_assessment=impact_assessment,
        historic_date_offset=_HISTORIC_DATE_OFFSET,
        term_id=TERM_ID
    )
