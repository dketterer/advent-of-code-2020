import re
from copy import copy


def parse_input(lines):
    pat_rule = re.compile(r"(\d+): (.+)")

    rules = {}
    state = 0
    inputs = []
    for line in lines:
        if not line:
            state = 1
            continue
        if not state:
            m = pat_rule.match(line)
            rule = m[2].replace('\"', '')
            if '|' in rule:
                rules[int(m[1])] = f'( {rule} )'
            else:
                rules[int(m[1])] = f'{rule}'
        else:
            inputs.append(line)

    return rules, inputs


def parse_deterministic(rules):
    regex = rules[0]
    next_regex = ""
    non_terminal = True
    while non_terminal:
        non_terminal = False
        for part in regex.split(' '):
            if part in ['(', ')', '|']:
                next_regex += f' {part}'
            if part.isdigit():
                next_regex += f' {rules[int(part)]}'
                non_terminal = True
            if part.isalpha():
                next_regex += f' {part}'

        regex = next_regex
        next_regex = ""

    regex = regex.replace(' ', '')
    regex = f'^{regex}$'
    return regex


def parse_with_loop(rules):
    regex = rules[0]
    next_regex = ""
    for i in range(26):
        for part in regex.split(' '):
            if part in ['(', ')', '|']:
                next_regex += f' {part}'
            elif part.isdigit():
                next_regex += f' {rules[int(part)]}'
            else:
                next_regex += f' {part}'

        if i == 15:
            rules[8] = "( 42 | 42 .* )"
            rules[11] = "( 42 31 | 42 .* 31 )"

        regex = next_regex
        next_regex = ""

    regex = regex.replace(' ', '')
    regex = f'^{regex}$'
    return regex


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    rules1, inputs = parse_input(lines)
    rules2 = copy(rules1)

    rules2[8] = "( 42 | 42 8 )"
    rules2[11] = "( 42 31 | 42 11 31 )"

    regex1 = parse_deterministic(rules1)
    regex2 = parse_with_loop(rules2)

    lang1 = re.compile(regex1)
    lang2 = re.compile(regex2)

    print(f'Part 1: {sum([bool(lang1.match(inp)) for inp in inputs])}')
    print(f'Part 2: {sum([bool(lang2.match(inp)) for inp in inputs])}')
