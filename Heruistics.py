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
    size = len(state_to)**2
    current_coords, solved_coords = _calculate_coords(state_from, state_to, size)
    h = 0
    for i in range(size):
        if i == 0:
            continue
        distance = sum([abs(x1 - x2) for x1, x2 in zip(solved_coords[i], current_coords[i])])
        h += distance
    return h * 3

def is_item_conflicts(item_pos, item_goal, conflicted_pos, conflicted_goal, axis):
    if item_goal == conflicted_pos or\
        item_pos == conflicted_goal:
        return 1
    if item_goal[axis] > conflicted_pos[axis] or\
        item_pos[axis] < conflicted_goal[axis]:
        return 1
    return 0

def find_conflicting_item(item_pos, item_goal, state_from, solved_coords, current_coords, i, j):
    linear_conflict = 0
    for x in range(j + 1, len(state_from)):
        conflicted_elem = state_from[i][x]
        if conflicted_elem == 0:
            continue
        linear_conflict += is_item_conflicts(
                item_pos, item_goal, current_coords[conflicted_elem], solved_coords[conflicted_elem], 1)
    for y in range(i + 1, len(state_from)):
        conflicted_elem = state_from[y][j]
        if conflicted_elem == 0:
            continue
        linear_conflict += is_item_conflicts(
                item_pos, item_goal, solved_coords[conflicted_elem], current_coords[conflicted_elem], 0)
    return linear_conflict

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
            item_goal = solved_coords[item]
            item_pos = current_coords[item]
            linear_conflict += find_conflicting_item(item_pos, item_goal,
                    state_from, solved_coords, current_coords, i, j)
    return h + 2*linear_conflict

if __name__ == "__main__":
    state_from = [
            [2,3,1],
            [4,5,6],
            [7,8,0]
            ]
    state_to = [
            [1,2,3],
            [4,5,6],
            [7,8,0]
            ]
    print("manhattan_distance: ", manhattan_distance(state_from, state_to))
    print("linear_conflict: ", linear_conflict(state_from, state_to))
    print("hamming_distance: ", hamming_distance(state_from, state_to))
