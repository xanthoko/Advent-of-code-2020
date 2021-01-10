from typing import List
from itertools import product

from utils import get_input_text


def get_input_list():
    input_text = get_input_text(14)
    return input_text.split('\n')


def solve1(program_lines: List[str]):
    memory = {}

    mask = ''
    for program_line in program_lines:
        if program_line.startswith('mask'):
            _, mask_value = program_line.split(' = ')
            mask = mask_value
        else:
            position_str, mem_value = program_line.split(' = ')
            # update value according to mask
            binary_mem_value = bin(int(mem_value))[2:]  # '0b003' -> '003'
            # pad zeros to make its length 36
            binary_mem_value = binary_mem_value.zfill(36)
            binary_mem_value = _replace_bits_from_mask(binary_mem_value, mask, 'X')

            int_mem_value = int(binary_mem_value, 2)
            # update memory list
            mem_index = int(position_str[4:].split(']')[0])  # mem[8] -> 8
            memory[mem_index] = int_mem_value

    return sum(memory.values())


def solve2(program_lines: List[str]):
    memory = {}
    mask = ''

    for program_line in program_lines:
        if program_line.startswith('mask'):
            _, mask_value = program_line.split(' = ')
            mask = mask_value
        else:
            # programm line = 'mem[8] = 11'
            position_str, mem_value = program_line.split(' = ')
            address = int(position_str[4:].split(']')[0])  # mem[8] -> 8
            binary_address = bin(address)[2:]
            binary_address = binary_address.zfill(36)
            binary_address = _replace_bits_from_mask(binary_address, mask, '0')

            indexes_of_x = [
                pos for pos, char in enumerate(binary_address) if char == 'X'
            ]
            # if for example there are 2 X in binary address we will have 2^2 = 4
            # combinations -> [[0,0], [0,1], [1,0], [1,1]] to replace in the address
            binary_combs = list(
                map(list, product(['0', '1'], repeat=len(indexes_of_x))))

            addresses = []
            for comb in binary_combs:
                ba_copy = binary_address
                for index, value in zip(indexes_of_x, comb):
                    ba_copy = _replace_at(ba_copy, index, value)
                addresses.append(int(ba_copy, 2))

            # replace the value in all the possible memory addresses
            int_mem_value = int(mem_value)
            for address in addresses:
                memory[address] = int_mem_value

    return sum(memory.values())


def _replace_bits_from_mask(bits: str, mask: str, neutral_char: str):
    """Replaces some bits according to the given mask.

    For example, if:
    bit  = 00010010
    mask = XXXX1XX1
    and the neutral character is 'X',
    the non-X characters will replace the ones in the original bits.
    So the result will be 00011011
    """
    bit_len = len(bits)
    for i in range(bit_len):
        if (mask_char := mask[i]) != neutral_char:
            bits = _replace_at(bits, i, mask_char)
    return bits


def _replace_at(string: str, index: int, char: str):
    return string[:index] + char + string[index + 1:]


def solve():
    program_lines = get_input_list()

    # PART 1
    sum_of_values_1 = solve1(program_lines)
    print(f'[PART 1] The sum of values is {sum_of_values_1}')

    # PART 2
    sum_of_values_2 = solve2(program_lines)
    print(f'[PART 2] The sum of values is {sum_of_values_2}')


if __name__ == '__main__':
    solve()
