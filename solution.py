#!/usr/bin/env python3
import sys
from npuzzle_view import NpuzzleView
from OrderedHashSet import OrderedHashSet
from State import State, set_f_score

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

class NpuzzleSolver:

    def __init__(self, initial_state, solved_state, heruistic_estimate):
        self.g_score = {}
        self.f_score = {}
        self.came_from = {}
        set_f_score(self.f_score)
        self.opened_states = OrderedHashSet()
        self.closed_states = OrderedHashSet()
        self.heruistic_estimate = heruistic_estimate
        self.solved_state = solved_state

        self.opened_states.add(State(initial_state, 0))
        first_item = self.opened_states.getElem()
        self.g_score[first_item] = 0
        self.f_score[first_item] = self.heruistic_estimate(first_item.state, self.solved_state)

    def select_optimal_state(self):
        return self.opened_states.getElem()

    def _print_best_state_status(self, e):
        print("opened_states: ", len(self.opened_states),
                "closed_states: ", len(self.closed_states),
                "score: ", self.g_score[e],
                self.f_score[e] - self.g_score[e],
                self.f_score[e])

    def solve(self):
        opened_states = self.opened_states
        closed_states = self.closed_states
        came_from = self.came_from
        f_score = self.f_score
        g_score = self.g_score
        solved_state = self.solved_state

        explored_states = 0
        while len(opened_states) >= 1:
            e = self.select_optimal_state()
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
                self._print_best_state_status(e)
        print("cant solve")
        return ()

def main():
    size = 4
    solved_state = [[y + x * size for y in range(1, 1 + size)] for x in range(size)]
    solved_state[-1][-1] = 0
    initial_state = shuffle(solved_state, int(sys.argv[1])).state
    solver = NpuzzleSolver(initial_state, solved_state, heruistic_estimate);
    states = solver.solve()
    view = NpuzzleView(states)
    view.display()

if __name__ == "__main__":
    main()
