import argparse


def bfs(state_space):
    start, goal, ss_dict = parse_space_state(state_space)
    states_visited = 1
    path = []
    total_cost = 0
    queue = [start]
    while queue:
        curr_state =
    return


def ucs(state_space):
    start, goal, ss_dict = parse_space_state(state_space)
    return


def astar(state_space, heuristic):
    start, goal, ss_dict = parse_space_state(state_space)
    h_dict = parse_heuristic(heuristic)
    return


def check_optimistic(state_space, heuristic):
    start, goal, ss_dict = parse_space_state(state_space)
    h_dict = parse_heuristic(heuristic)
    return


def check_consistent(state_space, heuristic):
    start, goal, ss_dict = parse_space_state(state_space)
    h_dict = parse_heuristic(heuristic)
    return


def parse_arguments():
    """

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
    with open(file_location) as file:
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
    goal = data[1].strip()
    for line in data:
        new_line = line.strip().replace(':', '').split(' ')
        ss_dict[new_line[0]] = [tuple(word.split(',')) for word in new_line[1:]]
    return start, goal, ss_dict


def parse_heuristic(data):
    "Converts the list of lines to a dictionary where each state holds heuristic value"
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
            bfs(state_space)
        else:
            print('State space descriptor not defined!')
    elif args.alg == 'ucs':
        if args.ss:
            state_space = parse_file(args.ss)
            ucs(state_space)
        else:
            print('State space descriptor not defined!')
    elif args.alg == 'astar':
        if args.ss and args.h:
            state_space = parse_file(args.ss)
            heuristic = parse_file(args.h)
            astar(state_space, heuristic)
        else:
            print('State space descriptor or Heuristic descriptor not defined!')
    if args.check_optimistic:
        if args.ss and args.h:
            state_space = parse_file(args.ss)
            heuristic = parse_file(args.h)
            check_optimistic(state_space, heuristic)
        else:
            print('State space descriptor or Heuristic descriptor not defined!')
    if args.check_consistent:
        if args.ss and args.h:
            state_space = parse_file(args.ss)
            heuristic = parse_file(args.h)
            check_consistent(state_space, heuristic)
        else:
            print('State space descriptor or Heuristic descriptor not defined!')


if __name__ == '__main__':
    main()
