#!/usr/bin/env python3
import sys
from time import perf_counter
from ArgumentParser import parse_arguments, validate_arguments
from npuzzle_view import NpuzzleView
from OrderedHashSet import OrderedHashSet
from State import State, set_f_score

INF=10e15

import networkx as nx
import matplotlib.pyplot as plt

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
    print("Solution lenght: %d" % len(path))
    return [x.state for x in reversed(path)]

class NpuzzleSolver:

    def __init__(self, initial_state, solved_state, heruistic_estimate, verbose=False):
        self.verbose = verbose
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
        self.max_state_number = 0

        self.graph = nx.Graph()

    def select_optimal_state(self):
        return self.opened_states.getElem()

    def _print_best_state_status(self, e):
        print("opened_states: ", len(self.opened_states),
                "closed_states: ", len(self.closed_states),
                "score: ", self.g_score[e],
                self.f_score[e] - self.g_score[e],
                self.f_score[e])

    def _update_max_state_count(self):
        self.max_state_number = max(self.max_state_number, len(self.opened_states) + len(self.closed_states))

    def _update_graph(self, e):
        self.graph.add_node(e)
        parent = self.came_from.get(e, None)
        if parent:
            self.graph.add_edge(parent, e)

    def solve(self):
        opened_states = self.opened_states
        closed_states = self.closed_states
        came_from = self.came_from
        f_score = self.f_score
        g_score = self.g_score
        solved_state = self.solved_state

        explored_states = 0
        while len(opened_states) >= 1:
            self._update_max_state_count()
            e = self.select_optimal_state()
            self._update_graph(e)
            explored_states += 1
            if self.verbose:
                print(e)
            if e.state == solved_state:
                print("Solved explored_states (time complexity):", explored_states, ", max_state_number(memory complexity):", self.max_state_number)
                return reconstruct_path(came_from, e)
            opened_states.remove(e)
            closed_states.add(e)
            for s in e.makeMoves():
                test_score = g_score.get(e, INF) + 1
                if test_score >= g_score.get(s, INF):
                    continue
                came_from[s] = e
                g_score[s] = test_score
                f_score[s] = test_score + self.heruistic_estimate(s.state, solved_state)
                if s in closed_states:
                    continue
                if s not in opened_states:
                    opened_states.add(s)
            if self.verbose and e in f_score and e in g_score:
                self._print_best_state_status(e)
        print("cant solve")
        return ()

def run_one_solver(initial_state, solved_state, heruistic_estimate, args):
    solver = NpuzzleSolver(initial_state, solved_state, heruistic_estimate, args.verbose);
    start_time = perf_counter()
    states = solver.solve()
    print("Compleated in %f seconds" % (perf_counter() - start_time))
    if args.plot_path:
        layout = nx.kamada_kawai_layout(solver.graph)
        nx.draw_networkx(solver.graph, pos=layout, node_size=100, with_labels=False,)
        plt.show()
    return states

def main():
    args = parse_arguments()
    initial_state, solved_state, selected_heruistics, is_one_algo_used = validate_arguments(args)
    states = None
    if is_one_algo_used:
        print("Solving with %s heruistics" % args.algorithm)
        states = run_one_solver(initial_state, solved_state, selected_heruistics, args)
    else:
        for heruistic_name in selected_heruistics:
            print("Solving with %s heruistics" % heruistic_name)
            new_states = run_one_solver(initial_state, solved_state, selected_heruistics[heruistic_name], args)
            if states == None:
                states = new_states
            if len(new_states) < len(states):
                states = new_states
    if args.draw_solution:
        view = NpuzzleView(states)
        view.display()

if __name__ == "__main__":
    main()
