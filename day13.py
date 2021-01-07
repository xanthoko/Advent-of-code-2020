from utils import get_input_text


def get_input_lists():
    input_text = get_input_text(13)
    arrival_time, bus_ids_str = input_text.split('\n')
    return int(arrival_time), bus_ids_str


def solve1(arrival_time: int, bus_ids_str: str):
    """Finds the earliest bus you can take upon arrival and the waiting time.

    The waiting time is found by x - (arrival_time % x) where x is the period
    of the bus.
    (arrival_time % x) finds the minutes since the last bus of the line arrived.
    Let's say x = 5 and arrival_time = 9. (arrival_time % x) = 4 minutes since
    the last bus arrived. So we have to wait 5 - 4 = 1 minutes.
    """
    int_bus_ids = [int(x) for x in bus_ids_str.split(',') if x != 'x']
    waiting_times = [x - (arrival_time % x) for x in int_bus_ids]

    min_waiting_time = min(waiting_times)
    # the index of the min value in waiting_times
    min_waiting_bus_index = waiting_times.index(min_waiting_time)
    min_waiting_bus_id = int_bus_ids[min_waiting_bus_index]

    return min_waiting_time * min_waiting_bus_id


def solve2(bus_ids_str: str):
    """Finds the earliest timestamp such that all of the listed bus IDs depart
    at offsets matching their positions in the given list.

    BIG THANKS to this guy
    https://math.stackexchange.com/questions/2218763/how-to-find-lcm-of-two-numbers-when-one-starts-with-an-offset
    """
    bus_ids = bus_ids_str.split(',')
    # active_bus_lines = {bus_id: index_in_list}
    active_bus_lines = {int(x): ind for ind, x in enumerate(bus_ids) if x != 'x'}
    period = None
    phase = None
    for bus_id, index in active_bus_lines.items():
        if not period:
            period = bus_id
            phase = 0
        else:
            period_b = bus_id
            phase_b = -index % bus_id
            period, phase = _combine_phased_rotations(period, phase, period_b,
                                                      phase_b)
    return phase


def _combine_phased_rotations(a_period, a_phase, b_period, b_phase):
    """Combine two phased rotations into a single phased rotation

    Returns: combined_period, combined_phase

    The combined rotation is at its reference point if and only if both a and b
    are at their reference points.
    """
    gcd, s, t = _extended_gcd(a_period, b_period)
    phase_difference = a_phase - b_phase
    pd_mult, pd_remainder = divmod(phase_difference, gcd)
    if pd_remainder:
        raise ValueError("Rotation reference points never synchronize.")

    combined_period = a_period // gcd * b_period
    combined_phase = (a_phase - s * pd_mult * a_period) % combined_period
    return combined_period, combined_phase


def _extended_gcd(a, b):
    """Extended Greatest Common Divisor Algorithm

    Returns:
        gcd: The greatest common divisor of a and b.
        s, t: Coefficients such that s*a + t*b = gcd

    Reference:
        https://en.wikipedia.org/wiki/Extended_Euclidean_algorithm#Pseudocode
    """
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r:
        quotient, remainder = divmod(old_r, r)
        old_r, r = r, remainder
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t

    return old_r, old_s, old_t


def solve():
    arrival_time, bus_ids_str = get_input_lists()

    # PART 1
    multiplied_value_1 = solve1(arrival_time, bus_ids_str)
    print(f'[PART 1] Multiplied value is {multiplied_value_1}')

    # PART 2
    wanted_timestamp = solve2(bus_ids_str)
    print(f'[PART 2] Wanted timestamp is {wanted_timestamp}')


if __name__ == '__main__':
    solve()
