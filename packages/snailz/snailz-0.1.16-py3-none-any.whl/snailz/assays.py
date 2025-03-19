'''Generate snailz assays.'''

from argparse import Namespace
from datetime import date, datetime, time, timedelta, timezone
import json
from pathlib import Path
import polars as pl
import random
import string
import pytz

from .params import AssayParams, load_params


class DateTimeEncoder(json.JSONEncoder):
    '''Encode date and datetime objects as JSON.'''

    def default(self, obj: date|datetime) -> str:
        '''Encode date or datetime.

        Args:
            obj: what to encode.

        Returns:
            String representation.
        '''
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()


def assays(options: Namespace) -> None:
    '''Main driver for assay generation.

    1.  Load previously-generated samples and staff.
    2.  Generate experiments for some samples, each performed by one or more staff.
    3.  Save.

    Args:
        options: options object.
    '''
    assert options.params != options.outfile, 'Cannot use same filename for options and parameters'
    options.params = load_params(AssayParams, options.params)
    random.seed(options.params.seed)

    mutant_status = _reload_mutant_status(options)
    staff_ids = _reload_staff(options)
    result = _make_experiments(options.params, mutant_status, staff_ids)
    _save(options.outfile, result)


def _reload_mutant_status(options: Namespace) -> list:
    '''Re-create sample genomic information.

    Args:
        options: controlling options.

    Returns:
        List of Booleans showing which samples are for mutant snails.
    '''
    genomes = json.loads(Path(options.genomes).read_text())
    susc_loc = genomes['susceptible_loc']
    susc_base = genomes['susceptible_base']
    samples = pl.read_csv(options.samples)
    return [g[susc_loc] == susc_base for g in samples['sequence']]


def _reload_staff(options: Namespace) -> pl.DataFrame:
    '''Re-load staff information.

    Args:
        options: controlling options.

    Returns:
        Dataframe with staff information.
    '''
    return pl.read_csv(options.staff)['staff_id'].to_list()


def _make_experiments(params: AssayParams, mutant_status: list, staff_ids: list) -> dict:
    '''Create experiments and their data.

    Args:
        params: assay generation parameters.
        mutant_status: list showing which samples are mutants.
        staff_ids: list of staff IDs.

    Returns:
        Dictionary holding data to serialize.
    '''

    # Setup.
    kinds = list(params.assay_types)
    experiments = []
    performed = []
    plates = []

    # Which samples have experiments been done on?
    num_samples = len(mutant_status)
    keepers = set(random.sample(list(range(num_samples)), k=int(params.fraction * num_samples)))

    filename_gen = _make_random_filename_generator(params)
    for i, flag in enumerate(mutant_status):
        # Skip samples that aren't experimented on.
        if i not in keepers:
            continue

        # Create basic facts about experiment.
        sample_id = i + 1
        kind = random.choice(kinds)
        started, ended = _random_experiment_duration(params, kind)
        experiments.append(
            {'sample_id': sample_id, 'kind': kind, 'start': _round_date(started), 'end': _round_date(ended)}
        )

        # Keep track of staff involved in experiment.
        num_staff = random.randint(*params.assay_staff)
        performed.extend(
            [{'staff_id': s, 'sample_id': sample_id} for s in random.sample(staff_ids, num_staff)]
        )

        # Only generate plates for experiments that have finished.
        if ended is not None:
            plates.extend(
                _random_plates(params, kind, sample_id, len(plates), started, filename_gen)
            )

    # Invalidate some plates.
    invalidated = _invalidate_plates(params, staff_ids, plates)

    # Return structure with results.
    return {
        'experiment': experiments,
        'performed': performed,
        'plate': plates,
        'invalidated': invalidated
    }


def _invalidate_plates(params: AssayParams, staff_ids: int, plates: list) -> list:
    '''Invalidate a random set of plates.

    Args:
        params: assay generation parameters.
        staff_ids: list of staff IDs.
        plates: list of generated plates.

    Returns:
        List of dictionaries describing invalidated plates.
    '''
    selected = [
        (i, p['date']) for (i, p) in enumerate(plates) if random.random() < params.invalid
    ]
    return [
        {
            'plate_id': plate_id,
            'staff_id': random.choice(staff_ids),
            'date': _random_date_interval(exp_date, params.enddate),
        }
        for (plate_id, exp_date) in selected
    ]


def _make_random_filename_generator(params: AssayParams) -> callable:
    '''Create a random filename generator.

    Args:
        params: assay generation parameters.

    Returns:
        Unique random filename each time generator is invoked.
    '''
    filenames = set([''])
    result = ''
    while True:
        while result in filenames:
            stem = ''.join(random.choices(string.hexdigits, k=params.filename_length)).lower()
            result = f'{stem}.csv'
        filenames.add(result)
        yield result


def _random_experiment_duration(params: AssayParams, kind: str) -> tuple:
    '''Choose random start date and end date for experiment.

    The start date is uniformly selected from the experiment period.
      The end date is the same as or later than the start date,
      and `None` if the experiment hasn't finished.

    Args:
        params: assay generation parameters.
        kind: experimental procedure used.

    Returns:
        A pair with a start date and either an end date or `None`.
    '''
    start = random.uniform(params.startdate.timestamp(), params.enddate.timestamp())
    start = datetime.fromtimestamp(start, tz=timezone.utc)
    duration = timedelta(days=random.randint(*params.assay_duration))
    end = start + duration
    end = None if end > params.enddate else end
    return start, end


def _random_plates(params: AssayParams, kind: str, sample_id: int, start_id: int, start_date: date, filename_gen: str) -> list:
    '''Generate random plate data.

    Args:
        params: assay generation parameters.
        kind: experimental procedure used.
        sample_id: sample used in the experiment.
        start_id: starting ID of plates.
        start_date: when experiment started.
        filename_gen: random filename generator

    Returns:
        List of dictionaries of plate data.
    '''
    return [
        {
            'plate_id': start_id + i + 1,
            'sample_id': sample_id,
            'date': _random_date_interval(start_date, params.enddate),
            'filename': next(filename_gen),
        }
        for i in range(random.randint(*params.assay_plates))
    ]

def _random_date_interval(start_date: date, end_date: date) -> date:
    '''Choose a random date (inclusive).

    Args:
        start_date: earliest allowed date.
        end_date: last possible date.

    Returns:
        Randomly-selected date.
    '''
    # Convert date to datetime at midnight UTC
    start_datetime = datetime.combine(start_date, time.min).replace(tzinfo=pytz.UTC)
    end_datetime = datetime.combine(end_date, time.max).replace(tzinfo=pytz.UTC)

    choice_timestamp = random.uniform(start_datetime.timestamp(), end_datetime.timestamp())
    choice = datetime.fromtimestamp(choice_timestamp, tz=pytz.UTC)
    return _round_date(choice)

def _round_date(raw: datetime|None) -> date|None:
    '''Round time to whole day.

    Args:
        raw: starting datetime (or `None`).

    Returns:
        Input rounded to nearest whole day (or `None`).
    '''
    return None if raw is None else raw.date()

def _save(outfile: str, result: dict) -> None:
    '''Save or show generated data.

    Args:
        outfile: where to write (or `None` for standard output).
        result: data to write.
    '''
    as_text = json.dumps(result, indent=4, cls=DateTimeEncoder)
    if outfile:
        Path(outfile).write_text(as_text)
    else:
        print(as_text)
