import math

# Hamming distance
def hamming_distance(configuration, goal_configuration):
    distance = 0
    for i in range(len(configuration)):
        for j in range(len(configuration[i])):
            if(configuration[i][j] == 0):
                continue
            if configuration[i][j] != goal_configuration[i][j]:
                distance+=1
    # print("Hamming Distance: ", distance)
    return distance
            
# Manhattan distance
def manhattan_distance(configuration, goal_configuration):
    total_distance = 0
    for i in range(len(configuration)):
        for j in range(len(configuration)):
            if(configuration[i][j] == 0):
                continue
            if configuration[i][j] != goal_configuration[i][j]:
                value = configuration[i][j]
                total_distance += measure_deviation(i, j, value, goal_configuration)
    # print("Manhattan distance: ", total_distance)
    return total_distance

# helper function associated with manhattan_distance
def measure_deviation(row, column, value, goal_configuration):
    for i in range(len(goal_configuration)):
        for j in range(len(goal_configuration[i])):
            if(value == goal_configuration[i][j]):
                distance = abs(row - i)
                distance = distance + abs(column - j)
                return distance
            
def euclidean_distance(configuration, goal_configuration):
    total_distance = 0.0
    for i in range(len(configuration)):
        for j in range(len(configuration)):
            if(configuration[i][j] == 0):
                continue
            if configuration[i][j] != goal_configuration[i][j]:
                value = configuration[i][j]
                total_distance += measure_euclidean_deviation(i, j, value, goal_configuration)
    # print("Euclidean Distance: ", total_distance)
    return total_distance

# helper function for euclidean distance
def measure_euclidean_deviation(row, column, value, goal_configuration):
    for i in range(len(goal_configuration)):
        for j in range(len(goal_configuration[i])):
            if(value == goal_configuration[i][j]):
                row_deviation = abs(row - i)
                column_deviation = abs(column - j)
                return math.sqrt(pow(row_deviation, 2) + pow(column_deviation, 2))
            
def linear_conflict(configuration, goal_configuration):
    manhattan = manhattan_distance(configuration, goal_configuration)
    total_conflict = 0
    total_conflict += measure_conflict(configuration, goal_configuration)
    transpose_configuration = [list(row) for row in zip(*configuration)]
    transpos_goal_configuration = [list(row) for row in zip(*goal_configuration)]
    total_conflict += measure_conflict(transpose_configuration, transpos_goal_configuration)
    return manhattan + 2 * total_conflict
    
def measure_conflict(configuration, goal_configuration):
    conflict = 0
    for i in range(len(configuration)):
        for j in range(len(configuration[i])):
            for k in range(j + 1, len(configuration[i])):
                if(configuration[i][j] == 0 or configuration[i][k] == 0):
                    continue
                is_same_row = isSameRowInGoal(i, configuration[i][j], configuration[i][k], goal_configuration)

                if(is_same_row):
                    if(configuration[i][j] > configuration[i][k]):
                        # print("conflict: ", configuration[i][j], " ", configuration[i][k])
                        conflict += 1   
    return conflict

def isSameRowInGoal(actual_row, first, second, goal_configuration):
    for i in range(len(goal_configuration)):
        for j in range(len(goal_configuration)):
            if(first == goal_configuration[i][j]):
                first_row = i
            elif(second == goal_configuration[i][j]):
                second_row = i    
    
    if(first_row == second_row == actual_row):
        return True
    else:
        return False