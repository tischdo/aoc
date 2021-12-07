from dataclasses import dataclass
from collections import Counter

test_input = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""

@dataclass
class Point():
    x: int
    y: int

    def __hash__(self) -> int:
        return hash((self.x, self.y))

@dataclass
class Vector():
    origin: Point
    target: Point

    def walk_straight(self) -> list[Point]:
        if (static_x := self.origin.x) == self.target.x:
            return [
                Point(x=static_x, y=y)
                for y in range(
                    min(self.origin.y, self.target.y),
                    max(self.origin.y, self.target.y) + 1
                )
            ]
        elif (static_y := self.origin.y) == self.target.y:
            return [
                Point(x=x, y=static_y)
                for x in range(
                    min(self.origin.x, self.target.x),
                    max(self.origin.x, self.target.x) + 1
                )
            ]
        else:
            return list()

    def walk(self) -> list[Point]:
        if points_straight := self.walk_straight():
            return points_straight

        if self.origin.x < self.target.x:
            x_range = range(self.origin.x, self.target.x + 1)
        else:
            x_range = range(self.origin.x, self.target.x - 1, -1)

        if self.origin.y < self.target.y:
            y_range = range(self.origin.y, self.target.y + 1)
        else:
            y_range = range(self.origin.y, self.target.y - 1, -1)

        return [
            Point(x=x, y=y)
            for x, y in zip(x_range, y_range)
        ]

def format_input(input: str) -> list[Vector]:
    lines = input.splitlines()
    segments = []
    for line in lines:
        origin_raw, target_raw = line.split(' -> ')
        origin = Point(*[int(val) for val in origin_raw.split(',')])
        target = Point(*[int(val) for val in target_raw.split(',')])
        segments.append(Vector(origin=origin, target=target))

    return segments

def read_input(path: str='5/input.txt') -> str:
    with open(path, 'r') as infile:
        return infile.read()

def solve(segments: list[Vector]):
    passed_points = []
    for segment in segments:
        if points := segment.walk_straight():
            passed_points.extend(points)

    return len(Counter(passed_points) - Counter(set(passed_points)))

def solve_v2(segments: list[Vector]):
    passed_points = []
    for segment in segments:
        if points := segment.walk():
            passed_points.extend(points)


    return len(Counter(passed_points) - Counter(set(passed_points)))

if __name__=='__main__':
    test_segments = format_input(test_input)
    segments = format_input(read_input())

    # solution 1
    assert solve(test_segments) == 5
    print(solve(segments))

    # solution 2
    assert solve_v2(test_segments) == 12
    print(solve_v2(segments))
