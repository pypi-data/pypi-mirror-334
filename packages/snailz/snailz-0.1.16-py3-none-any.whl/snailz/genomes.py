'''Generate genomes for snailz with random mutations.'''

from argparse import Namespace
from dataclasses import dataclass, asdict
import json
from pathlib import Path
import random

from .params import GenomeParams, load_params


# Bases.
DNA = 'ACGT'


@dataclass
class GenePool:
    '''Keep track of generated genomes.'''

    length: int
    reference: str
    individuals: list[str]
    locations: list[int]
    susceptible_loc: int = 0
    susceptible_base: str = ''


def genomes(options: Namespace) -> None:
    '''Main driver for genome generation.

    Each genome is a string of ACGT bases of the same length.
      One location is randomly chosen as "significant",
      and a specific mutation there predisposes the snail to size changes.
      Other mutations are added randomly at other locations.

    - options.params: parameter file.
    - options.outfile: output file.

    The result is saved as JSON with the following entries:

    - length: fixed length of all genomes.
    - reference: the unmutated reference genome.
    - individuals: a list of individual genomes with mutations.
    - locations: a list of locations where mutations may occur.
    - susceptible_loc: one of those locations where the significant mutation may occur.
    - susceptible_base: the mutated base at that location that indicates susceptibility.
    '''
    assert options.params != options.outfile, 'Cannot use same filename for options and parameters'
    options.params = load_params(GenomeParams, options.params)
    random.seed(options.params.seed)
    data = _random_genomes(options.params)
    _add_susceptibility(data)
    _save(options.outfile, data)


def _add_susceptibility(data: GenePool) -> None:
    '''Add indication of genetic susceptibility.

    Args:
        data: a GenePool instance being populated.
    '''
    if not data.locations:
        return
    loc = _choose_one(data.locations)
    choices = {ind[loc] for ind in data.individuals} - {data.reference[loc]}
    data.susceptible_loc = loc
    data.susceptible_base = _choose_one(list(sorted(choices)))


def _random_bases(length: int) -> str:
    '''Generate a random sequence of bases of the specified length.

    Args:
        length: desired genome length.

    Returns:
        Random sequence of bases of required length.
    '''
    assert 0 < length
    return ''.join(random.choices(DNA, k=length))


def _random_genomes(params: GenomeParams) -> GenePool:
    '''Generate a set of genomes with specified number of point mutations.

    Args:
        params: genome generation parameters.

    Returns:
        A GenePool object suitable for serialization.
    '''
    assert 0 <= params.num_snp <= params.length

    # Reference genomes and specific genomes to modify.
    reference = _random_bases(params.length)
    individuals = [reference] * params.num_genomes

    # Locations for SNPs.
    locations = random.sample(list(range(params.length)), params.num_snp)

    # Introduce significant mutations.
    for loc in locations:
        candidates = _other_bases(reference, loc)
        bases = [reference[loc]] + random.sample(candidates, k=len(candidates))
        individuals = [_mutate_snps(params, reference, ind, loc, bases) for ind in individuals]

    # Introduce other random mutations.
    other_locations = list(set(range(params.length)) - set(locations))
    individuals = [
        _mutate_other(ind, params.prob_other, other_locations) for ind in individuals
    ]

    # Return structure.
    individuals.sort()
    locations.sort()
    return GenePool(
        length=params.length, reference=reference, individuals=individuals, locations=locations
    )


def _save(outfile: str, data: GenePool) -> None:
    '''Save or show generated data.

    Args:
        outfile: output filename.
        data: to be saved.
    '''
    as_text = json.dumps(asdict(data), indent=4)
    if outfile:
        Path(outfile).write_text(as_text)
    else:
        print(as_text)


def _mutate_snps(params: GenomeParams, reference: str, genome: str, loc: int, bases: str) -> str:
    '''Introduce single nucleotide polymorphisms at the specified location.

    Args:
        params: genome generation parameters.
        reference: reference genome.
        genome: genome to mutate.
        loc: where to introduce mutation.
        bases: alternative bases.

    Returns:
        Mutated genome.
    '''
    choice = _choose_one(bases, params.snp_probs)
    return genome[:loc] + choice + genome[loc + 1 :]


def _mutate_other(genome: str, prob: float, locations: list) -> str:
    '''Introduce other mutations at specified locations.

    Args:
        genome: to be mutated.
        prob: probability of mutation.
        locations: where mutation might occur

    Returns:
        Possibly-mutated genome.
    '''
    if random.random() > prob:
        return genome
    loc = random.sample(locations, k=1)[0]
    base = random.choice(_other_bases(genome, loc))
    genome = genome[:loc] + base + genome[loc + 1 :]
    return genome


def _choose_one(values: list, weights: list|None = None) -> object:
    '''Convenience wrapper to choose a single items with weighted probabilities.

    Args:
        values: what to choose from.
        weights: optional list of weights.

    Returns:
        One value chosen at random from those given.
    '''
    return random.choices(values, weights=weights, k=1)[0]


def _other_bases(seq: str, loc: int) -> list:
    '''Create a list of bases minus the one in the sequence at that location.

    Returns a list instead of a set because the result is used in random.choices(),
      which requires an indexable sequence. Result is sorted for reproducibility.

    Args:
        seq: base sequence.
        loc: location of base to _not_ choose.

    Returns:
        List of other bases.
    '''
    return list(sorted(set(DNA) - {seq[loc]}))
