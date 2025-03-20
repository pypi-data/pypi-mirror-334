"""
Pre Checks Cache Sources

This model caches the sources of all Cycle models.
"""
from hestia_earth.models.utils.cache_sources import cache_sources

REQUIREMENTS = {
    "Cycle": {}
}
RETURNS = {
    "Cycle": {}
}


def run(cycle: dict): return cache_sources(cycle)
