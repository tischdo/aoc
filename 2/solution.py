import enum
from dataclasses import dataclass
from typing import NamedTuple

test_input = """forward 5
down 5
forward 8
up 3
down 8
forward 2
"""

class Command(enum.Enum):
    FORWARD=enum.auto()
    UP=enum.auto()
    DOWN=enum.auto()

class Position(NamedTuple):
    horizontal: int=0
    depth: int=0
    aim: int=0

@dataclass
class Instruction():
    command: Command
    steps: int

    def apply(self, mode: str, last_position: Position | None=None) -> Position:
        if mode not in (available_modes := ('v1', 'v2')):
            raise ValueError(f'Mode {mode} not implemented. Available modes: {available_modes}')

        if last_position is None:
            last_position = Position()

        match (self.command, mode):
            case (Command.FORWARD, 'v1'):
                return Position(
                    horizontal=last_position.horizontal + self.steps,
                    depth=last_position.depth
                )
            case (Command.FORWARD, 'v2'):
                return Position(
                    horizontal=last_position.horizontal + self.steps,
                    depth=last_position.depth + (last_position.aim * self.steps),
                    aim=last_position.aim
                )
            case (Command.UP, 'v1'):
                return Position(
                    horizontal=last_position.horizontal,
                    depth=last_position.depth - self.steps
                )
            case (Command.UP, 'v2'):
                return Position(
                    horizontal=last_position.horizontal,
                    depth=last_position.depth,
                    aim=last_position.aim - self.steps
                )
            case (Command.DOWN, 'v1'):
                return Position(
                    horizontal=last_position.horizontal,
                    depth=last_position.depth + self.steps
                )
            case (Command.DOWN, 'v2'):
                return Position(
                    horizontal=last_position.horizontal,
                    depth=last_position.depth,
                    aim=last_position.aim + self.steps
                )
        raise NotImplementedError(f'Command not implemented: {self.command}')

def format_input(input: str) -> list[Instruction]:
    instructions_raw = input.splitlines()
    instructions = []

    for instruction_raw in instructions_raw:
        command, n_steps_raw = instruction_raw.split(' ')
        n_steps = int(n_steps_raw)
        match command:
            case 'forward':
                instruction = Instruction(Command.FORWARD, n_steps)
            case 'up':
                instruction = Instruction(Command.UP, n_steps)
            case 'down':
                instruction = Instruction(Command.DOWN, n_steps)
            case _:
                raise ValueError(f'Command not known: {command}')
        instructions.append(instruction)

    return instructions

def read_input(path: str='2/input.txt') -> str:
    with open(path, 'r') as infile:
        return infile.read()

def apply_instructions(instructions: list[Instruction], mode: str) -> Position:
    position = instructions[0].apply(mode=mode)

    for instruction in instructions[1:]:
        position = instruction.apply(last_position=position, mode=mode)

    return position

def multiply_position(position: Position):
    return position.horizontal * position.depth

def navigate(instructions = list[Instruction], mode:str='v1') -> int:
    final_position = apply_instructions(instructions, mode=mode)
    return multiply_position(final_position)

if __name__=='__main__':
    test_instructions = format_input(test_input)
    instructions = format_input(read_input())

    # solution 1
    assert navigate(test_instructions) == 150
    print(navigate(instructions))

    # solution 2
    assert navigate(test_instructions, mode='v2') == 900
    print(navigate(instructions, mode='v2'))
