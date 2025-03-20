from functools import reduce
from enum import Enum
from pydash.objects import merge
from hestia_earth.utils.api import download_hestia
from hestia_earth.utils.tools import flatten

from .log import logger
from .utils import CACHE_KEY, cached_value
from .utils.site import CACHE_YEARS_KEY
from .site.pre_checks.cache_geospatialDatabase import (
    list_vectors, list_rasters, cache_site_results, _should_run
)
from .geospatialDatabase.utils import (
    CACHE_VALUE as CACHE_GEOSPATIAL_KEY, CACHE_AREA_SIZE,
    has_boundary, has_coordinates,
    _run_query, _site_gadm_id
)


class ParamType(Enum):
    BOUNDARIES = 'boundaries'
    COORDINATES = 'coordinates'
    GADM_IDS = 'gadm-ids'


_VALUE_AS_PARAM = {
    ParamType.COORDINATES: lambda data: {'latitude': data[0].get('latitude'), 'longitude': data[0].get('longitude')},
    ParamType.BOUNDARIES: lambda data: data[0].get('boundary'),
    ParamType.GADM_IDS: lambda data: data[0].get('region', data[0].get('country', {})).get('@id')
}


def _cache_results(results: list, collections: list, index: int):
    start = index * len(collections)
    end = start + len(collections)
    return cache_site_results(results[start:end], collections)


def _run_values(sites: list, param_type: ParamType, rasters: list = [], vectors: list = [], years: list = None):
    param_values = list(map(_VALUE_AS_PARAM.get(param_type), sites))
    # unique list
    param_values = list(set(param_values)) if param_type == ParamType.GADM_IDS else list({
        str(v): v for v in param_values
    }.values())

    raster_results = _run_query({
        'ee_type': 'raster',
        'collections': rasters,
        param_type.value: param_values
    }) if rasters else []

    vector_results = _run_query({
        'ee_type': 'vector',
        'collections': vectors,
        param_type.value: param_values
    }) if vectors else []

    def _process_site(site_values: tuple):
        site, area_size = site_values

        # get real index in values to handle duplicates
        param_value = _VALUE_AS_PARAM.get(param_type)([site])
        index = param_values.index(param_value)

        cached_data = {
            **_cache_results(raster_results, rasters, index),
            **_cache_results(vector_results, vectors, index)
        } | ({CACHE_AREA_SIZE: area_size} if area_size is not None else {})
        cached_data = merge(cached_value(site, CACHE_GEOSPATIAL_KEY, {}), cached_data)
        site_cache = merge(
            site.get(CACHE_KEY, {}),
            {CACHE_GEOSPATIAL_KEY: cached_data},
            ({CACHE_YEARS_KEY: cached_value(site, CACHE_YEARS_KEY, []) + years} if years else {})
        )
        return merge(site, {CACHE_KEY: site_cache})

    return reduce(lambda prev, curr: prev + [_process_site(curr)], sites, [])


def _should_preload_region_area_size(site: dict): return not has_coordinates(site) and not has_boundary(site)


def _preload_regions_area_size(sites: dict):
    region_ids = set(map(_site_gadm_id, filter(_should_preload_region_area_size, sites)))
    return {term_id: download_hestia(term_id).get('area') for term_id in region_ids}


def _group_sites(sites: dict, check_has_cache: bool = True):
    # preload area size for all regions
    regions_area_size = _preload_regions_area_size(sites)

    def get_region_area_size(site: dict):
        return regions_area_size.get(_site_gadm_id(site)) if _should_preload_region_area_size(site) else None

    sites = [
        (n, ) + (_should_run(n, area_size=get_region_area_size(n), check_has_cache=check_has_cache)) for n in sites
    ]
    # restrict sites based on should_cache result
    sites = [(site, area_size) for site, should_cache, area_size in sites if should_cache]

    with_coordinates = [
        (site, area_size) for site, area_size in sites if has_coordinates(site)
    ]
    with_boundaries = [
        (site, area_size) for site, area_size in sites if not has_coordinates(site) and has_boundary(site)
    ]
    with_gadm_ids = [
        (site, area_size) for site, area_size in sites if not has_coordinates(site) and not has_boundary(site)
    ]

    return {
        ParamType.COORDINATES: with_coordinates,
        ParamType.BOUNDARIES: with_boundaries,
        ParamType.GADM_IDS: with_gadm_ids
    }


def _run(sites: list, years: list = [], years_only: bool = False):
    rasters = list_rasters(years=years, years_only=years_only)
    vectors = [] if years_only else list_vectors(sites)
    filtered_data = _group_sites(sites, not years_only)
    return flatten([
        _run_values(filtered_data.get(param_type), param_type, rasters, vectors, years)
        for param_type in [e for e in ParamType] if len(filtered_data.get(param_type)) > 0
    ])


def run(sites: list, years: list = None):
    """
    Run all queries at once for the list of provided Sites.
    Note: Earth Engine needs to be initiliased with `init_gee()` before running this function.

    Parameters
    ----------
    sites : list[dict]
        List of Site as dict.
    years : list[int]
        List of related years to fetch annual data.
    """
    sites = _run(sites)

    # avoid memory limit errors by running only a few years at a time
    unique_years = sorted(list(set(years)))
    batch_size = 5
    batches = range(0, len(unique_years), batch_size)

    for batch_index in batches:
        logger.info(f"Processing sites in batch {batch_index + 1} of {len(batches)}...")
        sub_years = unique_years[batch_index:batch_index + batch_size]
        sites = _run(sites, sub_years, years_only=True)

    return sites
