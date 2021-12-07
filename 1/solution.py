test_input = '''199
200
208
210
200
207
240
269
260
263'''

def count_increases(report: list) -> int:
    prev_depth = report[0]
    n_increases = 0

    for depth in report[1:]:
        if depth > prev_depth:
            n_increases += 1
        prev_depth = depth

    return n_increases

def count_increases_window(report: list, window: int=3) -> int:
    prev_depth_window = sum(report[0:window])
    n_increases = 0

    idx = 1
    while(len(report) >= idx + window):
        depth_window = sum(report[idx:idx+window])
        if depth_window > prev_depth_window:
            n_increases += 1
        prev_depth_window = depth_window
        idx += 1

    return n_increases

def format_input(input: str) -> list[int]:
    return [int(val) for val in input.split('\n')]

def read_input(path: str='1/input.txt') -> str:
    with open(path, 'r') as infile:
        return infile.read()

if __name__=='__main__':
    test_input_formatted = format_input(test_input)
    input_formatted = format_input(read_input())

    # solution 1
    assert count_increases(test_input_formatted) == 7
    print(count_increases(input_formatted))

    # solution 2
    assert count_increases_window(test_input_formatted) == 5
    print(count_increases_window(input_formatted))
