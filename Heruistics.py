#!/usr/bin/env python3

def _calculate_coords(state_from, state_to, size):
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
    return current_coords, solved_coords

def manhattan_distance(state_from, state_to):
    size = len(state_to)**2
    current_coords, solved_coords = _calculate_coords(state_from, state_to, size)
    h = 0
    for i in range(size):
        distance = sum([abs(x1 - x2) for x1, x2 in zip(solved_coords[i], current_coords[i])])
        h += distance
    return h