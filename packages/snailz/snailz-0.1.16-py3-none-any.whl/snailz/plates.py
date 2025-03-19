'''Generate random assay plates.'''

from argparse import Namespace
import csv
import json
from pathlib import Path
import random
import sys

from .params import AssayParams, load_params


MODEL = 'Weyland-Yutani 470'
PLATE_HEIGHT = 4
PLATE_WIDTH = 4


def plates(options: Namespace) -> None:
    '''Main driver for snailz plate creation.

    Each plate is represented by two files: one with the design and one with the results.
      Plate generation re-uses assay parameters: see `assays.py` for details.
      Plates are saved in the specified output directory with auto-generated names.

    -   options.assays: path to assay parameter files.
    -   options.designs: output directory for plate design files.
    -   options.readings: output directory for plate reading files.

    Args:
        options: see above.
    '''
    options.params = load_params(AssayParams, options.params)
    random.seed(options.params.seed)
    for filename, sample_id, kind in _join_assay_data(options):
        _make_plate(
            options.params,
            sample_id,
            kind,
            Path(options.designs, filename),
            Path(options.readings, filename),
        )


def _generate(params: AssayParams, sample_locs: list, func: callable) -> list:
    '''Make body of plate design or results.

    -   Each result is represented as a rectangular list of lists.
    -   The first row of each result is lettered started with 'A' like a spreadsheet.
    -   Each subsequent row starts with a row number from '1' like a spreadsheet.

    Args:
        params: assay parameters.
        sample_locs: location of sample in each row of plate
        func: function used to generate interior table value

    Returns:
        Rectangular list-of-lists.
    '''
    title_row = ['', *[chr(ord('A') + col) for col in range(PLATE_WIDTH)]]
    values = [
        [func(params, col == sample_locs[row]) for col in range(PLATE_WIDTH)]
        for row in range(PLATE_HEIGHT)
    ]
    labeled = [[str(i + 1), *r] for (i, r) in enumerate(values)]
    return [title_row, *labeled]


def _join_assay_data(options: Namespace) -> callable:
    '''Get experiment type and plate filename from data.

    Args:
        options: see above.

    Returns:
        Generator that produces tuples of plate filename, plate, and experiment.
    '''
    assays = json.load(open(options.assays, 'r'))
    experiments = {x['sample_id']: x['kind'] for x in assays['experiment']}
    plates = {p['filename']: p['sample_id'] for p in assays['plate']}
    return ((f, plates[f], experiments[plates[f]]) for f in plates)


def _make_head(kind: str, sample_id: int) -> list:
    '''Make head of plate.

    Args:
        kind: kind of experiment ('calibration' or other).
        sample_id: which sample this experiment is for.

    Returns:
        List-of-lists representation of head of plate.
    '''
    return [
        [MODEL, kind, sample_id],
        [],
    ]


def _make_placement(kind: str) -> tuple:
    '''Generate random arrangement of sample locations in plate.

    Args:
        kind: kind of experiment ('calibration' or other).

    Returns:
        Tuple of sample placements and column orders.
    '''
    placement = [[False for col in range(PLATE_WIDTH)] for row in range(PLATE_HEIGHT)]
    if kind == 'calibration':
        return placement, []
    columns = list(c for c in range(PLATE_WIDTH))
    random.shuffle(columns)
    columns = columns[:PLATE_HEIGHT]
    for r, row in enumerate(placement):
        row[columns[r]] = True
    return placement, columns


def _make_plate(params: AssayParams, sample_id: str, kind: str, design_file: str, readings_file: str) -> None:
    '''Generate an entire experimental plate.

    1.  Build overall placement grid and sample locations.
    2.  Make head and body of design file and save it.
    3.  Make random readings for plate cells and save.
    4.  Save plate and design in respective output directories.

    Args:
        params: assay parameters.
        sample_id: which sample this plate is for.
        kind: 'calibration' or something else.
        design_file: where to write design.
        readings_file: where to write readings.
    '''
    placement, sample_locs = _make_placement(kind)

    design = [*_make_head('design', sample_id), *_generate(params, sample_locs, _make_treatment)]
    _save(design_file, _normalize_csv(design))

    readings = [*_make_head('readings', sample_id), *_generate(params, sample_locs, _make_reading)]
    _save(readings_file, _normalize_csv(readings))


def _make_reading(params: AssayParams, treated: bool) -> float:
    '''Generate a single plate reading.

    The reading is a random value whose mean depends on whether it is treated or a control.

    Args:
        params: assay parameters.
        treated: is this location treated (versus a control)?

    Returns:
        Randomly-generated reading value.
    '''
    mean = params.treated_val if treated else params.control_val
    value = max(0.0, random.gauss(mean, params.stdev))
    return f'{value:.02f}'


def _make_treatment(params: AssayParams, treated: bool) -> str:
    '''Select a single plate treatment.

    Args:
        params: assay parameters.
        treated: is this location treated (versus a control)?

    Returns:
        Treatment if this is a treated cell or a randomly-selected control if it is not.
    '''
    result = params.treatment if treated else random.choice(params.controls)
    return result


def _normalize_csv(rows: list) -> list:
    '''Make sure all rows in list-of-lists table are the same length.

    Short rows are extended with empty string values to match the length of the longest row.

    Args:
        rows: input list of lists.

    Returns:
        Adjusted list of lists.
    '''
    required = max(len(r) for r in rows)
    for row in rows:
        row.extend([''] * (required - len(row)))
    return rows


def _save(filename: str|None, rows: list) -> None:
    '''Save results to file or show on standard output.

    Args:
        filename: output file (or None to write to standard output)
        rows: data to write.
    '''
    if not filename:
        csv.writer(sys.stdout).writerows(rows)
    else:
        csv.writer(open(filename, 'w'), lineterminator='\n').writerows(rows)
