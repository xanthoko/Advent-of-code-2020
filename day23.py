from typing import List
from collections import deque

from utils import get_input_text, get_example_input_text


def get_input_list():
    input_text = get_input_text(23)
    input_text = get_example_input_text()

    input_list = [int(x) for x in input_text]
    return input_list


def solve1(labels: List[int]):
    cups_lenght = len(labels)
    current_index = 0
    for _ in range(100):
        current_label = labels[current_index]
        picked_indexes = _get_next_3_indexes(current_index, cups_lenght)
        picked_labels = [labels[x] for x in picked_indexes]
        [labels.remove(x) for x in picked_labels]

        min_label = min(labels)
        max_label = max(labels)
        destination_label = current_label - 1
        while destination_label not in labels:
            destination_label -= 1
            if destination_label < min_label:
                destination_label = max_label
                break

        destination_index = labels.index(destination_label)
        let_go_indexes = _get_next_3_indexes(destination_index, cups_lenght)
        for label, index in zip(picked_labels, let_go_indexes):
            labels.insert(index, label)

        current_index = (labels.index(current_label) + 1) % cups_lenght

    index_of_1 = labels.index(1)
    lab_deq = deque(labels)
    lab_deq.rotate(-index_of_1)
    labels_from_1 = list(lab_deq)[1:]
    return ''.join([str(x) for x in labels_from_1])


def _get_next_3_indexes(current_index: int, cups_lenght: int):
    return [(current_index + x) % cups_lenght for x in range(1, 4)]


def solve():
    labels = get_input_list()

    # PART 1
    wanted_labels_1 = solve1(labels)
    print(f'[PART 1] The labels are {wanted_labels_1}')


if __name__ == '__main__':
    solve()
