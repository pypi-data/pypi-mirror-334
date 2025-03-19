'''Generate sample snails with genomes and locations.'''

from argparse import Namespace
import json
import math
import numpy as np
from pathlib import Path
import polars as pl
import random
from geopy.distance import lonlat, distance
import sys

from .params import SampleParams, load_params


LON_LAT_PRECISION = 5
READING_PRECISION = 1
SIZE_PRECISION = 1


def samples(options: Namespace) -> None:
    '''Main driver for snailz snail creation.

    -   options.genomes: genomes data file.
    -   options.grids: grids parameter file.
    -   options.params: path to parameter file (see params.SampleParams for fields).
    -   options.outfile: optional path to saved output file.
    -   options.surveys: survey CSV parameter file.
    -   options.sites: sites CSV parameter file.

    Generated data is written as CSV to the specified output file.

    Args:
        options: see above.
    '''
    assert options.params != options.outfile, 'Cannot use same filename for options and parameters'
    options.params = load_params(SampleParams, options.params)
    options.surveys = pl.read_csv(options.surveys)
    options.sites = pl.read_csv(options.sites)
    random.seed(options.params.seed)

    genomes = json.loads(Path(options.genomes).read_text())
    grids = _load_grids(options)

    samples = _generate_samples(options, genomes, grids)
    _save(options, samples)


def _generate_samples(options: Namespace, genomes: dict, grids: dict) -> pl.DataFrame:
    '''Generate snail samples.

    For each previously-generated genome:

    1.  Select a survey and a random point in that survey's area, and determine if that point is contaminated.
    2.  Determine the range of possible snail sizes based on genotype and contamination.
    3.  Generate a size.
    4.  Append a record to a list that is later converted to a dataframe.

    Args:
        options: see samples().
        genomes: JSON representation of previously-generated genomes.
        grids: key-to-grid dictionary whose grids are NumPy arrays.

    Returns:
        Dataframe with sample ID, survey ID, longitude, latitude, sequence, and snail size.
    '''

    # Generate.
    samples = []
    for i, seq in enumerate(genomes['individuals']):
        survey_id, point, contaminated = _random_geo(options.sites, options.surveys, grids)
        limit = _size_limit(options, genomes, seq, contaminated)
        size = random.uniform(
            options.params.min_snail_size,
            options.params.min_snail_size + options.params.max_snail_size * limit
        )
        samples.append((i + 1, survey_id, point.longitude, point.latitude, seq, size))

    # Convert to dataframe.
    df = pl.DataFrame(samples, schema=('sample_id', 'survey_id', 'lon', 'lat', 'sequence', 'size'), orient='row')
    return df.with_columns(
        lon=df['lon'].round(LON_LAT_PRECISION),
        lat=df['lat'].round(LON_LAT_PRECISION),
        size=df['size'].round(SIZE_PRECISION),
    )


def _load_grids(options: Namespace) -> dict:
    '''Load all grid files.

    Args:
        options: see samples().

    Returns:
        Key-to-NumPy array map of contamination grids.
    '''
    return {
        s: np.loadtxt(Path(options.grids, f'{s}.csv'), dtype=int, delimiter=',')
        for s in set(options.surveys['site_id'])
    }


def _random_geo(sites: pl.DataFrame, surveys: pl.DataFrame, grids: dict) -> tuple:
    '''Select random point from a randomly-selected sample grid.

    1.  Select site.
    2.  Select random grid cell.
    3.  Determine whether that cell is contaminated.
    4.  Use site center point and survey spacing to determine longitude and latitude of cell.

    Args:
        sites: dataframe of site data.
        surveys: dataframe of surveys.
        grids: key-to-grid dictionary whose grids are NumPy arrays.

    Returns:
        Selected survey ID, (lon, lat) point, and whether point is contaminated
    '''
    # Get parameters.
    survey_row = random.randrange(surveys.shape[0])
    survey_id = surveys.item(survey_row, 'survey_id')
    spacing = float(surveys.item(survey_row, 'spacing'))
    site_id = surveys.item(survey_row, 'site_id')
    site_row = sites['site_id'].to_list().index(site_id)

    # Get grid information.
    grid = grids[site_id]
    width, height = grid.shape
    rand_x, rand_y = random.randrange(width), random.randrange(height)
    contaminated = bool(grid[rand_x, rand_x] != 0)

    # Generate point.
    site_lon = sites.item(site_row, 'lon')
    site_lat = sites.item(site_row, 'lat')
    corner = lonlat(site_lon, site_lat)
    rand_x *= spacing
    rand_y *= spacing
    dist = math.sqrt(rand_x**2 + rand_y**2)
    bearing = math.degrees(math.atan2(rand_y, rand_x))
    point = distance(meters=dist).destination(corner, bearing=bearing)

    return survey_id, point, contaminated


def _save(options: Namespace, samples: pl.DataFrame) -> None:
    '''Save results to file or show on standard output.

    Args:
        options: controlling options.
        samples: dataframe of generated samples.
    '''
    if options.outfile:
        samples.write_csv(Path(options.outfile))
    else:
        samples.write_csv(sys.stdout)


def _size_limit(options: Namespace, genomes: dict, seq: str, contaminated: bool) -> float:
    '''Calculate upper bound on snail size.

    If the genome has the significant mutation in the right location
      and the site is contaminated, the snail may have the mutant size.
      Otherwise, it has the normal size.

    Args:
        options: controlling options.
        genomes: JSON containing overall information about genomes.
        seq: specific sequence of this snail.
        contaminated: is sample location contaminated?

    Returns:
        Parameter value for upper bound on normal or mutant snail size.
    '''
    susc_loc = genomes['susceptible_loc']
    susc_base = genomes['susceptible_base']
    if contaminated and (seq[susc_loc] == susc_base):
        return options.params.mutant
    return options.params.normal
