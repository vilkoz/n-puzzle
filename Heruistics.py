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
        if i == 0:
            continue
        distance = sum([abs(x1 - x2) for x1, x2 in zip(solved_coords[i], current_coords[i])])
        h += distance
    return h

def hamming_distance(state_from, state_to):
    size = len(state_to)
    h = 0
    for i in range(size):
        for j in range(size):
            if state_from[i][j] != state_to[i][j]:
                h += 1
    return h


def linear_conflict(state_from, state_to):
    size = len(state_to)**2
    current_coords, solved_coords = _calculate_coords(state_from, state_to, size)
    h = 0
    for i in range(size):
        if i == 0:
            continue
        distance = sum([abs(x1 - x2) for x1, x2 in zip(solved_coords[i], current_coords[i])])
        h += distance

    linear_conflict = 0
    for i, row in enumerate(state_from):
        for j, item in enumerate(row):
            if item == 0:
                break
            # print("------------------------------------------------------------")
            # print("item:",item)
            goal = solved_coords[item]
            # print("goal", goal)
            # print("range", j, len(state_from))
            for x in range(j + 1, len(state_from)):
                conflicted_elem = state_from[i][x]
                # print("conflicted_elem x", conflicted_elem)
                if conflicted_elem == 0:
                    continue
                conflicted_goal = solved_coords[conflicted_elem]
                # print("conflicted_goal x", conflicted_goal)
                if goal[1] == conflicted_goal[1] and (goal == [x, i] or conflicted_goal == [j, i]):
                    linear_conflict += 1
                    # print("conflict")
            for y in range(i + 1, len(state_from)):
                conflicted_elem = state_from[y][j]
                # print("conflicted_elem y", conflicted_elem)
                if conflicted_elem == 0:
                    continue
                conflicted_goal = solved_coords[conflicted_elem]
                # print("conflicted_goal y", conflicted_goal)
                if goal[0] == conflicted_goal[0] and (goal == [j, y] or conflicted_goal == [j, i]):
                    linear_conflict += 1
                    # print("conflict")
            # print("------------------------------------------------------------")
    # print("conflicts", linear_conflict)
    return h + 2*linear_conflict
