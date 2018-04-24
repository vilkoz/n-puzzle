#!/usr/bin/env python3
import sys

INF=10e15

def heruistic_estimate(state_from, state_to):
    size = len(state_to)**2
    solved_coords = [[0,0] for _ in range(size)]
    current_coords = [[0,0] for _ in range(size)]
    for i, row in enumerate(state_to):
        for j, item in enumerate(row):
            solved_coords[item][0] = j
            solved_coords[item][1] = i
    for i, row in enumerate(state_from):
        for j, item in enumerate(row):
            current_coords[item][0] = j
            current_coords[item][1] = i
    h = 0
    for i in range(size):
        distance = sum([abs(x1 - x2) for x1, x2 in zip(solved_coords[i], current_coords[i])])
        h += distance
    return h

class State:
    def __init__(self, state, num_of_moves):
        self.state = state
        self.moves = num_of_moves
        self.h = -1

    def getG(self):
        return self.moves

    def getH(self, solved_state):
        if self.h != -1:
            return self.h
        self.h = heruistic_estimate(self.state, solved_state)
        return self.h

    def getScore(self, solved_state):
        return self.getG() + self.getH(solved_state)

    def _makeMove(self, empty_coord, direction):
        arr = [[y for y in x] for x in self.state]
        x1, y1 = empty_coord[0], empty_coord[1]
        x2, y2 = empty_coord[0] + direction[0], empty_coord[1] + direction[1]
        arr[x1][y1], arr[x2][y2] = arr[x2][y2], arr[x1][y1]
        next_state = State(arr, self.moves + 1)
        return next_state

    def makeMoves(self):
        empty_coord = [0, 0]
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                if self.state[i][j] == 0:
                    empty_coord = [j, i]
        moves = []
        if empty_coord[0] > 0:
            moves.append(self._makeMove(empty_coord, [-1,  0]))
        if empty_coord[0] < len(self.state) - 1:
            moves.append(self._makeMove(empty_coord, [ 1,  0]))
        if empty_coord[1] > 0:
            moves.append(self._makeMove(empty_coord, [ 0, -1]))
        if empty_coord[1] < len(self.state) - 1:
            moves.append(self._makeMove(empty_coord, [ 0,  1]))
        return moves

    def __hash__(self):
        s = "".join([str(x) for x in sum(self.state, [])])
        # print(s)
        return hash(s)#, self.moves))

    def __eq__(self, other):
        return (self.state) == (other.state)

    def __ne__(self, other):
        return not (self == other)

class HashSet:
    def __init__(self):
        self.table = {}

    def add(self, elem):
        self.table[elem] = 1

    def getElem(self):
        for key in self.table.keys():
            return key

    def __iter__(self):
        yield next(iter(self.table))
    
    def __len__(self):
        return len(self.table)

    def __contains__(self, key):
        try:
            if self.table[key]:
                pass
            return True
        except KeyError:
            return False

    def remove(self, elem):
        try:
            self.table.pop(elem)
        except KeyError:
            pass

def get_with_default(container, key, default):
    try:
        return container[key]
    except KeyError:
        return default

def select_optimal_state(f_score, states, solved_state):
    optimal = states.getElem()
    optimal_score = get_with_default(f_score, optimal, INF)
    for state in states:
        state_f_score = get_with_default(f_score, state, INF)
        if state_f_score < optimal_score:
            optimal = state
            optimal_score = state_f_score
    return optimal

def solve(initial_state, solved_state):
    g_score = {}
    f_score = {}
    came_from = {}
    solved = False
    opened_states = HashSet()
    opened_states.add(State(initial_state, 0))
    first_item = opened_states.getElem()
    g_score[first_item] = 0
    f_score[first_item] = heruistic_estimate(first_item.state, solved_state)
    closed_states = HashSet()
    while not solved and len(opened_states) >= 1:
        e = select_optimal_state(f_score, opened_states, solved_state)
        if e.state == solved_state:
            print("solved: ", e.state)
            solved = True
            return 
        else:
            opened_states.remove(e)
            closed_states.add(e)
            for s in e.makeMoves():
                if s in closed_states:
                    # print("repeat: ", repr(s.state).replace("]", "\\]").replace("[", "\\["))
                    print(repr(s.state).replace("]", "\\]").replace("[", "\\["))
                    continue
                if s not in opened_states:
                    print("add: ", s.state, file=sys.stderr)
                    opened_states.add(s)
                test_score = g_score.get(e, INF) + 1
                if test_score >= g_score.get(s, INF):
                    continue
                came_from[s] = e
                g_score[s] = test_score
                f_score[s] = test_score + heruistic_estimate(s.state, solved_state)
            # print("opened_states: ", len(opened_states), "closed_states: ", len(closed_states), "score: ", g_score[s], f_score[s] - g_score[s], f_score[s])
    print("cant solve")

def main():
    initial_state = [[0, 1, 2], [5, 6, 3], [4, 7, 8]]
    solved_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    solve(initial_state, solved_state)

if __name__ == "__main__":
    main()
