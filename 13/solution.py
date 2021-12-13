from dataclasses import dataclass
from math import floor

test_input = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

@dataclass
class Point:
    x: int
    y: int

@dataclass
class Fold:
    pos: int
    axis: str

@dataclass
class Origami:
    points: list[Point]
    folds: list[Fold]

    def __post_init__(self):
        self.width = max(point.x for point in self.points) + 1
        self.height = max(point.y for point in self.points) + 1

        grid = [[False for _ in range(self.width)] for _ in range(self.height)]

        for point in self.points:
            grid[point.y][point.x] = True

        self.grid = grid

    def pprint(self):
        for y in range(self.height):
            row_str = ''
            for x in range(self.width):
                if self.grid[y][x]:
                    row_str += '#'
                else:
                    row_str += '.'
            print(row_str)

    def apply_fold(self, fold: Fold | None = None):
        fold = self.folds[0]
        self.folds = self.folds[1:]

        if fold.axis == 'y':
            for i in range(fold.pos, -1, -1):
                up, down = fold.pos - i, fold.pos + i
                if up < 0 or down >= self.height:
                    continue
                for x in range(self.width):
                    self.grid[up][x] |= self.grid[down][x]
            self.grid = [row for row in self.grid[:fold.pos]]
            self.height = self.height // 2
        elif fold.axis == 'x':
            for i in range(fold.pos, -1, -1):
                left, right = fold.pos - i, fold.pos + i
                if left < 0 or right >= self.width:
                    continue
                for y in range(self.height):
                    self.grid[y][left] |= self.grid[y][right]
            self.grid = [row[:fold.pos] for row in self.grid]
            self.width = self.width // 2
        else:
            raise NotImplementedError(f'Fold axis not implemented, {fold.axis}')

    def fold_all(self):
        for fold in self.folds:
            self.apply_fold(fold)

    def count(self):
        cnt = 0
        for row in self.grid:
            for val in row:
                if val:
                    cnt += 1
        return cnt

def read_input(path: str='13/input.txt') -> str:
    with open(path, 'r') as infile:
        return infile.read()

def format_input(input: str) -> Origami:
    points, folds = [], []
    for line in input.splitlines():
        if line:
            if not line.startswith('fold'):
                x, y = (int(val) for val in line.split(','))
                points.append(Point(
                    x=x,
                    y=y
                ))
            else:
                fold_str, value = line.split('=')
                folds.append(Fold(
                    pos=int(value),
                    axis=fold_str[-1]
                ))
    return Origami(
        points=points,
        folds=folds
    )

if __name__=='__main__':
    test_origami = format_input(test_input)
    origami = format_input(read_input())

    # solution 1
    test_origami.apply_fold()
    assert test_origami.count() == 17
    origami.apply_fold()
    print(origami.count())

    # solution 2
    origami.fold_all()
    origami.pprint()
