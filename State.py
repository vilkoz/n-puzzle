#!/usr/bin/env python3
from random import randint

F_SCORE=None
INF=10e15

def set_f_score(f_score):
    global F_SCORE
    F_SCORE = f_score

class State:
    def __init__(self, state, num_of_moves):
        self.state = state
        self.moves = num_of_moves
        self.h = -1

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

    def __hash__(self):
        s = "".join([str(x) for x in sum(self.state, [])])
        return hash(s)

    def __eq__(self, other):
        if type(other) != type(self):
            return False
        return (self.state) == (other.state)

    def __ne__(self, other):
        return not (self == other)

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
