from dataclasses import dataclass

test_input = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""

OPENING_BRACKETS = list('([{<')
CLOSING_BRACKETS = list(')]}>')
BRACKETS_SCORES = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}
BRACKETS_SCORES_V2 = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}
BRACKETS_PAIRS = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}

@dataclass
class Instructions:
    line: str

    def check_syntax(self) -> int:
        brackets = []
        for char in self.line:
            if char in OPENING_BRACKETS:
                brackets.append(char)
            elif char in CLOSING_BRACKETS:
                last_bracket = brackets.pop()
                if BRACKETS_PAIRS[last_bracket] != char:
                    return BRACKETS_SCORES[char]
        return 0

    def missing_brackets(self) -> str:
        if self.check_syntax() != 0:
            return ''

        brackets: list[str] = []
        for char in self.line:
            if char in OPENING_BRACKETS:
                brackets.append(char)
            else:
                # validation is already checked in check_syntax
                brackets.pop()

        return ''.join(BRACKETS_PAIRS[bracket] for bracket in reversed(brackets))

    def calculate_missing_score(self):
        if not (closing_brackets := self.missing_brackets()):
            return 0

        score = 0
        for bracket in closing_brackets:
            score *= 5
            score += BRACKETS_SCORES_V2[bracket]

        return score


@dataclass
class Program:
    instructions: list[Instructions]

    def calculate_score(self):
        scores = sorted([
            score
            for instruction in self.instructions
            if (score := instruction.calculate_missing_score()) > 0
        ])
        return scores[len(scores) // 2]

def read_input(path: str='10/input.txt') -> str:
    with open(path, 'r') as infile:
        return infile.read()

def format_input(input: str) -> list[Instructions]:
    return [Instructions(line=line) for line in input.splitlines()]


if __name__=='__main__':
    test_instructions = format_input(test_input)
    instructions = format_input(read_input())

    # # solution 1
    test_syntax_error_score = sum([
        test_instruction.check_syntax()
        for test_instruction in test_instructions
    ])
    assert test_syntax_error_score == 26397
    syntax_error_score = sum([
        instruction.check_syntax()
        for instruction in instructions
    ])
    print(syntax_error_score)

    # solution 2
    test_program = Program(test_instructions)
    assert test_program.calculate_score() == 288957
    program = Program(instructions)
    print(program.calculate_score())
