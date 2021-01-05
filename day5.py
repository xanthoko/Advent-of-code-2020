from utils import get_input_text


def get_input_list():
    input_text = get_input_text(5)
    return input_text.split('\n')


def get_all_seat_ids(boarding_passes):
    """Each seat is specified by a string like this FBFBBFFRLR

    The first 7 characters identify the row and the last 3 the column.
    'F' is for Front-Lower half and 'B' is for Back-Upper half.
    'L' is for Left-Lower half and 'R' if for Right-Upper half.

    Args:
        boarding_passes (list of strings)
    Returns:
        list of integers: The seat ids
    """
    seat_ids = []

    # O(n*m) where n is the number of boarding passes and m the length of the
    # row idenitifiers
    for boarding_pass in boarding_passes:
        row_identifier = boarding_pass[:7]
        row = _get_index_from_identifiers(row_identifier, {'F': '0', 'B': '1'})

        col_identifier = boarding_pass[7:]
        col = _get_index_from_identifiers(col_identifier, {'L': '0', 'R': '1'})

        seat_id = row * 8 + col
        seat_ids.append(seat_id)

    return seat_ids


def _get_index_from_identifiers(idenitifier, replace_map):
    """Returns the integer id of the seat described by the identifier.

    The row or the column can be represented by a binary number where
    0 is the lower half and 1 is the upper half.

    Args:
        identifier (string): Identifier like 'FBFBBFF' or 'LRL'
        replace_map (dictionary): Defines the replacement in the identifier
    """
    binary_identifier = idenitifier
    for key, value in replace_map.items():
        binary_identifier = binary_identifier.replace(key, value)

    return int(binary_identifier, 2)


def find_my_seat_id(seat_ids):
    """Finds my seat id which is missing from the given ids.

    First sort the ids in ascending order. We know that our left and right seat
    is not missing so the area where our id is will be like this
    100 101 (102) 103 104 , where 102 is our id
    So we can find my id if we find the id which does not equal to the last + 1.
    In the example above this id would be 103 and my id will be 102.

    Args:
        seat_ids (list of integers)
    Returns:
        integer: My seat id
    """
    seat_ids.sort()
    last = seat_ids[0] - 1

    for seat_id in seat_ids:
        if seat_id != (last + 1):
            return seat_id - 1
        last = seat_id


def solve():
    input_list = get_input_list()
    seat_ids = get_all_seat_ids(input_list)

    # PART 1
    highest_seat_id = max(seat_ids)
    print(f'[PART 1] Highest seat ID is {highest_seat_id}')

    # PART 2
    my_seat_id = find_my_seat_id(seat_ids)
    print(f'[PART 2] My seat ID is {my_seat_id}')


if __name__ == '__main__':
    solve()
