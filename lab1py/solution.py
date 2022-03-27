import argparse
import heapq


def bfs(state_space):
    start, goal, ss_dict = parse_space_state(state_space)
    visited = {}
    state_visited = 0
    for state in list(ss_dict.keys()):
        visited[state] = False
    queue = [(start, 1)]
    visited[start] = True
    while queue:
        curr_state = queue.pop(0)
        state_visited += 1
        if curr_state[0] in goal:
            return curr_state
        for state_tuple in ss_dict[curr_state[0]]:
            if not visited[state_tuple[0]]:
                queue.append((state_tuple[0], curr_state[1] + 1, state_visited))
                visited[state_tuple[0]] = True
    return False


def ucs(start, goal, ss_dict):
    states_visited = 0
    visited = {}
    for state in list(ss_dict.keys()):
        visited[state] = float('inf')
    queue = [(0, start, 1, [start])]
    visited[start] = 0
    heapq.heapify(queue)
    while queue:
        curr_state = heapq.heappop(queue)
        states_visited += 1
        if curr_state[1] in goal:
            return curr_state, states_visited
        for state_tuple in ss_dict[curr_state[1]]:
            distance = curr_state[0] + float(state_tuple[1])
            if distance < visited[state_tuple[0]]:
                curr_state_tuple = (curr_state[0] + float(state_tuple[1]), state_tuple[0], curr_state[2] + 1,
                                    curr_state[3].copy())
                curr_state_tuple[3].append(state_tuple[0])
                heapq.heappush(queue, curr_state_tuple)
                visited[curr_state[1]] = distance
    return False


def astar(state_space, heuristic):
    start, goal, ss_dict = parse_space_state(state_space)
    h_dict = parse_heuristic(heuristic)
    open = [(float(h_dict[start]), start, int(h_dict[start]), 0.0)]
    open_dict = {}
    closed_dict = {}
    states_visited = 0
    for state in ss_dict:
        open_dict[state] = False
        closed_dict[state] = False
    open_dict[start] = True
    heapq.heapify(open)
    closed = []
    heapq.heapify(closed)
    while open:
        curr_state = heapq.heappop(open)
        open_dict[curr_state[1]] = False
        states_visited += 1
        if curr_state[1] in goal:
            return curr_state, states_visited
        heapq.heappush(closed, curr_state)
        closed_dict[curr_state[1]] = True
        for state_tuple in ss_dict[curr_state[1]]:
            if open_dict[state_tuple[0]] and open_dict[state_tuple[0]] <= curr_state[3] + int(state_tuple[1]) or closed_dict[state_tuple[0]]:
                continue
            curr_state_tuple = (curr_state[3] + int(state_tuple[1]) + int(h_dict[state_tuple[0]]), state_tuple[0],
                                int(h_dict[state_tuple[0]]),
                                curr_state[3] + float(state_tuple[1]))
            heapq.heappush(open, curr_state_tuple)
            open_dict[state_tuple[0]] = curr_state_tuple[3]


def check_optimistic(state_space, heuristic):
    start, goal, ss_dict = parse_space_state(state_space)
    h_dict = parse_heuristic(heuristic)
    optimistic = True
    for node in h_dict:
        result, states_visited = ucs(node, goal, ss_dict)
        if result[0] >= float(h_dict[node]):
            print(f"[CONDITION]: [OK] h({node}) <= h*: {float(h_dict[node])} <= {float(result[0])}")
        else:
            print(f"[CONDITION]: [ERR] h({node}) <= h*: {float(h_dict[node])} <= {float(result[0])}")
            optimistic = False
    return optimistic


def check_consistent(state_space, heuristic):
    start, goal, ss_dict = parse_space_state(state_space)
    h_dict = parse_heuristic(heuristic)
    consistent = True
    for node in ss_dict:
        for transition, cost in ss_dict[node]:
            if float(h_dict[node]) <= float(h_dict[transition]) + float(cost):
                print(f"[CONDITION]: [OK] h({node}) <= h({transition}) + c:"
                      f" {float(h_dict[node])} <= {float(h_dict[transition])} + {float(cost)}")
            else:
                print(f"[CONDITION]: [ERR] h({node}) <= h({transition}) + c:"
                      f" {float(h_dict[node])} <= {float(h_dict[transition])} + {float(cost)}")
                consistent = False
    return consistent


def parse_arguments():
    """
    Function for passing arguments
    """
    parser = argparse.ArgumentParser(
        description='UI labos',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--alg', type=str, default=None)
    parser.add_argument('--ss', type=str, default=None)
    parser.add_argument('--h', type=str, default=None)
    parser.add_argument('--check-optimistic', action='store_true')
    parser.add_argument('--check-consistent', action='store_true')
    return parser.parse_args()


def parse_file(file_location):
    """
    Loads the file and puts all lines in a list.
    After loading, it removes all commented lines that start with #
    """
    with open(file_location, encoding='utf-8') as file:
        data = file.readlines()
    index = 0
    while index < len(data):
        if data[index].startswith('#'):
            del data[index]
        else:
            index += 1
    return data


def parse_space_state(data):
    """
    Converts the line list to a dictionary where each states hold a list of tuples
    A tuple consists of a state and cost (state, cost)
    """
    ss_dict = {}
    start = data[0].strip()
    goal = data[1].strip().split(" ")
    for line in data[2:]:
        new_line = line.strip().replace(':', '').split(' ')
        ss_dict[new_line[0]] = [list(word.split(',')) for word in new_line[1:]]
        for i in range(len(ss_dict[new_line[0]])):
            ss_dict[new_line[0]][i][1] = int(ss_dict[new_line[0]][i][1])
        ss_dict[new_line[0]].sort(key=lambda x: x[1])
    return start, goal, ss_dict


def parse_heuristic(data):
    """
    Converts the list of lines to a dictionary where each state holds heuristic value
    """
    h_dict = {}
    for line in data:
        words = line.strip().split(': ')
        h_dict[words[0]] = words[1]
    return h_dict


def main():
    """
    Parses arguments and initiates all necessary checks
    """
    args = parse_arguments()
    if args.alg and args.alg == 'bfs':
        if args.ss:
            state_space = parse_file(args.ss)
            result = bfs(state_space)
            if result:
                print(f"[FOUND_SOLUTION]: yes")
                print(f"[PATH_LENGTH]: {result[1]}")
                print(f"[STATES_VISITED]: {result[2]}")
            else:
                print(f"[FOUND_SOLUTION]: no")
        else:
            print('State space descriptor not defined!')
    elif args.alg == 'ucs':
        if args.ss:
            state_space = parse_file(args.ss)
            start, goal, ss_dict = parse_space_state(state_space)
            result, state_space = ucs(start, goal, ss_dict)
            if result:
                print(f"[FOUND_SOLUTION]: yes")
                print(f"[STATES_VISITED]: {state_space}")
                print(f"[PATH_LENGTH]: {result[2]}")
                print(f"[TOTAL_COST]: {result[0]}")
                print(f"[PATH]: {' => '.join(result[3])}")
            else:
                print(f"[FOUND_SOLUTION]: no")
        else:
            print('State space descriptor not defined!')
    elif args.alg == 'astar':
        if args.ss and args.h:
            state_space = parse_file(args.ss)
            heuristic = parse_file(args.h)
            result, states_visited = astar(state_space, heuristic)
            if result:
                print(f"[FOUND_SOLUTION]: yes")
                print(f"[STATES_VISITED]: {states_visited}")
                print(f"[TOTAL_COST]: {result[3]}")
            else:
                print(f"[FOUND_SOLUTION]: no")
        else:
            print('State space descriptor or Heuristic descriptor not defined!')
    if args.check_optimistic:
        if args.ss and args.h:
            state_space = parse_file(args.ss)
            heuristic = parse_file(args.h)
            result = check_optimistic(state_space, heuristic)
            if result:
                print(f"[CONCLUSION]: Heuristic is optimistic.")
            else:
                print(f"[CONCLUSION]: Heuristic is not optimistic.")
        else:
            print('State space descriptor or Heuristic descriptor not defined!')
    if args.check_consistent:
        if args.ss and args.h:
            state_space = parse_file(args.ss)
            heuristic = parse_file(args.h)
            result = check_consistent(state_space, heuristic)
            if result:
                print(f"[CONCLUSION]: Heuristic is consistent.")
            else:
                print(f"[CONCLUSION]: Heuristic is not consistent.")
        else:
            print('State space descriptor or Heuristic descriptor not defined!')


if __name__ == '__main__':
    main()
