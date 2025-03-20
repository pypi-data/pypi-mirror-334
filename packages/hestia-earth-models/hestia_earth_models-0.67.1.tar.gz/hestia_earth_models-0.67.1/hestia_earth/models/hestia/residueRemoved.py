"""
This model will gap-fill the value for `residueRemoved` when the only provided data is the incorporated residue.
We are assuming that anything that was not incorporated must have been removed.
"""
from hestia_earth.schema import TermTermType
from hestia_earth.utils.model import filter_list_term_type
from hestia_earth.utils.tools import list_sum

from hestia_earth.models.log import logRequirements, logShouldRun, log_as_table
from hestia_earth.models.utils.completeness import _is_term_type_incomplete
from hestia_earth.models.utils.practice import _new_practice
from hestia_earth.models.utils import is_from_model
from . import MODEL

REQUIREMENTS = {
    "Cycle": {
        "completeness.cropResidue": "False",
        "practices": [{
            "@type": "Practice",
            "term.@id": [
                "residueIncorporated",
                "residueIncorporatedLessThan30DaysBeforeCultivation",
                "residueIncorporatedMoreThan30DaysBeforeCultivation"
            ]
        }],
        "none": {
            "practices": [{
                "@type": "Practice",
                "term.@id": [
                    "residueRemoved",
                    "residueBurnt",
                    "residueLeftOnField"
                ]
            }]
        }
    }
}
RETURNS = {
    "Practice": [{
        "value": ""
    }]
}
TERM_ID = 'residueRemoved'


def _practice(value: float):
    practice = _new_practice(TERM_ID, MODEL)
    practice['value'] = [value]
    return practice


def _should_run(cycle: dict):
    crop_residue_incomplete = _is_term_type_incomplete(cycle, TermTermType.CROPRESIDUE)

    practices = filter_list_term_type(cycle.get('practices', []), TermTermType.CROPRESIDUEMANAGEMENT)
    incorporated_practices = [
        {'id': p.get('term', {}).get('@id'), 'value': list_sum(p.get('value'), None)}
        for p in practices
        if p.get('term', {}).get('@id').startswith('residueIncorporated') and not is_from_model(p)
    ]
    has_other_practices = any([
        not p.get('term', {}).get('@id').startswith('residueIncorporated')
        for p in practices
    ])
    incorporated_value = list_sum([p.get('value') for p in incorporated_practices], None)

    logRequirements(cycle, model=MODEL, term=TERM_ID,
                    term_type_cropResidue_incomplete=crop_residue_incomplete,
                    incorporated_practices=log_as_table(incorporated_practices),
                    incorporated_value=incorporated_value,
                    has_other_practices=has_other_practices)

    should_run = all([crop_residue_incomplete, incorporated_value, not has_other_practices])
    logShouldRun(cycle, MODEL, TERM_ID, should_run)
    return should_run, 100 - (incorporated_value or 0)


def run(cycle: dict):
    should_run, value = _should_run(cycle)
    return [_practice(value)] if should_run else []
