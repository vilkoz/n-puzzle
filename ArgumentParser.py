#!/usr/bin/env python3
import sys
import argparse
from Heruistics import heruistic_estimate

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
            action="store_true")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--file", type=str, help="file with map")
    group.add_argument("-g", "--generate", type=int, help="generate map with provided size", default=3)
    parser.add_argument("-a", "--algorithm", type=str, choices=["manhattan", "row", "a_star", "all"],
            help="algorithm to solve N-puzzle", default="all", required=False)
    return parser.parse_args();

def generate_solved_state(size):
    solved_state = [[y + x * size for y in range(1, 1 + size)] for x in range(size)]
    solved_state[-1][-1] = 0
    return solved_state

def is_state_solvable(state):
    # https://www.cs.princeton.edu/courses/archive/fall12/cos226/assignments/8puzzle.html
    size = len(state)
    inversions = 0;
    flat = sum(state, [])
    for i, num in enumerate(flat):
        for val in flat[i:]:
            if num != 0 and val != 0 and num > val:
                inversions += 1
    print("inversions", inversions)
    if (size % 2) == 0:
        for i, row in enumerate(state):
            if 0 in row:
                empty_row = i
                break
        return ((empty_row + inversions) % 2) != 0
    else:
        return (inversions % 2) == 0

def is_valid_items(state, size):
    items = sum(state, []) # flatten list
    items = [x for x in sorted(items)]
    valid_items = [x for x in range(size**2)]
    return items == valid_items

def parse_file(file_name):
    with open(file_name, 'r') as f:
        initial_state = []
        size = None
        for line in f:
            if line[0] == "#":
                continue
            if not size:
                size = int(line.strip())
                continue
            current_row = [int(x) for x in line.strip().split()]
            if len(current_row) > size:
                raise Exception("Invalid file format")
            if len(initial_state) == size:
                break
            initial_state.append(current_row)
    if len(initial_state) > size:
        raise Exception("Invalid file format")
    if not is_valid_items(initial_state, size):
        raise Exception("Invalid value in map")
    if not is_state_solvable(initial_state):
        raise Exception("Map is not solvable")
    return size, initial_state

def validate_arguments(args):
    if args.file:
        try:
            size, initial_state = parse_file(args.file)
        except Exception as e:
            print(e)
            sys.exit(1)
    else:
        size = args.generate
        initial_state = None
    if size < 2:
        print("generate map size should be more than 2")
        sys.exit(1)
    if size > 8:
        print("OH MY FUCKING GOD THAT WILL BE FUN TO REBOOT COMPUTER")
    solved_state = generate_solved_state(size)
    if not initial_state:
        initial_state = shuffle(solved_state, 40)
    heruistics = {
            "manhattan": heruistic_estimate,
            "row": heruistic_estimate,
            "a_star": heruistic_estimate
            }
    if args.algorithm == "all":
        is_one_algo_used = False
        selected_heruistics = heruistics
    else:
        is_one_algo_used = True
        selected_heruistics = heruistics[args.algorithm]
    return initial_state, solved_state, selected_heruistics, is_one_algo_used
