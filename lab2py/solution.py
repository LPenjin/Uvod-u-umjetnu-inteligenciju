import sys


def resolve(clause1, clause2, solution):
    resolvents = []
    for literal1 in clause1:
        for literal2 in clause2:
            if literal1.startswith('~') and literal1[1:] == literal2 or literal2.startswith('~') and literal2[1:] == literal1:
                resolvent = list(clause1).copy() + list(clause2)
                resolvent.remove(literal1)
                resolvent.remove(literal2)
                if resolvent:
                    resolvents.append(set(resolvent))
                    solution[' '.join(resolvent)] = (clause1, clause2)
                else:
                    resolvents.append('NIL')
                    solution['NIL'] = (clause1, clause2)

    return resolvents


def resolution(clauses, goals):
    og_nbr = len(clauses) + len(goals)
    new = goals
    current_clauses = clauses.copy()
    solution = {}
    checked = []
    while True:
        new_new = []
        for clause1 in current_clauses:
            for clause2 in new:
                if clause1 != clause2 and (clause1, clause2) not in checked:
                    resolvents = resolve(clause1, clause2, solution)
                    checked.append((clause1, clause2))
                    if resolvents:
                        if 'NIL' in resolvents:
                            if solution['NIL'][0] not in clauses:
                                clauses.append(solution['NIL'][0])
                            elif solution['NIL'][1] not in clauses:
                                clauses.append(solution['NIL'][1])
                            clauses.append(set(['NIL']))
                            queue = ['NIL']
                            path = ['NIL']
                            visited = {}
                            for clause in clauses:
                                visited[' '.join(clause)] = False
                            while queue:
                                node = queue.pop()
                                if node in solution and visited[node] == False:
                                    visited[node] = True
                                    queue.append(" ".join(solution[node][0]))
                                    queue.append(" ".join(solution[node][1]))
                                    path.append(f"{clauses.index(set(node.split(' '))) + 1}. {node} ({clauses.index(solution[node][0]) + 1}, {clauses.index(solution[node][1]) + 1})")
                            for index, clause in enumerate(clauses[:og_nbr]):
                                print(f"{index + 1}. {' v '.join(clause)}")
                            print("====================")
                            path.sort()
                            for step in path[:-1]:
                                print(step)
                            return True
                        for resolvent in resolvents:
                            if resolvent not in new_new:
                                new_new.append(resolvent)
        no_new_clauses = True
        repeated_clause = []
        for clause in new_new:
            if clause not in clauses:
                no_new_clauses = False
            else:
                repeated_clause.append(clause)
        if no_new_clauses:
            return False
        for clause in repeated_clause:
            new_new.remove(clause)
        current_clauses, new_new = delete_redundant(current_clauses, new_new)
        new_new = remove_tautology(new_new)
        current_clauses.extend(new_new)
        clauses.extend(new)
        new = new_new.copy()


def remove_tautology(new_new):
    removal = []
    for clause in new_new:
        list_clause = list(clause)
        for index in range(len(list_clause)):
            list_clause[index] = list_clause[index].replace('~', '')
        for literal in list_clause:
            if list_clause.count(literal) > 1:
                removal.append(clause)
                break
    for remove in removal:
        new_new.remove(remove)
    return new_new


def delete_redundant(clauses, new_new):
    removal = []
    for old_clause in clauses:
        for new_clause in new_new:
            intersection = old_clause.intersection(new_clause)
            if intersection == old_clause:
                removal.append(new_clause)
            elif intersection == new_clause:
                removal.append(old_clause)
    for remove in removal:
        if remove in clauses:
            clauses.remove(remove)
        if remove in new_new:
            new_new.remove(remove)
    return clauses, new_new


def get_goals(line):
    line = list(line)
    clauses = []
    for statement in line:
        if statement.startswith('~'):
            clause = set([statement[1:]])
        else:
            clause = set(['~' + statement])
        clauses.append(clause)
    return clauses


def parse_clause(data):
    clauses = []
    for line in data:
        clauses.append(set(line.strip().lower().split(' v ')))
    return clauses


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


def main(argv):
    if argv[0] == "resolution":
        data = parse_file(argv[1])
        clause = parse_clause(data)
        goals = get_goals(clause[-1])
        clause = clause[:-1]
        result = resolution(clause, goals)
        if result:
            print(f"[CONCLUSION]: {data[-1].strip()} is true")
        else:
            print(f"[CONCLUSION]: {data[-1].strip()} is unknown")
    elif argv[0] == "cooking":
        clauses = parse_file(argv[1])
        clauses = parse_clause(clauses)
        cookings = parse_file(argv[2])
        for cooking in cookings:
            ckg = cooking.strip().lower()
            if ckg.endswith('?'):
                goals = get_goals(ckg[:-2].split(' v '))
                result = resolution(clauses.copy(), goals)
                if result:
                    print(f"[CONCLUSION]: {ckg[:-2]} is true")
                else:
                    print(f"[CONCLUSION]: {ckg[:-2]} is unknown")
            elif ckg.endswith('+'):
                ckg = set(ckg[:-2].split(' v '))
                clauses.append(ckg)
            elif ckg.endswith('-'):
                ckg = set(ckg[:-2].split(' v '))
                clauses.remove(ckg)



if __name__ == "__main__":
    main(sys.argv[1:])