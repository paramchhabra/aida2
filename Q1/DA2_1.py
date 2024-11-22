import numpy as np
import copy

GOAL_STATE = [[1, 2, 3], 
              [4, 5, 6], 
              [7, 8, 0]]

def manhattan_distance(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] != 0:
                x, y = divmod(state[i][j] - 1, 3)
                distance += abs(x - i) + abs(y - j)
    return distance

def get_neighbors(state):
    neighbors = []
    empty_x, empty_y = next((i, j) for i in range(3) for j in range(3) if state[i][j] == 0)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in directions:
        new_x, new_y = empty_x + dx, empty_y + dy
        if 0 <= new_x < 3 and 0 <= new_y < 3:
            new_state = copy.deepcopy(state)
            new_state[empty_x][empty_y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[empty_x][empty_y]
            neighbors.append(new_state)
    return neighbors

def hill_climbing(initial_state):
    current_state = initial_state
    steps = 0
    while True:
        neighbors = get_neighbors(current_state)
        neighbors.sort(key=manhattan_distance)
        best_neighbor = neighbors[0]
        if manhattan_distance(best_neighbor) >= manhattan_distance(current_state):
            return current_state, steps
        current_state = best_neighbor
        steps += 1
        print(f"Step {steps}:")
        print(np.array(current_state))
        if current_state == GOAL_STATE:
            print("Goal reached!")
            return current_state, steps

initial_state = [[5, 2, 3], 
                 [1, 0, 6], 
                 [4, 7, 8]]

final_state, total_steps = hill_climbing(initial_state)
print("Final or Plateau State Reached:")
print(np.array(final_state))
print("Total steps:", total_steps)