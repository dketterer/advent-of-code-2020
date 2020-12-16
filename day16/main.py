import re
from dataclasses import dataclass, field
from typing import Tuple, List


@dataclass
class ExtendedRule:
    name: str
    pat1: Tuple[int, int]
    pat2: Tuple[int, int]
    pos: int = None
    pos_candidates: List[int] = field(default_factory=list)


def match_rules(rules, input):
    for lower, upper in rules:
        if lower <= input <= upper:
            return True
    return False


if __name__ == '__main__':
    with open('input.txt', 'r') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines]

    part1_rules = []
    extended_rules = []
    othertickets = []
    myticket = []
    rule_pat = re.compile(r"(.*): (\d+)-(\d+) or (\d+)-(\d+)$")

    state = 0
    for line in lines:
        if not line:
            state += 1
            continue
        if state == 0:
            match = rule_pat.match(line)
            part1_rules.append((int(match[2]), int(match[3])))
            part1_rules.append((int(match[4]), int(match[5])))
            extended_rules.append(
                ExtendedRule(match[1], (int(match[2]), int(match[3])), (int(match[4]), int(match[5]))))
        if state == 1 and not line.startswith('your ticket:'):
            myticket = [int(num) for num in line.split(',')]
        if state == 2 and not line.startswith('nearby tickets:'):
            othertickets.append([int(num) for num in line.split(',')])

    errors = []
    correct_tickets = []
    for ticket in othertickets:
        ticket_ok = True
        for ticket_field in ticket:
            if not match_rules(part1_rules, ticket_field):
                errors.append(ticket_field)
                ticket_ok = False
        if ticket_ok:
            correct_tickets.append(ticket)

    print(f'Part 1: {sum(errors)}')

    for ex_rule in extended_rules:
        for col in range(len(othertickets[0])):
            for other in correct_tickets + [myticket]:
                if not match_rules([ex_rule.pat1], other[col]) and not match_rules([ex_rule.pat2], other[col]):
                    break
            else:
                ex_rule.pos_candidates.append(col)

    changed = True
    while changed:
        changed = False
        for ex_rule in extended_rules:
            if len(ex_rule.pos_candidates) == 1:
                ex_rule.pos = ex_rule.pos_candidates[0]
                for ex_rule2 in extended_rules:
                    if ex_rule.pos in ex_rule2.pos_candidates:
                        ex_rule2.pos_candidates.remove(ex_rule.pos)
                        changed = True

    result_part2 = 1
    for ex_rule in extended_rules:
        if ex_rule.name.startswith('departure'):
            result_part2 *= myticket[ex_rule.pos]

    print(f'Part 2: {result_part2}')
