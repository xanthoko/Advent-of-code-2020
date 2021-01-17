from typing import List
from itertools import product

from utils import get_input_text


def get_input():
    input_text = get_input_text(19)

    rules_text, messages_text = input_text.split('\n\n')
    rules_str_list = rules_text.split('\n')
    messages_list = messages_text.split('\n')
    rules_dict = {}
    for rule_str in rules_str_list:
        rule_number, rule = rule_str.split(': ')
        rules_dict[int(rule_number)] = rule
    return rules_dict, messages_list


def solve1(rules: dict, messages: List[str]):
    valid_messages = 0
    for message in messages:
        valid_messages += consume(rules, message, 0) == len(message)
    return valid_messages


def _unpack_rule(rules: dict, rule_index: int):
    """My solution. Produces a list of possible sequences for the given rule.

    It is not used because a message is valid if it is inside the valid sequences
    produced and this procedure is really slow.
    """
    rule = rules[rule_index]
    if rule == '"a"':
        return ['a']
    elif rule == '"b"':
        return ['b']

    rule_valid_seqs = []
    parts_of_rule = rule.split(' | ')
    for part_of_rule in parts_of_rule:
        sub_rules = part_of_rule.split(' ')
        sub_rules_list = [_unpack_rule(rules, int(x)) for x in sub_rules]
        combined_text_list = list(product(*sub_rules_list))
        joined_combined_texts = [''.join(x) for x in combined_text_list]
        rule_valid_seqs.extend(joined_combined_texts)

    return rule_valid_seqs


def consume(rules: List[str], message: str, rule_number: int):
    """Solution credits to https://www.youtube.com/watch?v=OxDp11u-GUo&t=945s

    Calculates the number of charactes that the given rule can consume from the
    given message. If this number is equal to the length of the message, then the
    message is considered valid.
    """
    rule = rules[rule_number]

    if rule[0] == '"':
        # terminal symbol
        rule = rule.strip('"')
        if message.startswith(rule):
            return 1
        return -1

    for opt in rule.split(' | '):
        acc = 0
        for rn in opt.split(' '):
            rn = int(rn)
            ret = consume(rules, message[acc:], rn)
            if ret == -1:
                acc = -1
                break
            acc += ret
        if acc != -1:
            return acc
    return -1


def solve2(rules: dict, messages: List[str]):
    # update rules
    rules[8] = '42 | 42 8'
    rules[11] = '42 31 | 42 11 31'

    valid_messages = 0
    for message in messages:
        valid_messages += len(message) in consume2(rules, message, 0)
    return valid_messages


def consume2(rules: List[str], message: str, rule_number: int):
    """Solution credits to https://www.youtube.com/watch?v=OxDp11u-GUo&t=945s"""
    rule = rules[rule_number]

    if rule[0] == '"':
        rule = rule.strip('"')
        if message.startswith(rule):
            return [len(rule)]
        return []

    bret = []
    for opt in rule.split(' | '):
        possible_accs = [0]
        for rn in opt.split(' '):
            nacc = []
            rn = int(rn)
            for acc in possible_accs:
                consumes = consume2(rules, message[acc:], rn)
                for c in consumes:
                    nacc.append(c + acc)
            possible_accs = nacc
        bret += possible_accs
    return bret


def solve():
    rules, messages = get_input()

    # PART 1
    rule_0_msgs_1 = solve1(rules, messages)
    print(f'[PART 1] {rule_0_msgs_1} messages match rule 0')

    # PART 2
    rule_0_msgs_2 = solve2(rules, messages)
    print(f'[PART 2] {rule_0_msgs_2} messages match rule 0')


if __name__ == '__main__':
    solve()
