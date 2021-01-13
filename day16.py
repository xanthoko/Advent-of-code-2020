from typing import List
from math import prod

from utils import get_input_text


def get_input_list():
    input_text = get_input_text(16)

    rules, my_ticket_str, near_tickets_str = input_text.split('\n\n')
    rules = rules.split('\n')
    my_ticket_str = my_ticket_str.split('\n')[1]
    near_tickets_list = near_tickets_str.split('\n')[1:]

    return rules, my_ticket_str, near_tickets_list


def solve1(rules: List[str], my_ticket: str, near_tickets: List[str]):
    """Finds the ticket scanning error rate.

    The error rate is the sum of the values of the invalid fields per ticket.
    """
    valid_range_set = _find_total_valid_range(rules)

    invalid_fields_sum = 0
    for near_ticket in near_tickets:
        non_valid_fields = [
            int(field) for field in near_ticket.split(',')
            if int(field) not in valid_range_set
        ]
        invalid_fields_sum += sum(non_valid_fields)
    return invalid_fields_sum


def _find_total_valid_range(rules: List[str]):
    """Finds the combined valid range of the rules

    Rules are given with the given format: 'class': '0-2 or 10-23'

    Returns:
        set of integers: The combined valid range of all the rules
    """
    str_rule_ranges = [x.split(': ')[1] for x in rules]

    total_valid_range_set = set()
    for str_rule_range in str_rule_ranges:
        total_valid_range_set.update(_find_valid_range(str_rule_range))

    return total_valid_range_set


def _find_valid_range(rule_range: str):
    # rule_range example: '0-2 or 10-23'
    str_range1, str_range2 = rule_range.split(' or ')
    range1_low, range1_high = list(map(int, str_range1.split('-')))
    range2_low, range2_high = list(map(int, str_range2.split('-')))
    # the rule range must be inclusive, so increase higher limit by 1
    range1 = list(range(range1_low, range1_high + 1))
    range2 = list(range(range2_low, range2_high + 1))
    return range1 + range2


def solve2(rules: List[str], my_ticket: str, near_tickets: List[str]):
    valid_tickets = _get_valid_tickets(rules, near_tickets)
    range_per_rule = {
        x.split(': ')[0]: _find_valid_range(x.split(': ')[1])
        for x in rules
    }

    # split the tickets by columns
    number_of_cols = len(valid_tickets[0])
    cols = []
    for i in range(number_of_cols):
        cols.append([x[i] for x in valid_tickets])

    # candidates_per_rule = [{'rule': class, candidates: [0,2,3]}, ...]
    candidates_per_rule = []
    for rule_name, rule_range in range_per_rule.items():
        candidate_columns = []
        for ind, col in enumerate(cols):
            elements_in_range = [x for x in col if x in rule_range]
            # if the all the elements of the column are inside the
            # range, then this col is a candidate for the rule
            if len(elements_in_range) == len(col):
                candidate_columns.append(ind)

        candidates_per_rule.append({
            'rule': rule_name,
            'candidates': candidate_columns
        })

    rule_index_map = {}
    sorted_candidates_per_rule = sorted(candidates_per_rule,
                                        key=lambda x: len(x['candidates']))
    # We know that each field is represented by EXACTLY ONE column
    # So, at all times there must be a rule that has ONLY ONE candidate. The process
    # is that we start from the rule that has one candidate and then proceed to the
    # one with two candidates, three, etc. When removing each time the used index
    # there will be only one candidate left each time
    # For example: 'class' rule has cand=[2] and 'row' rule cand=[2,4]. When we
    # remove the 2 cand from class the only remaining cand in row is 4.
    used_col_indexes = set()
    for sorted_candidates in sorted_candidates_per_rule:
        candidates_without_used = [
            x for x in sorted_candidates['candidates'] if x not in used_col_indexes
        ]
        matching_candidate = candidates_without_used[0]
        used_col_indexes.add(matching_candidate)
        rule_index_map[sorted_candidates['rule']] = matching_candidate

    wanted_cols = [
        v for k, v in rule_index_map.items() if k.startswith('departure')
    ]
    my_fields = list(map(int, my_ticket.split(',')))
    my_wanted_fields = [my_fields[x] for x in wanted_cols]

    return prod(my_wanted_fields)


def _get_valid_tickets(rules, near_tickets):
    valid_tickets = []
    valid_range_set = _find_total_valid_range(rules)

    for near_ticket in near_tickets:
        non_valid_fields = [
            int(field) for field in near_ticket.split(',')
            if int(field) not in valid_range_set
        ]
        if not non_valid_fields:
            # append the ticket with its fields converted to int
            valid_tickets.append(list(map(int, near_ticket.split(','))))

    return valid_tickets


def solve():
    rules, my_ticket, near_tickets = get_input_list()

    # PART 1
    invalid_fields_sum = solve1(rules, my_ticket, near_tickets)
    print(f'[PART 1] The sum is {invalid_fields_sum}')

    # PART 2
    product = solve2(rules, my_ticket, near_tickets)
    print(f'[PART 2] The product of the fields is {product}')


if __name__ == '__main__':
    solve()
