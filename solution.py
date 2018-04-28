#!/usr/bin/env python3
import sys
from random import randint
from npuzzle_view import NpuzzleView
from OrderedHashSet import OrderedHashSet

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

    def findEmpty(self):
        for i in range(len(self.state)):
            for j in range(len(self.state[i])):
                if self.state[i][j] == 0:
                    return i, j

    def makeOneRandomMove(self):
        empty_coord = self.findEmpty()
        i = randint(0, 3)
        if i == 0 and empty_coord[0] > 0:
            return self._makeMove(empty_coord, [-1, 0])
        elif i == 1 and empty_coord[0] < len(self.state) - 1:
            return self._makeMove(empty_coord, [ 1, 0])
        elif i == 2 and empty_coord[1] > 0:
            return self._makeMove(empty_coord, [ 0,-1])
        elif i == 3 and empty_coord[1] < len(self.state) - 1:
            return self._makeMove(empty_coord, [ 0, 1])

    def makeMoves(self):
        empty_coord = self.findEmpty()
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
        return hash(s)

    def __eq__(self, other):
        return (self.state) == (other.state)

    def __ne__(self, other):
        return not (self == other)

    def print(self):
        s = ""
        for row in self.state:
            for item in row:
                s += str(item) + " "
            s += "\n"
        s += "moves: " + str(self.moves)
        print(s)

    def __repr__(self):
        s = "State("
        s += "["
        for row in self.state:
            s += "["
            for item in row:
                s += " " + str(item) + ","
            s += "]"
        s += "], "
        s += "moves: " + str(self.moves) + ")"
        return s

    def __lt__(self, value):
        return F_SCORE.get(self, INF) < F_SCORE.get(value, INF)

F_SCORE=None

def get_with_default(container, key, default):
    try:
        return container[key]
    except KeyError:
        return default

def select_optimal_state(f_score, states, solved_state):
    optimal = states.getElem()
    return optimal

def reconstruct_path(came_from, state):
    path = [state]
    end = False
    current_state = state
    while not end:
        try:
            path.append(came_from[current_state])
            current_state = path[-1]
        except KeyError:
            end = True
    return [x.state for x in reversed(path)]

def shuffle(solved_state, times):
    s = State(solved_state, 0)
    for _ in range(0, times):
        tmp = s.makeOneRandomMove()
        if tmp:
            s = tmp
    return s

def solve(initial_state, solved_state):
    global F_SCORE
    g_score = {}
    f_score = {}
    came_from = {}
    F_SCORE = f_score
    opened_states = OrderedHashSet()
    closed_states = OrderedHashSet()

    opened_states.add(State(initial_state, 0))
    first_item = opened_states.getElem()
    g_score[first_item] = 0
    f_score[first_item] = heruistic_estimate(first_item.state, solved_state)

    explored_states = 0
    while len(opened_states) >= 1:
        e = select_optimal_state(f_score, opened_states, solved_state)
        explored_states += 1
        print(e)
        if e.state == solved_state:
            print("solved: ", e.state, "explored_states:", explored_states)
            return reconstruct_path(came_from, e)
        opened_states.remove(e)
        closed_states.add(e)
        for s in e.makeMoves():
            test_score = g_score.get(e, INF) + 1
            if test_score >= g_score.get(s, INF):
                continue
            came_from[s] = e
            g_score[s] = test_score
            f_score[s] = test_score + heruistic_estimate(s.state, solved_state)
            if s in closed_states:
                continue
            if s not in opened_states:
                opened_states.add(s)
        if e in f_score and e in g_score:
            print("opened_states: ", len(opened_states), "closed_states: ", len(closed_states), "score: ", g_score[e], f_score[e] - g_score[e], f_score[e])
    print("cant solve")
    return ()

def main():
    size = 3
    solved_state = [[y + x * size for y in range(1, 1 + size)] for x in range(size)]
    solved_state[-1][-1] = 0
    initial_state = shuffle(solved_state, 100).state
    states = solve(initial_state, solved_state)
    view = NpuzzleView(states)
    view.display()

if __name__ == "__main__":
    main()
