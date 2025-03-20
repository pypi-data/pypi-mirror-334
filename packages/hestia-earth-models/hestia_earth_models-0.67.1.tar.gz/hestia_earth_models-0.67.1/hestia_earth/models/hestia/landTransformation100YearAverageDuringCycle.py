"""
Creates an [emissionsResourceUse](https://hestia.earth/schema/Emission) for every landCover land transformation.
contained within the [ImpactAssesment.cycle](https://hestia.earth/schema/ImpactAssessment#cycle), averaged over the last
100 years.

It does this by multiplying the land occupation during the cycle by the
[Site](https://hestia.earth/schema/Site) area 100 years ago and dividing by 100.

Land transformation from [land type] 100 years =
(Land occupation, during Cycle * Site Percentage Area 100 years ago [land type] / 100) / 100
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
TERM_ID = 'landTransformation100YearAverageDuringCycle'
_HISTORIC_DATE_OFFSET = 100


def run(impact_assessment: dict):
    return run_resource_use(
        impact_assessment=impact_assessment,
        historic_date_offset=_HISTORIC_DATE_OFFSET,
        term_id=TERM_ID
    )
