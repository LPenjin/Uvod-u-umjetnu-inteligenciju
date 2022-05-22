import csv
import sys
import math

CLASS_LABEL = "class_label"
INTEGER_GREATER_THAN_ZERO = 2
NO_NAME = "no_name"
NO_RESULT = "no_result"


class Node:

    def __init__(self, name, value, depth):
        self.depth = depth
        self.name = name
        self.value = value
        self.leaves = []
        self.conditions = {}
        self.nodes_above = []


class Leaf:

    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.next = None
        self.result = None


def fit(train_dataset, *depth):
    if not depth:
        depth = math.inf
    else:
        depth = int(depth[0])

    all_results = list(set(train_dataset[CLASS_LABEL]))
    all_results.sort()
    max_count = -1
    statistically_highest = NO_RESULT
    for result in all_results:
        if train_dataset[CLASS_LABEL].count(result) > max_count:
            max_count = train_dataset[CLASS_LABEL].count(result)
            statistically_highest = result

    initial_entropy = get_entropy(train_dataset[CLASS_LABEL], statistically_highest)
    labels_count = {}
    for label in train_dataset:
        count = set(train_dataset[label])
        labels_count[label] = count

    initial_label_entropies = {}
    for label in train_dataset:
        if label == CLASS_LABEL:
            continue
        initial_label_entropies[label] = []
        for variable in labels_count[label]:
            class_label_list = extract_list(train_dataset, {label: variable})
            label_entropy = get_entropy(class_label_list, statistically_highest)
            initial_label_entropies[label].append(label_entropy)

    max_ig = 0
    name = NO_NAME
    for label in initial_label_entropies:
        information_gain = get_information_gain(initial_entropy[0], initial_label_entropies[label],
                                                len(train_dataset[CLASS_LABEL]))
        if information_gain > max_ig:
            max_ig = information_gain
            name = label
    root_node = Node(name, initial_entropy, 1)

    for index, variable in enumerate(labels_count[name]):
        new_leaf = Leaf(variable, initial_label_entropies[name][index])
        new_leaf.result = initial_label_entropies[name][index][2]
        root_node.leaves.append(new_leaf)
    root_node.nodes_above = [CLASS_LABEL, root_node.name]
    queue = [root_node]

    while queue:
        node = queue.pop()
        for leaf in node.leaves:
            if leaf.value[0] == 0:
                continue
            label_entropies = {}
            for label in labels_count:
                if label in node.nodes_above:
                    continue
                label_entropies[label] = []
                for variable in labels_count[label]:
                    conditions = node.conditions.copy()
                    conditions[node.name] = leaf.name
                    conditions[label] = variable
                    class_label_list = extract_list(train_dataset, conditions)
                    label_entropy = get_entropy(class_label_list, statistically_highest)
                    label_entropies[label].append(label_entropy)
            max_ig = -math.inf
            name = NO_NAME
            for label in initial_label_entropies:
                if label in node.nodes_above:
                    continue
                information_gain = get_information_gain(leaf.value[0], label_entropies[label],
                                                        len(train_dataset[CLASS_LABEL]))
                if information_gain > max_ig:
                    max_ig = information_gain
                    name = label
            if name == NO_NAME:
                break
            if node.depth + 1 <= depth:
                next_node = Node(name, node.value, node.depth + 1)
                for index, variable in enumerate(labels_count[name]):
                    new_leaf = Leaf(variable, label_entropies[name][index])
                    new_leaf.result = label_entropies[name][index][2]
                    next_node.leaves.append(new_leaf)
                leaf.next = next_node
                next_node.conditions = node.conditions.copy()
                next_node.conditions[node.name] = leaf.name
                next_node.nodes_above = node.nodes_above.copy()
                next_node.nodes_above.append(next_node.name)
                queue.append(next_node)
    return root_node, statistically_highest


def get_entropy(inputs, statistically_highest):
    if len(inputs) == 0:
        return 1.0, len(inputs), statistically_highest

    labels = list(set(inputs))
    labels.sort()
    helper_list = []
    max_count = -math.inf
    max_label = NO_RESULT
    for label in labels:
        if inputs.count(label) > max_count:
            max_count = inputs.count(label)
            max_label = label
    result = max_label
    for label in labels:
        input_count = inputs.count(label)
        if input_count == 0:
            input_count_log = INTEGER_GREATER_THAN_ZERO
        else:
            input_count_log = input_count
        helper_list.append((-(input_count/len(inputs)*math.log(input_count_log/len(inputs), 2))))
    entropy = sum(helper_list)
    return entropy, len(inputs), result


def get_information_gain(d, entropies, total):
    for entropy in entropies:
        d = d - entropy[0] * (entropy[1]/total)
    return d


def predict(test_dataset, root_node, statistically_highest):
    results = []
    for index in range(len(test_dataset[CLASS_LABEL])):
        queue = [root_node]
        while queue:
            node = queue.pop()
            found = False
            for leaf in node.leaves:
                if leaf.name == test_dataset[node.name][index]:
                    if leaf.next:
                        queue.append(leaf.next)
                    else:
                        results.append(leaf.result)
                    found = True
                    break
            if not found:
                results.append(statistically_highest)
    print(f"[PREDICTIONS]: {' '.join(results)}")
    accuracy_sum = 0
    for index, result in enumerate(results):
        if result == test_dataset[CLASS_LABEL][index]:
            accuracy_sum += 1
    accuracy = accuracy_sum/len(results)
    print(f"[ACCURACY]: {accuracy:.5f}")
    print('[CONFUSION_MATRIX]:')
    labels = sorted(list(set(test_dataset[CLASS_LABEL])))
    matrix = {}

    for l1 in labels:
        for l2 in labels:
            matrix[(l1, l2)] = 0

    for i, j in zip(results, test_dataset[CLASS_LABEL]):
        matrix[(j, i)] += 1

    for key in matrix:
        matrix[key] = str(matrix[key])

    for i in range(len(labels)):
        beginning = i*len(labels)
        ending = (i+1)*len(labels)
        print(" ".join(list(matrix.values())[beginning:ending]))


def extract_list(train_dataset, conditions):
    inputs = []
    for index, class_label_variable in enumerate(train_dataset[CLASS_LABEL]):
        broken = False
        for condition in conditions:
            if train_dataset[condition][index] != conditions[condition]:
                broken = True
                break
        if not broken:
            inputs.append(train_dataset[CLASS_LABEL][index])
    return inputs


def parse_csv(filename):
    csv_list = []
    train_dataset_dict = {}
    with open(filename, newline='') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            csv_list.append(row)
    csv_list[0][-1] = CLASS_LABEL
    for index_x, label in enumerate(csv_list[0]):
        train_dataset_dict[label] = []
        for index_y in range(1, len(csv_list)):
            train_dataset_dict[label].append(csv_list[index_y][index_x])
    return train_dataset_dict


def show_tree(root_node):
    print("[BRANCHES]:")
    queue = [root_node]
    while queue:
        curr_node = queue.pop()
        dfs(curr_node, [], 1)


def dfs(node, path, depth):
    for leaf in node.leaves:
        path.append(f"{depth}:{node.name}={leaf.name}")
        if leaf.next:
            dfs(leaf.next, path.copy(), depth+1)
            del(path[-1])
        else:
            print(" ".join(path) + ' ' + leaf.result)
            del(path[-1])


def main(arguments):
    if len(arguments) < 2:
        print("Not enough arguments given")
        return -1
    csv_train = parse_csv(arguments[0])
    csv_test = parse_csv(arguments[1])
    if len(arguments) == 3:
        depth = arguments[2]
        root_node, statistically_highest = fit(csv_train, depth)
    else:
        root_node, statistically_highest = fit(csv_train)
    show_tree(root_node)
    predict(csv_test, root_node, statistically_highest)


if __name__ == '__main__':
    main(sys.argv[1:])
