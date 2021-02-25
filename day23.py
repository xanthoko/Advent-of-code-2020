from typing import List
from collections import deque

from utils import get_input_text


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.previous = None

    def __repr__(self):
        return str(self.data)


class CircularLinkedList:
    def __init__(self, nodes_data=None):
        self.head = None
        self.length = len(nodes_data)

        if nodes_data:
            current_node = Node(data=nodes_data.pop(0))
            self.head = current_node
            previous_node = self.head
            for node_data in nodes_data:
                next_node = Node(data=node_data)

                current_node.next = next_node
                current_node = next_node
                current_node.previous = previous_node

                previous_node = current_node

            current_node.next = self.head
            self.head.previous = current_node

    def pick_up_next(self, current_node: Node, length: int) -> List[Node]:
        node = current_node.next
        picked = []
        for _ in range(length):
            nn = node.next
            picked.append(node)
            self.remove_node(node)
            node = nn
        return picked

    def place_next(self, current_node: Node, picked_nodes: List[Node]):
        node = current_node
        for picked_node in picked_nodes:
            self.add_after(node, picked_node)
            node = picked_node

    def add_after(self, target_node, new_node):
        if self.head is None:
            raise Exception('List is empty')

        next_node = target_node.next
        target_node.next = new_node
        next_node.previous = new_node
        new_node.next = next_node
        new_node.previous = target_node

        self.length += 1

    def remove_node(self, target_node: Node):
        if self.head is None:
            raise Exception('List is empty')

        previous_node = target_node.previous
        next_node = target_node.next

        if target_node.data == self.head.data:
            self.head = self.head.next

        previous_node.next = target_node.next
        next_node.previous = previous_node

        self.length -= 1

    def get_by_index(self, element_index: int) -> Node:
        if self.head is None:
            raise Exception('List is empty')

        element_index %= self.length
        counter = 0
        for node in self:
            if counter == element_index:
                return node
            counter += 1

        raise IndexError

    def get(self, node_data: str) -> Node:
        if self.head is None:
            raise Exception('List is empty')

        for node in self.traverse():
            if node.data == node_data:
                return node

    def traverse(self, starting_node=None):
        if starting_node is None:
            starting_node = self.head

        node = starting_node
        while node is not None and (node.next != starting_node):
            yield node
            node = node.next
        yield node

    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def __repr__(self):
        nodes = []
        for node in self.traverse():
            nodes.append(str(node.data))
        nodes.append('<-')
        return " -> ".join(nodes)


def get_input_list():
    input_text = get_input_text(23)

    input_list = [int(x) for x in input_text]
    return input_list


def solve1_old(labels: List[int], moves: int) -> str:
    """Implementation with simple list"""
    cups_lenght = len(labels)
    current_index = 0
    for _ in range(moves):
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


def solve1(labels: List[int], moves: int) -> str:
    """Implementation with Circular Linked Lists"""
    min_label = min(labels)
    max_label = max(labels)
    current_index = 0

    ll = CircularLinkedList(labels)
    current_node = ll.get_by_index(current_index)
    for _ in range(moves):
        picked_up = ll.pick_up_next(current_node, 3)

        destination_data = current_node.data - 1
        destination_node = ll.get(destination_data)
        while destination_node is None:
            destination_data -= 1
            if destination_data < min_label:
                destination_data = max_label
            destination_node = ll.get(destination_data)

        ll.place_next(destination_node, picked_up)
        current_node = current_node.next

    node_with_data_1 = ll.get(1)
    str_labels = ''
    for i in ll.traverse(node_with_data_1):
        str_labels += str(i.data)

    return str_labels[1:]


def solve2(labels: List[int]):
    next_cup = _build_list(labels)
    max_label = len(next_cup) - 1
    current_label = labels[0]

    for _ in range(10000000):
        first = next_cup[current_label]
        second = next_cup[first]
        third = next_cup[second]
        picked = (first, second, third)

        next_cup[current_label] = next_cup[third]

        destination_label = max_label if current_label == 1 else current_label - 1
        while destination_label in picked:
            if destination_label == 1:
                destination_label = max_label
            else:
                destination_label -= 1

        next_cup[third] = next_cup[destination_label]
        next_cup[destination_label] = first

        current_label = next_cup[current_label]

    after_1 = next_cup[1]
    second_after_1 = next_cup[after_1]
    return after_1 * second_after_1


def _build_list(labels: List[int]) -> List[int]:
    """Builds the list that in the i index contains the next label of the
    i-th label."""
    max_label = max(labels)
    labels += list(range(max_label + 1, 1000001))

    next_cup = [0] * len(labels)
    for prev, cur in zip(labels, labels[1:]):
        next_cup[prev] = cur
    next_cup.append(labels[0])

    return next_cup


def solve():
    labels = get_input_list()

    # PART 1
    wanted_labels_1 = solve1(labels, 100)
    print(f'[PART 1] The labels are {wanted_labels_1}')

    # PART 2
    wanted_labels_2 = solve2(labels)
    print(f'[PART 2] The labels are {wanted_labels_2}')


if __name__ == '__main__':
    solve()
