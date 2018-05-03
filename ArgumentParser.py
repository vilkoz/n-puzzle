#!/usr/bin/env python3
import sys
import argparse
from Heruistics import manhattan_distance, linear_conflict, hamming_distance
from State import State

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="increase output verbosity",
            action="store_true")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--file", type=str, help="file with map")
    group.add_argument("-g", "--generate", type=int, help="generate map with provided size", default=3)
    parser.add_argument("-a", "--algorithm", type=str, choices=["manhattan", "linear_conflict", "hamming_distance", "all"],
            help="heruistics algorithm to solve N-puzzle", default="all", required=False)
    parser.add_argument("-i", "--iterations", type=int,
            help="how many times to shuffle board in map generation", default=20, required=False)
    parser.add_argument("-p", "--plot_path",
            help="plot solution path", action="store_true", required=False)
    parser.add_argument("-d", "--draw_solution",
            help="draw animated solution moves", action="store_true", required=False)
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

def remove_comments(line):
    if '#' in line:
        line = line[:line.index('#')]
    return line

def parse_file(file_name):
    with open(file_name, 'r') as f:
        initial_state = []
        size = None
        for line in f:
            if line[0] == "#":
                continue
            if not size:
                line = remove_comments(line)
                size = int(line.strip())
                continue
            current_row = [int(x) for x in remove_comments(line).strip().split()]
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

def shuffle(solved_state, times):
    s = State(solved_state, 0)
    for _ in range(0, times):
        tmp = s.makeOneRandomMove()
        if tmp:
            s = tmp
    return s.state

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
    if args.iterations < 0:
        print("wrong iteration number")
        sys.exit(1)
    if not initial_state:
        initial_state = shuffle(solved_state, args.iterations)
    heruistics = {
            "manhattan": manhattan_distance,
            "linear_conflict": linear_conflict,
            "hamming_distance": hamming_distance
            }
    if args.algorithm == "all":
        is_one_algo_used = False
        selected_heruistics = heruistics
    else:
        is_one_algo_used = True
        selected_heruistics = heruistics[args.algorithm]
    return initial_state, solved_state, selected_heruistics, is_one_algo_used
