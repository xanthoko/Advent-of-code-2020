from typing import List

from utils import get_input_text


def get_input_list():
    input_text = get_input_text(10)
    str_input_list = input_text.split('\n')
    input_list = list(map(int, str_input_list))
    return input_list


def solve_1(joltages: List[int]):
    """Calculates the number of 1-joltage difference multiplied by the number
    of 3-jolt differences.

    Sorts the list of joltages and store the difference of the consecutive joltages
    in dictionary. The product of diffs[1] * diffs[3] is returned.
    """
    joltages.sort()  # TimSort - O(n logn)
    # the device's built in adapter has 3 more joltages than the max in the list
    device_adapter_joltage = joltages[-1] + 3
    joltages.append(device_adapter_joltage)

    # the differences can be 1,2 or 3 joltages
    diffs = {1: 0, 2: 0, 3: 0}

    previous = 0
    # O(n)
    for joltage in joltages:
        diff = joltage - previous
        diffs[diff] += 1
        previous = joltage

    return diffs[3] * diffs[1]


def solve_2(joltages: List[int]):
    """Calculates the number of ways the adapters can connect with each other."""
    joltages.sort()
    joltages = [0] + joltages
    return _get_number_of_orders(joltages)


def _get_number_of_orders(joltages: List[int]):
    """The iterative method that calculates the number of ways to connect the
    adapters

    For example if the adapters at the end of the list were 10, 11, 12, 15.
    We know the 15 has only 1 way to connect with the max (15 + 3), so
    orders[15] = 1.
    Next 12 can only connect to 12 so orders[12] = orders[15] = 1. In the same
    way order[11] = order[12] = 1. However, 10 can connect to both 11 and 12
    so order[10] = order[11] + order[12] = 1 + 1 = 2. The iteration continues till
    the order[0] is calculated.
    """
    last_joltage = joltages[-1]
    cache = {last_joltage: 1}
    index = len(joltages) - 2  # second from last
    while index > -1:
        joltage = joltages[index]
        # find the joltages that can connect to the current one
        conn_index = index + 1
        conn_orders = 0
        while conn_index < len(joltages):
            con_joltage = joltages[conn_index]
            # check if valid for connection
            if con_joltage - joltage < 4:
                # we know con_joltage is a valid key for cache because we have
                # already calculated it in the previous steps
                conn_orders += cache[con_joltage]
                conn_index += 1
            else:
                break
        cache[joltage] = conn_orders

        # update index
        index -= 1
    return conn_orders


def solve():
    joltages = get_input_list()

    # PART 1
    multiplied = solve_1(joltages)
    print(f'[PART 1] The product is {multiplied}')

    # PART 2
    arrange_orders = solve_2(joltages)
    print(f'[PART 2] The number of ways to arrange is {arrange_orders}')


if __name__ == '__main__':
    solve()
