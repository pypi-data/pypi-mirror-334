'''Generate snailz sample grids using invasion percolation.

To create a grid:

1.  Generate an MxN grid of random numbers. (Our are always square and odd-sized.)
2.  Mark the center cell as "filled" by negating its value.
3.  On each iteration:
    1.  Find the lowest-valued cell adjacent to the filled region.
    2.  Fill that in by negating its value. (If several cells tie for lowest value, pick one at random.)
4.  Stop when the filled region hits the edge of the grid.

Instead of repeatedly searching for cells adjacent to the filled region,
  the grid keeps a value-to-coordinates dictionary.
  When a cell is filled in, neighbors not already recorded are added.

The grid is saved as comma-separated values.
  0 shows unfilled cells; filled cells contain their original (positive) value.
'''

from argparse import Namespace
from pathlib import Path
import polars as pl
import random

from .params import GridParams, load_params


class Grid:
    '''Represent a 2D grid that supports lazy filling.'''

    def __init__(self, params: GridParams) -> None:
        '''Record shared state.

        Args:
            params: grid creation parameters.
        '''
        self._width = params.width
        self._height = params.height
        self._depth = params.depth
        self._grid = []
        for x in range(self._width):
            col = []
            for y in range(self._height):
                col.append(random.randint(1, self._depth))
            self._grid.append(col)
        self._candidates = {}

    def __getitem__(self, key: list|tuple) -> int:
        '''Get value at location.

        Args:
            key: (x, y) coordinates.

        Returns:
            Value at that location.
        '''
        x, y = key
        return self._grid[x][y]

    def __setitem__(self, key: list|tuple, value: int) -> None:
        '''Set value at location.

        Args:
            key: (x, y) coordinates.
            value: new value.
        '''
        x, y = key
        self._grid[x][y] = value

    def __str__(self) -> str:
        '''Convert to printable string.'''
        rows = []
        for y in range(self.height - 1, -1, -1):
            rows.append(''.join('x' if self[x, y] == 0 else '.' for x in range(self.width)))
        return '\n'.join(rows)

    @property
    def depth(self) -> int:
        '''Get depth of grid.'''
        return self._depth

    @property
    def height(self) -> int:
        '''Get height of grid.'''
        return self._height

    @property
    def width(self) -> int:
        '''Get width of grid.'''
        return self._width

    def fill(self) -> None:
        '''Fill grid one cell at a time.'''
        x, y = self.width // 2, self.height // 2
        self[x, y] = - self[x, y]
        self.add_candidates(x, y)
        while True:
            x, y = self.choose_cell()
            self[x, y] = - self[x, y]
            if self.on_border(x, y):
                break

    def add_candidates(self, x: int, y: int) -> None:
        '''Add candidates next to a newly-filled cell.

        Args:
            x: X coordinate of newly-filled cell.
            y: Y coordinate of newly-filled cell.

        '''
        for ix in (x - 1, x + 1):
            self.add_one_candidate(ix, y)
        for iy in (y - 1, y + 1):
            self.add_one_candidate(x, iy)

    def add_one_candidate(self, x: int, y: int) -> None:
        '''Add a point to the set of candidates.

        Args:
            x: X coordinate of potential candidate.
            y: Y coordinate of potential candidate.
        '''
        if (x < 0) or (x >= self.width) or (y < 0) or (y >= self.height):
            return
        if self[x, y] < 0:
            return

        value = self[x, y]
        if value not in self._candidates:
            self._candidates[value] = set()
        self._candidates[value].add((x, y))

    def adjacent(self, x: int, y: int) -> bool:
        '''Is (x, y) adjacent to a filled cell?

        Args:
            x: X coordinate of cell to check.
            y: Y coordinate of cell to check.

        Returns:
            Whether or not this cell is adjacent to a filled cell.
        '''
        x_1, y_1 = x + 1, y + 1
        if (x > 0) and (self[x - 1, y] < 0):
            return True
        if (x_1 < self.width) and (self[x_1, y] < 0):
            return True
        if (y > 0) and (self[x, y - 1] < 0):
            return True
        if (y_1 < self.height) and (self[x, y_1] < 0):
            return True
        return False

    def choose_cell(self) -> tuple:
        '''Choose the next cell to fill.

        Returns:
            (x, y) coordinates of next cell to fill.
        '''
        min_key = min(self._candidates.keys())
        available = list(sorted(self._candidates[min_key]))
        i = random.randrange(len(available))
        choice = available[i]
        del available[i]
        if not available:
            del self._candidates[min_key]
        else:
            self._candidates[min_key] = set(available)
        self.add_candidates(*choice)
        return choice

    def on_border(self, x: int, y: int) -> bool:
        '''Is this cell on the border of the grid?

        Args:
            x: X coordinate of cell to check.
            y: Y coordinate of cell to check.

        Returns:
            Whether or not this cell is on the border of the grid.
        '''
        if (x == 0) or (x == self.width - 1):
            return True
        if (y == 0) or (y == self.height - 1):
            return True
        return False


def grid(options: Namespace) -> None:
    '''Main driver for grid generation.

    -   options.outdir: path to output directory.
    -   options.params: path to grid parameter file.
    -   options.sites: path to sites parameter file.

    Args:
        options: see above.
    '''
    options.params = load_params(GridParams, options.params)
    options.sites = pl.read_csv(options.sites)
    random.seed(options.params.seed)
    for row in options.sites.iter_rows(named=True):
        grid = Grid(options.params)
        grid.fill()
        _save(options.outdir, row['site_id'], grid)


def _save(outdir: str, site_id: str, grid: Grid) -> None:
    '''Save grid as CSV.

    Args:
        outdir: output directory.
        site_id: site identifier (used to construct output filename).
        grid: what to save.
    '''
    Path(outdir).mkdir(parents=True, exist_ok=True)
    with open(Path(outdir, f'{site_id}.csv'), 'w') as writer:
        for y in range(grid.height - 1, -1, -1):
            values = (- grid[x, y] if grid[x, y] < 0 else 0 for x in range(grid.width))
            print(','.join((str(v) for v in values)), file=writer)
