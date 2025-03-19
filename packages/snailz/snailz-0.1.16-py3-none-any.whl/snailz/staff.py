'''Generate snailz experimental staff by creating random first and last names.'''

from argparse import Namespace
import faker
from pathlib import Path
import polars as pl
import random
import sys

from .params import StaffParams, load_params


def staff(options: Namespace) -> None:
    '''Main driver for snailz experimental staff creation.

    -   options.params: path to parameter file (see params.StaffParams for fields).
    -   options.outfile: optional path to saved output file.

    Generated data is written as CSV to the specified output file.

    Args:
        options: see above.
    '''
    options.params = load_params(StaffParams, options.params)
    random.seed(options.params.seed)
    faker.Faker.seed(options.params.seed)
    fake = faker.Faker(options.params.locale)
    people = _make_people(options.params, fake)
    _save(options, people)


def _make_people(params: StaffParams, fake: faker.Faker) -> pl.DataFrame:
    '''Create people.

    Args:
        params: staff generation parameters.
        fake: fake name generator.

    Returns:
        Dataframe containing staff ID, personal name, and family name.
    '''
    people = [(i+1, fake.first_name(), fake.last_name()) for i in range(params.num)]
    return pl.DataFrame(people, schema=('staff_id', 'personal', 'family'), orient='row')


def _save(options: Namespace, people: pl.DataFrame) -> None:
    '''Save results to file or show on standard output.

    Args:
        options: controlling options.
        people: dataframe of staff ID, personal name, and family name.
    '''
    if options.outfile:
        people.write_csv(Path(options.outfile))
    else:
        people.write_csv(sys.stdout)
