from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass

CYCLE_LENGTH = 6
CYCLE_LENGTH_NEW = 8

test_input = '3,4,3,1,2'

@dataclass
class Lanternfish():
    cycle: int
    reproduction_cycle_length: int=6
    cycle_length: int=8

    @classmethod
    def reproduce(cls) -> Lanternfish:
        return Lanternfish(cycle=CYCLE_LENGTH_NEW)

    def age(self) -> bool:
        if self.cycle > 0:
            self.cycle -= 1
            return False
        else:
            self.cycle = CYCLE_LENGTH
            return True

@dataclass
class Swarm():
    lanternfishes: list[Lanternfish]

    def age(self, days: int=1):
        for _ in range(days):
            lanternfishes = self.lanternfishes.copy()
            for lanternfish in self.lanternfishes:
                if lanternfish.age():
                    lanternfishes.append(Lanternfish.reproduce())
            self.lanternfishes = lanternfishes

    def pprint(self):
        print(','.join([str(lanternfish.cycle) for lanternfish in self.lanternfishes]))

    def count(self):
        return len(self.lanternfishes)

def read_input(path: str='6/input.txt') -> str:
    with open(path, 'r') as infile:
        return infile.read()

def format_input(input: str) -> Swarm:
    return Swarm([Lanternfish(cycle=int(cycle)) for cycle in input.split(',')])

@dataclass
class SwarmFast():
    population: Counter

    @classmethod
    def from_swarm(cls, swarm: Swarm) -> SwarmFast:
        return cls(Counter([lanternfish.cycle for lanternfish in swarm.lanternfishes]))

    def age(self, days: int=1):
        for _ in range(days):
            old_population = dict(self.population)
            new_population = defaultdict(int)

            for cycle in range(CYCLE_LENGTH_NEW, 0, -1):
                if cycle in old_population.keys():
                    new_population[cycle - 1] = (
                        old_population[cycle]
                    )

            if 0 in old_population.keys():
                new_population[CYCLE_LENGTH] = old_population[0] + new_population[CYCLE_LENGTH]
                new_population[CYCLE_LENGTH_NEW] += old_population[0]

            self.population = Counter(new_population)

    def count(self):
        return self.population.total()

if __name__=='__main__':
    test_swarm = format_input(test_input)
    swarm = format_input(read_input())

    test_swarm_fast = SwarmFast.from_swarm(test_swarm)
    swarm_fast = SwarmFast.from_swarm(swarm)

    # solution 1 (could also use _fast implementations here)
    test_swarm.age(days=18)
    assert test_swarm.count() == 26
    test_swarm.age(days=80-18)
    assert test_swarm.count() == 5934
    swarm.age(days=80)
    print(swarm.count())

    # solution 2
    test_swarm_fast.age(days=256)
    assert test_swarm_fast.count() == 26984457539
    swarm_fast.age(days=256)
    print(swarm_fast.count())
