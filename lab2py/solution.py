import sys


def resolve(clause1, clause2):
    deletion_letter = []
    new_clause = []
    letter_deleted = False
    for letter1 in clause1:
        for letter2 in clause2:
            if letter1.startswith('~') and not letter2.startswith('~') and letter1[1:] == letter2:
                deletion_letter.append(letter2)
                deletion_letter.append(letter1)
                letter_deleted = True
            elif letter2.startswith('~') and not letter1.startswith('~') and letter2[1:] == letter1:
                deletion_letter.append(letter2)
                deletion_letter.append(letter1)
                letter_deleted = True
    for letter in clause1:
        if letter not in deletion_letter:
            new_clause.append(letter)
    for letter in clause2:
        if letter not in deletion_letter:
            new_clause.append(letter)
    return set(new_clause), letter_deleted



def resolution(clauses, goal):
    if goal[0].startswith('~'):
        goal[0] = goal[0][1:]
    else:
        goal[0] = '~' + goal[0]
    clauses.append(goal)
    First = True
    new = clauses
    while True:
        new_clause_added = False
        new_new = []
        for clause1, clause2 in [(clause1, clause2) for clause1 in clauses for clause2 in new]:
            new_clause, result = resolve(clause1, clause2)
            if result:
                if not new_clause:
                    return True
                elif new_clause not in clauses:
                    new_clause_added = True
                    new_new.append(new_clause)
        for clause in new:
            if clause not in clauses:
                clauses.append(clause)
        new = new_new.copy()
        if not new_clause_added:
            return False


def parse_goals(data):
    goals = []
    for line in data:
        goals.append(line.strip().lower().split(' v '))
    return goals


def parse_clause(data):
    clauses = []
    for line in data:
        clauses.append(set(line.strip().lower().split(' v ')))
    clauses[-1] = list(clauses[-1])
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
        goal = clause[-1][0]
        result = resolution(clause[:-1], clause[-1])
        if result:
            print(f"[CONCLUSION]: {goal} is true")
        else:
            print(f"[CONCLUSION]: {goal} is unknown")
    elif argv[0] == "cooking":
        data = parse_file(argv[2])

if __name__ == "__main__":
    main(sys.argv[1:])