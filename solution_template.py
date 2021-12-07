import typing

test_input = """"""

def read_input(path: str='X/input.txt') -> str:
    with open(path, 'r') as infile:
        return infile.read()

def format_input(input: str) -> typing.Any:
    return

if __name__=='__main__':
    test_input_formatted = format_input(test_input)
    input_formatted = format_input(read_input())

    # solution 1
    assert True
