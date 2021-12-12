from collections import defaultdict, Counter
from dataclasses import dataclass, field

test_input_one = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""

test_input_two = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""

test_input_three = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""

@dataclass
class Cave:
    cave_map: dict[str, set]
    paths: list = field(default_factory=list)
    mode: str = 'v1'

    def walk(self, cur_path: list[str] | None = None):
        if cur_path is None:
            cur_path = ['start']
        cur_position = cur_path[-1]

        for destination in self.cave_map[cur_position]:
            if self.is_valid_path(cur_path, destination):
                next_path = cur_path + [destination]
                if destination == 'end':
                    self.paths.append(next_path)
                else:
                    self.walk(next_path)

    def is_valid_path(self,
                      cur_path: list[str],
                      destination: str):
        counts = Counter(cur_path + [destination])
        if counts.pop('start') > 1:
            return False

        if self.mode == 'v1':
            for cave in cur_path:
                if all(char.lower() == char for char in cave):
                    # small caves
                    if counts[cave] > 1:
                        return False
        else:
            visited_twice = False
            for cave in set(cur_path) - {'start', 'end'}:
                if all(char.lower() == char for char in cave):
                    # small caves
                    if counts[cave] > 2:
                        return False
                    if counts[cave] > 1:
                        if visited_twice:
                            return False
                        visited_twice = True

        return True

def read_input(path: str='12/input.txt') -> str:
    with open(path, 'r') as infile:
        return infile.read()

def format_input(input: str) -> Cave:
    cave_map = defaultdict(set)

    for path in input.splitlines():
        from_, to = path.split('-')
        cave_map[from_].add(to)
        cave_map[to].add(from_)

    return Cave(cave_map)


if __name__=='__main__':
    test_cave_one = format_input(test_input_one)
    test_cave_two = format_input(test_input_two)
    test_cave_three = format_input(test_input_three)
    cave = format_input(read_input())

    # solution 1
    test_cave_one.walk()
    assert len(test_cave_one.paths) == 10
    test_cave_two.walk()
    assert len(test_cave_two.paths) == 19
    test_cave_three.walk()
    assert len(test_cave_three.paths) == 226
    cave.walk()
    print(len(cave.paths))

    # solution 2
    test_cave_one = format_input(test_input_one)
    test_cave_two = format_input(test_input_two)
    test_cave_three = format_input(test_input_three)
    cave = format_input(read_input())
    test_cave_one.mode = 'v2'
    test_cave_two.mode = 'v2'
    test_cave_three.mode = 'v2'
    cave.mode = 'v2'

    test_cave_one.walk()
    assert len(test_cave_one.paths) == 36
    test_cave_two.walk()
    assert len(test_cave_two.paths) == 103
    test_cave_three.walk()
    assert len(test_cave_three.paths) == 3509

    # warning: takes about 13s on my laptop
    cave.walk()
    print(len(cave.paths))
