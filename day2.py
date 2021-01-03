from utils import get_input_text_from_url


def get_input_list():
    """Returns a list of dictionaries in the following format
    [
        {'policy': '', 'password': ''}, ...
    ]
    """
    input_text = get_input_text_from_url(2)
    splited_str_input_list = input_text.split('\n')
    input_list = [{
        'policy': x.split(':')[0],
        'password': x.split(':')[1].strip()
    } for x in splited_str_input_list]

    return input_list


def get_number_of_valid_passwords_1(input_list):
    """Solves the number of occurancies problem.

    Example for policies:
        1-3 a: ajkads (Valid - has 2 'a')
        2-5 c: asdcsa (Invalid - has 1 'c')
        3-6 d: dddddkmdd (Invalid - has 7 'd')

    Args:
        input_list (list of dictionaries): Each dictionary has 'policy' and
            'password' keys.
    """
    number_of_valid_passwords = 0
    for pass_dict in input_list:
        policy = pass_dict['policy']
        password = pass_dict['password']

        valid_range, spotlight_char = policy.split(' ')
        # valid_range = '1-3'
        valid_range = list(map(int, valid_range.split('-')))
        # increase the upper limit so that it is included in the range
        valid_range[1] = valid_range[1] + 1

        occurancies_of_char_in_pass = password.count(spotlight_char)
        is_valid = occurancies_of_char_in_pass in range(*valid_range)
        # int(True) = 1 and int(False) = 0
        number_of_valid_passwords += int(is_valid)

    return number_of_valid_passwords


def get_number_of_valid_passwords_2(input_list):
    """Solves the indexes problem.

    Example for policies:
        1-3 a: abcde is valid: position 1 contains a and position 3 does not.
        1-3 b: cdefg is invalid: neither position 1 nor position 3 contains b.
        2-9 c: ccccccccc is invalid: both position 2 and position 9 contain c.

    Args:
        input_list (list of dictionaries): Each dictionary has 'policy' and
            'password' keys.
    """
    number_of_valid_passwords = 0
    for pass_data in input_list:
        policy = pass_data['policy']
        password = pass_data['password']

        indexes, spotlight_char = policy.split(' ')
        indexes = list(map(int, indexes.split('-')))

        # AOC was 1-indexed
        cond1 = password[indexes[0] - 1] == spotlight_char
        cond2 = password[indexes[1] - 1] == spotlight_char

        # only 1 condition must be True
        if int(cond1) + int(cond2) == 1:
            number_of_valid_passwords += 1

    return number_of_valid_passwords


def solve():
    input_list = get_input_list()

    # part 1
    valid_passwords = get_number_of_valid_passwords_1(input_list)
    print(f'{valid_passwords} valid passwords')

    # part 2
    valid_passwords = get_number_of_valid_passwords_2(input_list)
    print(f'{valid_passwords} valid passwords')


if __name__ == '__main__':
    solve()
