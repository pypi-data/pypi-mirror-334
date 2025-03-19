'''Mangle readings plate files to simulate poor formatting.'''

from argparse import Namespace
import csv
from pathlib import Path
import random
import sqlite3


# Query used to join records from database.
SELECT = '''
select
    plate.plate_id as plate_id,
    plate.filename as filename,
    plate.date as date,
    staff.staff_id as staff_id,
    staff.personal as personal,
    staff.family as family
from
    plate join performed join staff
on
    (plate.sample_id = performed.sample_id)
    and
    (performed.staff_id = staff.staff_id)
'''


def mangle(options: Namespace) -> None:
    '''Main driver for mangling readings plates.

    -   options.dbfile: path to SQLite database.
    -   options.outdir: output directory.
    -   options.tidy: directory containing tidy readings files.

    Mangled files are written to the specified output directory.
      The files have the same name as the original (tidy) files.

    Args:
        options: see above.
    '''
    con = sqlite3.connect(options.dbfile)
    con.row_factory = sqlite3.Row
    records = list(dict(r) for r in con.execute(SELECT).fetchall())
    random.seed(len(records))
    records = _consolidate(records)
    for rec in records:
        _mangle_file(options, rec)


def _consolidate(records: list) -> list:
    '''Pick a single (plate, staff) pair for each plate.

    Args:
        records: list of (plate, staff) pairs from database.

    Returns:
        One (plate, staff) pair for each plate.
    '''
    grouped = {}
    for r in records:
        if r['plate_id'] not in grouped:
            grouped[r['plate_id']] = []
        grouped[r['plate_id']].append(r)

    result = []
    for group in grouped.values():
        result.append(random.choice(group))
    return result


def _mangle_file(options: Namespace, record: dict) -> None:
    '''Mangle a single file.

    1.  Read file as header and body sections.
    2.  Apply randomly-chosen mangling functions to modify in place.
    3.  Save result.

    Args:
        options: see above.
        record: dictionary of database query results for a single record.
    '''
    sections = _read_sections(options, record['filename'])
    for func in (_do_staff_name, _do_date, _do_footer, _do_indent,):
        if random.random() < func.prob:
            func(record, sections)
    _write_sections(options, record['filename'], sections)


def _do_date(record: dict, sections: dict) -> None:
    '''Mangle data in place by adding date in header.

    Args:
        record: entire record data.
        sections: dictionary of header, body, and footer.
    '''
    row = [''] * len(sections['header'][0])
    row[0] = 'Date'
    row[1] = record['date']
    sections['header'].append(row)
_do_date.prob = 0.1


def _do_footer(record: dict, sections: dict) -> None:
    '''Mangle data in place by adding a footer.

    Args:
        record: entire record data.
        sections: dictionary of header, body, and footer.
    '''
    blank = [''] * len(sections['header'][0])
    foot = [''] * len(sections['header'][0])
    foot[0] = record['staff_id']
    sections['footer'] = [blank, foot]
_do_footer.prob = 0.1


def _do_indent(record: dict, sections: dict) -> None:
    '''Mangle data in place by indenting all rows by one space

    Args:
        record: entire record data.
        sections: dictionary of header, body, and footer.
    '''
    for section in sections.values():
        for row in section:
            row.insert(0, '')
_do_indent.prob = 0.1


def _do_staff_name(record: dict, sections: dict) -> None:
    '''Mangle data in place by adding staff name.

    Args:
        record: entire record data.
        sections: dictionary of header, body, and footer.
    '''
    sections['header'][0][-2] = f'{record["personal"]} {record["family"]}'
_do_staff_name.prob = 0.1


def _read_sections(options: Namespace, filename: str) -> dict:
    '''Read tidy readings file and split into sections.

    Args:
        options: see above.
        filename: file to read from.

    Returns:
        Dictionary with header, head-to-body spacing, body, and footer (empty in tidy file).
    '''
    with open(Path(options.tidy, filename), 'r') as raw:
        rows = [row for row in csv.reader(raw)]
    return {
        'header': rows[0:1],
        'headspace': rows[1:2],
        'body': rows[2:],
        'footer': []
    }


def _write_sections(options: Namespace, filename: str, sections: dict) -> None:
    '''Write sections of mangled file to file.

    Args:
        options: see above.
        filename: file to write to.
        sections: dictionary of header, head-to-body spacing, body, and footer.
    '''
    with open(Path(options.outdir, filename), 'w') as raw:
        writer = csv.writer(raw, lineterminator='\n')
        for section in sections.values():
            writer.writerows(section)
