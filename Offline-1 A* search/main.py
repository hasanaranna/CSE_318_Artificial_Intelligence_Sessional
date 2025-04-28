from solvable import is_solvable
from solver import solver
from heuristicFunctions import *

def print_board(configuration):
    for row in configuration:
        for num in row:
            print(num, end=" ")
        print()

def main():
    n = int(input("Enter the value of n: "))
    initial_configuration = []
    print("Enter the initial configuration row-wise (use 0 for blank space):")
    for i in range(n):
        row = list(map(int, input().split()))
        initial_configuration.append(row)
    
    #goal state will be defined based on the value of n
    #goal state will be a 2D list with numbers from 1 to n^2-1 and 0 at the last position
    goal_configuration = []
    for i in range(n):
        row = []
        for j in range(n):
            if i == n-1 and j == n-1:
                row.append(0)
            else:
                row.append(i*n + j + 1) 
        goal_configuration.append(row)

    h = int(input("Enter the heuristic value\n1. Hamming distance\n2. Manhattan distance\n3. Euclidean distance\n4. Linear Conflict\n\n"))
    if(h == 1):
        heuristic_function = hamming_distance
        print("Hamming distance: ", hamming_distance(initial_configuration, goal_configuration))
    elif(h == 2):
        heuristic_function = manhattan_distance
        print("Manhattan distance: ", manhattan_distance(initial_configuration, goal_configuration))
    elif(h == 3):
        heuristic_function = euclidean_distance
        print("Euclidean distance: ", round(euclidean_distance(initial_configuration, goal_configuration), 2))
    else:
        heuristic_function = linear_conflict
        print("Linear Conflict distance: ", linear_conflict(initial_configuration, goal_configuration))

    flag = is_solvable(initial_configuration)
    if flag:
        path = solver(initial_configuration, goal_configuration, heuristic_function)
        print()
        print("Minimum number of moves = ", len(path) - 1)
        print()  
        for move in path:
            print_board(move)
            print()
    else:
        print("\nUnsolvable puzzle.") 

if __name__ == "__main__":
    main()   