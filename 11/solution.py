from copy import deepcopy
from dataclasses import dataclass

test_input = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""

@dataclass
class Position:
    h: int
    w: int

    def __hash__(self):
        return hash(self.h * -self.w)

@dataclass
class OctopusMap:
    grid: list[list[int]]

    height: int = 10
    width: int = 10
    total_flashes: int = 0

    def increase_energy_level(self) -> list[list[int]]:
        temp_grid = deepcopy(self.grid)
        for h in range(self.height):
            for w in range(self.width):
                temp_grid[h][w] += 1

        return temp_grid

    def flash(self, temp_grid: list[list[int]], position: Position) -> list[list[int]]:
        for h_adj, w_adj in [
            (position.h+1, position.w),
            (position.h-1, position.w),
            (position.h, position.w+1),
            (position.h, position.w-1),
            (position.h+1, position.w+1),
            (position.h-1, position.w+1),
            (position.h+1, position.w-1),
            (position.h-1, position.w-1)
        ]:
            if h_adj >= 0 and h_adj < self.height and w_adj >= 0 and w_adj < self.width:
                temp_grid[h_adj][w_adj] += 1
        return temp_grid

    def in_sync(self) -> bool:
        for h in range(self.height):
            for w in range(self.width):
                if self.grid[h][w] != 0:
                    return False
        return True

    def cascade(self,
                temp_grid: list[list[int]],
                has_flashed: None | set[Position] = None) -> \
                    tuple[list[list[int]], set[Position]]:
        if has_flashed is None:
            has_flashed = set()
        for h in range(self.height):
            for w in range(self.width):
                if temp_grid[h][w] > 9:
                    position = Position(h, w)
                    if position not in has_flashed:
                        has_flashed.add(position)
                        self.cascade(self.flash(temp_grid, position), has_flashed)

        return temp_grid, has_flashed

    def relax(self, temp_grid: list[list[int]], has_flashed: set[Position]):
        for position in has_flashed:
            temp_grid[position.h][position.w] = 0
        return temp_grid

    def step(self, n: int = 1, verbose: bool = False):
        for _ in range(n):
            temp_grid = self.increase_energy_level()
            temp_grid, has_flashed = self.cascade(temp_grid)

            temp_grid = self.relax(temp_grid, has_flashed)
            if verbose:
                self.pprint(temp_grid)

            self.grid = temp_grid
            self.total_flashes += len(has_flashed)

    def step_until_sync(self) -> int:
        cycles = 0
        while not self.in_sync():
            self.step()
            cycles += 1
        return cycles

    def pprint(self, temp_grid: list[list[int]]):
        for h in range(self.height):
            for w in range(self.width):
                print(temp_grid[h][w], end='')
            print()

def read_input(path: str='11/input.txt') -> str:
    with open(path, 'r') as infile:
        return infile.read()

def format_input(input: str) -> OctopusMap:
    return OctopusMap(
        grid=[
            [int(val) for val in line]
            for line in input.splitlines()
        ]
    )

if __name__=='__main__':
    test_octopus_map = format_input(test_input)
    octopus_map = format_input(read_input())

    # solution 1
    test_octopus_map.step(100)
    assert test_octopus_map.total_flashes == 1656
    octopus_map.step(100)
    print(octopus_map.total_flashes)

    # solution 2
    test_octopus_map = format_input(test_input)
    octopus_map = format_input(read_input())
    assert test_octopus_map.step_until_sync() == 195
    print(octopus_map.step_until_sync())
