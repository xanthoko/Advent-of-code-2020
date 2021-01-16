import re
from math import prod
from typing import List

from utils import get_input_text


def get_input_list():
    input_text = get_input_text(18)
    return input_text.split('\n')


def solve1(expressions: List[str]):
    """Find the sums of the evaluations of the given expressions.

    The math rules are:
        - addition and multiplication have the same precedence
        - parentheses have the highest precedence
    """
    sum_of_values = 0
    for expression in expressions:
        sum_of_values += _evaluate_expression_1(expression)

    return sum_of_values


def _evaluate_expression_1(expression: str):
    """Returns the integer evaluation of the expression."""
    parentheses_str = _find_parentheses(expression)
    while parentheses_str is not None:
        inside_parenthesis = parentheses_str[1:-1]  # remove '(', ')'
        value = _evaluate_expression_1(inside_parenthesis)
        expression = expression.replace(parentheses_str, str(value))
        parentheses_str = _find_parentheses(expression)

    # every parentheses in the expression is replaces by its numeric value
    symbols = expression.split(' ')
    # symbols is a list of numbers and operators
    operator = ''
    value = 0
    for symbol in symbols:
        try:
            number = int(symbol)
            if operator == '+':
                value += number
            elif operator == '*':
                value *= number
            else:  # operator == '', first numebr
                value = number
        except ValueError:
            operator = symbol
    return value


def solve2(expressions: List[str]):
    """Find the sums of the evaluations of the given expressions.

    The math rules are:
        - addition has higher precedence than multiplication
        - parentheses have the highest precedence
    """
    sum_of_values = 0
    for expression in expressions:
        sum_of_values += _evaluate_expression_2(expression)
    return sum_of_values


def _evaluate_expression_2(expression: str):
    """Returns the integer evaluation of the expression."""
    # replace every parentheses in the expression with its numeric value
    parentheses_str = _find_parentheses(expression)
    while parentheses_str is not None:
        inside_parenthesis = parentheses_str[1:-1]  # remove '(', ')'
        value = _evaluate_expression_2(inside_parenthesis)
        expression = expression.replace(parentheses_str, str(value))
        parentheses_str = _find_parentheses(expression)

    # replace additions with its numeric sum value
    addition_search = re.search('[0-9]+ \+ [0-9]+', expression)
    while addition_search is not None:
        addition_str = addition_search.group()
        num1, num2 = addition_str.split(' + ')
        int_sum = int(num1) + int(num2)
        expression = expression.replace(addition_str, str(int_sum), 1)
        addition_search = re.search('[0-9]+ \+ [0-9]+', expression)

    # only left with multiplications
    numbers = expression.split(' * ')
    int_numbers = list(map(int, numbers))

    return prod(int_numbers)


def _find_parentheses(expression):
    """Returns the substring of the expression that has a parentheses."""
    pareth_open_pos = expression.find('(')
    if pareth_open_pos != -1:
        # parentheses found
        pos = pareth_open_pos + 1
        counter = 1
        # everytime a parentheses opens the counter is increased by 1
        # everytime a parentheses closes the counter is decreased by 1
        # when counter is 0 the initial parentheses is complete
        while counter > 0:
            char = expression[pos]
            if char == '(':
                counter += 1
            elif char == ')':
                counter -= 1
            pos += 1
        return expression[pareth_open_pos:pos]


def solve():
    expressions = get_input_list()

    # PART 1
    sum_of_values_1 = solve1(expressions)
    print(f'[PART 1] The sum is {sum_of_values_1}')

    # PART 2
    sum_of_values_2 = solve2(expressions)
    print(f'[PART 2] The sum is {sum_of_values_2}')


if __name__ == '__main__':
    solve()
