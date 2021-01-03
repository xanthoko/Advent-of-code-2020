from collections import Counter
from functools import reduce

from utils import get_input_text_from_url


def get_input_list():
    """Returns list of answers per group"""
    input_text = get_input_text_from_url(6)
    input_text = input_text
    # split answers per group
    by_group_anwers = input_text.split('\n\n')
    return by_group_anwers


def get_sum_of_counts_1(by_group_answers):
    """Calculates the sum for part 1.

    In each group we must find the number of questions that AT LEAST ONE person of
    the group answered 'yes'.
    For example if the answers per group were:

    abc

    ab
    ac

    In the first group there is only 1 person so every answer will be count = 3
    In the second group the answers with at least one 'yes' are a b and c so
    count = 3
    and sum of count: 3 + 3 = 6.

    Args:
        by_group_answers (list of strings)
    """
    sum_of_counts = 0
    for group_answers in by_group_answers:
        joined_group_answers = group_answers.replace('\n', '')
        # the set removes the duplicates
        count = len(set(joined_group_answers))
        sum_of_counts += count

    return sum_of_counts


def get_sum_of_counts_21(by_group_answers):
    """Calculates the sum for part 2 (Method 1).

    In each group we must find the number of questions that ALL the people of
    the group answered 'yes'.
    For example if the answers per group were:

    abc

    ab
    ac

    In the first group there is only 1 person so every answer will be count = 3
    In the second group the common answer of the 2 people is 'a' so count = 1
    and sum of count: 3 + 1 = 4.

    In this method lets say we have by_person_answers = ['ab', 'ac', 'ad'] we use
    reduce to apply a function that keeps only the common characters of the strings.
    This fuction is set(a) & set(b).

    Args:
        by_group_answers (list of strings)
    """
    sum_of_counts = 0
    for group_answers in by_group_answers:
        by_person_answers = group_answers.split('\n')
        count = reduce(lambda x, y: set(x) & set(y), by_person_answers)
        sum_of_counts += len(count)
    return sum_of_counts


def get_sum_of_counts_22(by_group_answers):
    """Calculates the sum for part 2 (Method 2).

    If an answer is in every persons list the occurancies of this character must
    be equal to the number of the people answered.
    So we count the occurancies of the characters in the joined string.

    Args:
        by_group_answers (list of strings)
    """
    sum_of_counts = 0
    for group_answers in by_group_answers:
        by_person_answers = group_answers.split('\n')
        joined_answers = group_answers.replace('\n', '')
        c = Counter(joined_answers)
        for key in c:
            if c[key] == len(by_person_answers):
                sum_of_counts += 1
    return sum_of_counts


def solve():
    input_list = get_input_list()

    # PART 1
    sum_of_counts_1 = get_sum_of_counts_1(input_list)
    print(f'[PART 1] Sum of counts is {sum_of_counts_1}')

    # PART 2
    sum_of_counts_2 = get_sum_of_counts_21(input_list)
    print(f'[PART 2] Sum of counts is {sum_of_counts_2}')


if __name__ == '__main__':
    solve()
