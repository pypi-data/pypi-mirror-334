r'''Snailz is a collection of synthetic data generators for use in teaching.

To re-create all of the data, run the following commands:

# Create copies of default parameter files (replacing './params' as necessary).
mkdir params
snailz params \
  --outdir params

# Make required output directories (replacing '.' as necessary).
mkdir -p data/grids data/designs data/readings

# Synthesize genomes for snails from survey sites.
snailz genomes \
  --outfile data/genomes.json \
  --params params/genomes.json

# Synthesize grids showing pollution at survey sites.
snailz grid \
  --grids params/grids.json \
  --outdir data/grids \
  --sites params/sites.csv

# Synthesize descriptions of snails collected in surveys.
snailz samples \
  --genomes data/genomes.json \
  --grids data/grids \
  --outfile data/samples.csv \
  --params params/samples.json \
  --sites params/sites.csv \
  --surveys params/surveys.csv

# Generate map of survey locations.
snailz survey \
  --outfile data/survey.png \
  --samples data/samples.csv

# Synthesize assay experiment descriptions.
snailz assays \
  --genomes data/genomes.json \
  --outfile data/assays.json \
  --params params/assays.json \
  --samples data/samples.csv

# Store information generated so far in a SQLite database.
snailz db \
  --dbfile data/lab.db \
  --assays data/assays.json \
  --samples data/samples.csv \
  --sites params/sites.csv \
  --surveys params/surveys.csv

# Synthesize assay plates used in those experiments.
snailz plates \
  --assays data/assays.json \
  --designs data/designs \
  --params params/assays.json \
  --readings data/readings

# Synthesize 'raw' reading files.
snailz mangle \
  --dbfile data/lab.db \
  --tidy data/readings \
  --outdir data/mangled
'''

from .assays import assays
from .db import db
from .genomes import genomes
from .grid import grid
from .mangle import mangle
from .plates import plates
from .samples import samples
from .surveymap import surveymap

__all__ = [
    'assays',
    'db',
    'genomes',
    'grid',
    'mangle',
    'plates',
    'samples',
    'surveymap',
]
