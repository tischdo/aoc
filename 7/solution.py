from dataclasses import dataclass

test_input = """16,1,2,0,4,2,7,1,2,14"""

@dataclass
class Result():
    position: int
    total_fuel: int

def read_input(path: str='7/input.txt') -> str:
    with open(path, 'r') as infile:
        return infile.read()

def format_input(input: str) -> list[int]:
    return [int(value) for value in input.split(',')]

def calculate_fuel(positions: list[int], target_position: int) -> int:
    total_fuel = 0

    for position in positions:
        total_fuel += abs(position - target_position)

    return total_fuel

def calculate_fuel_v2(positions: list[int], target_position: int) -> int:
    total_fuel = 0

    for position in positions:
        total_fuel += increasing_fuel_sum(abs(position - target_position))

    return total_fuel

def increasing_fuel_sum(delta: int) -> int:
    return sum(range(1, delta+1))

def find_optimal_position(positions: list[int], mode: str='v1') -> Result:
    if mode == 'v1':
        fuel_func = calculate_fuel
    else:
        fuel_func = calculate_fuel_v2
    cur_best_position = min(positions)
    cur_total_fuel = fuel_func(positions, min(positions))

    for position_to_test in range(min(positions)+1, max(positions)):
        total_fuel = fuel_func(positions, position_to_test)

        if total_fuel <= cur_total_fuel:
            cur_best_position = position_to_test
            cur_total_fuel = total_fuel

    return Result(
        position=cur_best_position,
        total_fuel=cur_total_fuel
    )

if __name__=='__main__':
    test_positions = format_input(test_input)
    positions = format_input(read_input())

    # solution 1
    assert find_optimal_position(test_positions).position == 2
    assert calculate_fuel(test_positions, 2) == 37
    assert calculate_fuel(test_positions, 1) == 41
    assert calculate_fuel(test_positions, 3) == 39
    assert calculate_fuel(test_positions, 10) == 71
    print(find_optimal_position(positions).total_fuel)

    # solution 2
    assert find_optimal_position(test_positions, mode='v2') == Result(5, 168)
    assert calculate_fuel_v2(test_positions, 2) == 206
    print(find_optimal_position(positions, mode='v2').total_fuel)
