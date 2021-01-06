from typing import List

from utils import get_input_text, get_example_input_text


def get_input_list():
    input_text = get_input_text(12)
    # input_text = get_example_input_text()
    return input_text.split('\n')


def solve1(instructions: List[str]):
    """Finds the Manhattan distance of the ship after following the instructions.

    The Manhattan distance is the sum of steps an object took from the starting
    position, in the horizontal and the vertical axis.

    | - - - - B      In this case the manhattan distance from A to B is 3
    |         |      1 step right , 2 steps up
    | - - - - |
    |         |
    A - - - - |
    """
    x = 0
    y = 0
    direction_map = {'N': 0, 'E': 1, 'S': 2, 'W': 3}
    starting_direction = 'E'
    direction = direction_map[starting_direction]

    for instruction in instructions:
        action = instruction[:1]
        value = int(instruction[1:])

        if action == 'F':
            x, y = _update_position(direction, value, x, y)
        elif action in ['R', 'L']:
            direction = _update_direction(direction, action, value)
        else:
            # action = N, E, S, W
            int_direction = direction_map[action]
            x, y = _update_position(int_direction, value, x, y)

    return abs(x) + abs(y)


def _update_position(direction: int, value: int, x: int, y: int):
    """Updates the values of x and y accoring to the current direction"""
    if direction == 0:
        y -= value
    elif direction == 1:
        x += value
    elif direction == 2:
        y += value
    elif direction == 3:
        x -= value

    return x, y


def _update_direction(direction: int, rotation_dir: str, value: int):
    """The rotation degrees are always a multiply of 90.

        0       If the rotation degrees are 270 and the rot_dir is R
                the new direction will be 1 + 3 = 4 % 4 = 0 (North)
    3     ->1

        2
    """
    steps = value // 90
    if rotation_dir == 'L':
        # counter clockwise rotation
        steps *= -1
    direction = direction + steps
    direction = direction % 4
    return direction


def solve2(instructions: List[str]):
    """Finds the manhattan distance of the ship after following the instructions.

    This time some instructions refer to the movement of the waypoint.
    """
    ship_x = 0
    ship_y = 0
    # coordinates of the waypoint according to the ship
    d_x = 10
    d_y = -1
    direction_map = {'N': 0, 'E': 1, 'S': 2, 'W': 3}

    for instruction in instructions:
        action = instruction[:1]
        value = int(instruction[1:])

        if action in ['L', 'R']:
            d_x, d_y = _rotate_waypoint(action, value, d_x, d_y)
        elif action == 'F':
            ship_x += d_x * value
            ship_y += d_y * value
        else:
            # action = N, E, S, W
            int_direction = direction_map[action]
            d_x, d_y = _update_position(int_direction, value, d_x, d_y)

    return abs(ship_x) + abs(ship_y)


def _rotate_waypoint(action: int, value: int, d_x: int, d_y: int):
    """Rotates the waypoint in relation to the ship.
    Ship is X, waypoint is o

            o   R1                  The left rotation steps are equal to
        X       ->      X           4 - {right rotation steps}
                            o
                R2
                ->      X
                    o
                R3  o
                ->      X
    """
    steps = value // 90
    if action == 'L':
        steps = 4 - steps

    if steps == 1:
        d_x, d_y = -d_y, d_x
    elif steps == 2:
        d_x *= -1
        d_y *= -1
    elif steps == 3:
        d_x, d_y = d_y, -d_x

    return d_x, d_y


def solve():
    instructions = get_input_list()

    # PART 1
    manhattan_distance_1 = solve1(instructions)
    print(f'[PART 1] Manhattan distance is {manhattan_distance_1}')

    # PART 2
    manhattan_distance_2 = solve2(instructions)
    print(f'[PART 1] Manhattan distance is {manhattan_distance_2}')


if __name__ == '__main__':
    solve()
