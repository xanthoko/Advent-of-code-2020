import re

from utils import get_input_text_from_url


def get_input_passports():
    """
    Returns:
        list of strings: The list of passport strings
    """
    input_text = get_input_text_from_url(4)
    passports = input_text.split('\n\n')

    return passports


def get_valid_passports(passports, part):
    """Finds the number of valid passport.

    A passport is valid if it contains the following required fields
       - byr (Birth Year)
       - iyr (Issue Year)
       - eyr (Expiration Year)
       - hgt (Height)
       - hcl (Hair Color)
       - ecl (Eye Color)
       - pid (Passport ID)

    The cid (Country ID) is considered optional.

    Args:
        passport (list of strings)
    """
    required_fields = set(['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid'])

    valid_passport_counter = 0
    for passport in passports:
        # split passport string to \n and ' ' to get the data in a list
        passport_str_data = re.split('\n| ', passport)
        # remove empty elemets
        passport_str_data = filter(None, passport_str_data)

        passport_data = {
            x.split(':')[0]: x.split(':')[1]
            for x in passport_str_data
        }
        # remove optional field
        try:
            passport_data.pop('cid')
        except KeyError:
            pass
        passport_fields = set(passport_data.keys())

        required_fields_present = passport_fields == required_fields
        # if PART 1 -> is_data_valid = True
        if not required_fields_present:
            continue

        if part == 1:
            is_data_valid = True
        else:
            is_data_valid = _validate_passport_data(passport_data)

        valid_passport_counter += is_data_valid

    return valid_passport_counter


def _validate_passport_data(passport_data):
    try:
        # -------- birth year --------
        birth_year = passport_data['byr']
        int_birth_year = int(birth_year)
        assert 1920 <= int_birth_year <= 2002

        # -------- issue year --------
        issue_year = passport_data['iyr']
        int_issue_year = int(issue_year)
        assert 2010 <= int_issue_year <= 2020

        # -------- expiration year --------
        expiration_year = passport_data['eyr']
        int_expiration_year = int(expiration_year)
        assert 2020 <= int_expiration_year <= 2030

        # -------- height --------
        height = passport_data['hgt']
        hgt_number = int(height[:-2])
        hgt_unit = height[-2:]
        if hgt_unit == 'cm':
            assert 150 <= hgt_number <= 193
        elif hgt_unit == 'in':
            assert 59 <= hgt_number <= 76
        else:
            raise ValueError

        # -------- hair color --------
        hair_color = passport_data['hcl']
        assert re.match('^#[a-f0-9]{6}$', hair_color)

        # -------- eye color --------
        eye_color = passport_data['ecl']
        assert eye_color in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']

        # -------- passport id --------
        passport_id = passport_data['pid']
        assert len(passport_id) == 9
        # making it an int removes the leading zeroes
        int(passport_id)

        return True
    except (ValueError, AssertionError, KeyError):
        # The KeyError should never be thrown as the required field should be
        # present
        return False


def solve():
    passports = get_input_passports()

    # PART 1
    valid_passports = get_valid_passports(passports, 1)
    print(f'[PART 1] {valid_passports} valid passports')

    # PART 2
    valid_passports = get_valid_passports(passports, 2)
    print(f'[PART 2] {valid_passports} valid passports')


if __name__ == '__main__':
    a = solve()
