from utils import get_input_text_from_url


def get_input_list():
    input_text = get_input_text_from_url(8)
    return input_text.split('\n')


def solve_1(instructions):
    """Get the value of the accumulator right before the program would run
    an instruction for the second time.

    Args:
        instructions (list of strings): A list of instructions. Each instruction
            contains an operator and an argument.
    Returns:
        dictionary: The value of the accumulator and if the program terminated
    """
    accumulator = 0
    # has a flag wether the line of the program has been executed
    book = {x: False for x in range(len(instructions))}

    instruction_index = 0
    terminated = False
    while True:
        try:
            instruction = instructions[instruction_index]
        except IndexError:
            # program terminated
            terminated = True
            break

        operation, argument = instruction.split(' ')
        argument = int(argument)

        # check if the insturction is already been executed
        is_executed = book[instruction_index]
        if is_executed:
            break

        # update the instructions book
        book[instruction_index] = True

        if operation == 'nop':
            instruction_index += 1
        elif operation == 'acc':
            accumulator += argument
            instruction_index += 1
        elif operation == 'jmp':
            instruction_index += argument

    return {'accumulator': accumulator, 'terminated': terminated}


def solve_2(instructions):
    """Get the value of the accumulator at the end of the program after replacing
    exactly one jmp (to nop) or nop (to jmp).

    In every step, we replace a key instruction (i.e 'jmp' or 'nop'), creating a new
    set of instructions. This new set is then given to solve_1. If the program
    terimenates we return the accumulator value returned.

    Args:
        instructions (list of strings): A list of instructions. Each instruction
            contains an operator and an argument.
    Returns:
        integer: The value of the accumulator
    """
    for ind, instruction in enumerate(instructions):
        operation, _ = instruction.split(' ')
        if operation == 'acc':
            continue

        # create the new set of instructions
        copy_instructions = instructions.copy()
        replaced_instruction = _replace_operation_of_instruction(instruction)
        copy_instructions[ind] = replaced_instruction

        # feed the new set to solve_1 to check if the replaced instruction allows
        # the program to terminate
        result = solve_1(copy_instructions)
        if result['terminated']:
            return result['accumulator']


def _replace_operation_of_instruction(instruction):
    """Replaces 'nop' with 'jmp' and vice versa."""
    operation, argument = instruction.split(' ')
    if operation == 'nop':
        new_operation = 'jmp'
    elif operation == 'jmp':
        new_operation = 'nop'
    else:
        new_operation = operation
    return f'{new_operation} {argument}'


def solve():
    instructions = get_input_list()

    # PART 1
    solve_result_1 = solve_1(instructions)
    print(f"[PART 1] Accumulator is {solve_result_1['accumulator']}")

    # PART 2
    accumulator_2 = solve_2(instructions)
    print(f'[PART 2] Accumulator is {accumulator_2}')


if __name__ == '__main__':
    solve()
