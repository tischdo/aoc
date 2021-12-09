import operator
from dataclasses import dataclass
from functools import reduce

test_input = """2199943210
3987894921
9856789892
8767896789
9899965678
"""
test_input_2 = """988
882
161
"""

@dataclass
class Point():
    x: int
    y: int
    value: int | None=None

@dataclass
class Heightmap():
    grid: list[list[int]]

    def __post_init__(self):
        self.height: int = len(self.grid[0])
        self.width: int = len(self.grid)

    def get_depth(self, x: int, y: int, default: int=10) -> int:
        if x < 0 or y < 0:
            return default
        try:
            return self.grid[x][y]
        except IndexError:
            return default

    def find_minima(self) -> list[Point]:
        minima = []
        for x in range(self.width):
            for y in range(self.height):
                depth = self.get_depth(x, y)
                adjacent_depths = [
                    self.get_depth(x_adj, y_adj)
                    for x_adj, y_adj in [
                        (x, y+1),
                        (x, y-1),
                        (x-1, y),
                        (x+1, y)
                    ]
                ]
                if all(depth < depth_adj for depth_adj in adjacent_depths):
                    minima.append(Point(x=x, y=y, value=depth))
        return minima

    def find_basin_size(self,
                        point: Point,
                        prev_points: list[Point] | None=None) -> int:
        if prev_points is None:
            prev_points = [point]

        x, y = point.x, point.y
        cur_depth = self.get_depth(x, y)
        for x_adj, y_adj in [
            (x, y+1),
            (x, y-1),
            (x-1, y),
            (x+1, y)
        ]:
            adj_point = Point(x_adj, y_adj)
            if (
                (depth_adj := self.get_depth(x_adj, y_adj)) < 9
                and depth_adj > cur_depth
                and adj_point not in prev_points
            ):
                prev_points.append(adj_point)
                self.find_basin_size(point=adj_point, prev_points=prev_points)

        return len(prev_points)

    def find_basin_sizes(self,
                         minima: list[Point]):
        basin_sizes = []
        for minimum in minima:
            basin_size = self.find_basin_size(point=minimum)
            basin_sizes.append(basin_size)
        return basin_sizes

    def risk_level(self):
        minima = self.find_minima()
        return sum(minimum.value + 1 for minimum in minima)

    def solve_v2(self) -> int:
        minima = self.find_minima()
        basin_sizes = self.find_basin_sizes(minima)

        return reduce(operator.mul, sorted(basin_sizes, reverse=True)[:3])

def read_input(path: str='9/input.txt') -> str:
    with open(path, 'r') as infile:
        return infile.read()

def format_input(input: str) -> Heightmap:
    grid = []
    for row in input.splitlines():
        grid.append([int(val) for val in list(row)])
    return Heightmap(grid=grid)

if __name__=='__main__':
    test_heatmap = format_input(test_input)
    test_heatmap_2 = format_input(test_input_2)
    heatmap = format_input(read_input())

    # solution 1
    assert test_heatmap.risk_level() == 15
    assert test_heatmap_2.risk_level() == 4
    print(heatmap.risk_level())

    # solution 2
    assert test_heatmap.solve_v2() == 1134
    print(heatmap.solve_v2())
