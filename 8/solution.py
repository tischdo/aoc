from dataclasses import dataclass
from itertools import combinations_with_replacement
import pprint

segment_numbers = {
    0: 'abcefg',
    1: 'cf',
    2: 'acdeg',
    3: 'acdfg',
    4: 'bcdf',
    5: 'abdfg',
    6: 'abdefg',
    7: 'acf',
    8: 'abcdefg',
    9: 'abcdfg'
}

test_input = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

@dataclass
class DigitsStore:
    signal_patterns: list[str]
    output_values: list[str]

def read_input(path: str='8/input.txt') -> str:
    with open(path, 'r') as infile:
        return infile.read()

def format_input(input: str) -> list[DigitsStore]:
    lines = input.splitlines()
    digits_stores = []
    for line in lines:
        signal_patterns_raw, output_values_raw = line.split(' | ')
        signal_patterns = [pattern.strip() for pattern in signal_patterns_raw.split(' ') if pattern]
        output_values = [pattern.strip() for pattern in output_values_raw.split(' ') if pattern]
        digits_stores.append(DigitsStore(
            signal_patterns,
            output_values
        ))
    return digits_stores

def count_output_numbers_by_pattern_length(digits_stores: list[DigitsStore],
                                           selected_numbers: list[int]):
    pattern_length = set(
        len(segment_numbers[number])
        for number in selected_numbers)
    total = 0

    for digit_store in digits_stores:
        for pattern in digit_store.output_values:
            if len(pattern) in pattern_length:
                total += 1
    return total


def deduce_output(digits_store: DigitsStore) -> int:
    all_mappings = {letter: 'abcdefg' for letter in 'abcdefg'}

    # deduce 1
    for pattern in digits_store.signal_patterns:
        if len(pattern) == 2:
            pattern_one = pattern
            break
    for letter in pattern_one:
        all_mappings[letter] = segment_numbers[1]
    for key, value in all_mappings.items():
        if key not in pattern_one:
            all_mappings[key] = ''.join(set(value) - set(segment_numbers[1]))

    # deduce 7
    for pattern in digits_store.signal_patterns:
        if len(pattern) == 3:
            pattern_seven = pattern
            break
    additional_letter_to_one = (set(pattern_seven) - set(pattern_one)).pop()
    all_mappings[additional_letter_to_one] = 'a'
    for key, value in all_mappings.items():
        if key != additional_letter_to_one:
            all_mappings[key] = ''.join(set(value) - set('a'))

    # brute force all the rest (sorry for ugliness!)
    for a_replacements in all_mappings['a']:
        for b_replacements in all_mappings['b']:
            for c_replacements in all_mappings['c']:
                for d_replacements in all_mappings['d']:
                    for e_replacements in all_mappings['e']:
                        for f_replacements in all_mappings['f']:
                            for g_replacements in all_mappings['g']:
                                matched = 0
                                for signal_pattern in digits_store.signal_patterns:
                                    new_signal_pattern_list = []
                                    if 'a' in signal_pattern:
                                        new_signal_pattern_list.append(a_replacements)
                                    if 'b' in signal_pattern:
                                        new_signal_pattern_list.append(b_replacements)
                                    if 'c' in signal_pattern:
                                        new_signal_pattern_list.append(c_replacements)
                                    if 'd' in signal_pattern:
                                        new_signal_pattern_list.append(d_replacements)
                                    if 'e' in signal_pattern:
                                        new_signal_pattern_list.append(e_replacements)
                                    if 'f' in signal_pattern:
                                        new_signal_pattern_list.append(f_replacements)
                                    if 'g' in signal_pattern:
                                        new_signal_pattern_list.append(g_replacements)
                                    new_signal_pattern = ''.join(sorted(set(
                                        new_signal_pattern_list)))
                                    if new_signal_pattern in segment_numbers.values():
                                        matched += 1
                                if matched == 10:
                                    output_numbers = []
                                    for output_number_pattern in digits_store.output_values:
                                        new_output_number_list = []
                                        if 'a' in output_number_pattern:
                                            new_output_number_list.append(a_replacements)
                                        if 'b' in output_number_pattern:
                                            new_output_number_list.append(b_replacements)
                                        if 'c' in output_number_pattern:
                                            new_output_number_list.append(c_replacements)
                                        if 'd' in output_number_pattern:
                                            new_output_number_list.append(d_replacements)
                                        if 'e' in output_number_pattern:
                                            new_output_number_list.append(e_replacements)
                                        if 'f' in output_number_pattern:
                                            new_output_number_list.append(f_replacements)
                                        if 'g' in output_number_pattern:
                                            new_output_number_list.append(g_replacements)
                                        new_output_number_pattern = ''.join(sorted(set(
                                            new_output_number_list)))
                                        for integer, pattern in segment_numbers.items():
                                            if new_output_number_pattern == pattern:
                                                output_numbers.append(integer)
                                                break

                                    return int(''.join([str(val) for val in output_numbers]))
    return 0

if __name__=='__main__':
    test_digit_stores = format_input(test_input)
    digit_stores = format_input(read_input())

    unique_numbers = [1, 4, 7, 8]

    # solution 1
    test_counts = count_output_numbers_by_pattern_length(
        test_digit_stores,
        unique_numbers
    )
    assert test_counts == 26
    counts = count_output_numbers_by_pattern_length(
        digit_stores,
        unique_numbers
    )
    print(counts)

    # solution 2
    assert sum(deduce_output(ds) for ds in test_digit_stores) == 61229
    print(sum(deduce_output(ds) for ds in digit_stores))
