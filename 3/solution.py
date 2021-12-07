from collections import Counter

test_input = """00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010"""

def format_input(input: str) -> list[str]:
    return input.splitlines()

def read_input(path: str='3/input.txt') -> str:
    with open(path, 'r') as infile:
        return infile.read()

# part 1
def count_bits(report: list[str], mode: str) -> list[str]:
    n_bits = len(report[0])
    bit_counts = []

    for bit_idx in range(n_bits):
        bits_at_idx = [bits[bit_idx] for bits in report]
        counts = Counter(bits_at_idx).most_common()

        counts = counts if mode == 'gamma' else counts[::-1]
        bit_counts.append(counts[0][0])

    return bit_counts

# part 2
def filter_bits(report: list[str], mode: str) -> list[str]:
    report = report.copy()
    bit_idx = 0

    def bit_to_keep(counts: list[tuple[str, int]]) -> str:
        if counts[0][1] == counts[1][1]:
            return '1' if mode == 'oxygen' else '0'
        return counts[0][0]

    while len(report) > 1:
        bits_at_idx = [bits[bit_idx] for bits in report]

        counts = Counter(bits_at_idx).most_common()
        counts = counts if mode == 'oxygen' else counts[::-1]

        relevant_bit = bit_to_keep(counts)

        report = [bitlist for bitlist in report if bitlist[bit_idx] == relevant_bit]
        bit_idx += 1

    return report

def bit_list_to_decimal(bitlist: list[str]) -> int:
    bitstr = ''.join(bitlist)
    return int(bitstr, base=2)

def calculate(report: list[str]) -> int:
    bit_counts_gamma = count_bits(report, mode='gamma')
    bit_counts_epsilon = count_bits(report, mode='epsilon')

    gamma = bit_list_to_decimal(bit_counts_gamma)
    epsilon = bit_list_to_decimal(bit_counts_epsilon)

    return gamma * epsilon

def calculate_v2(report: list[str]) -> int:
    bit_counts_oxygen = filter_bits(report, mode='oxygen')
    bit_counts_co2 = filter_bits(report, mode='co2')

    oxygen = bit_list_to_decimal(bit_counts_oxygen)
    co2 = bit_list_to_decimal(bit_counts_co2)

    return oxygen * co2

if __name__=='__main__':
    test_report = format_input(test_input)
    report = format_input(read_input())

    # solution 1
    assert calculate(test_report) == 198
    print(calculate(report))

    # solution 2
    assert calculate_v2(test_report) == 230
    print(calculate_v2(report))
