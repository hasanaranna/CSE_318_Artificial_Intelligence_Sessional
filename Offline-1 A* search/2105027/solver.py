# A* search algorithm implementation
from queue import PriorityQueue

def solver(initial_configuration, goal_configuration, heuristic_function):
    class Node:
        def __init__(self, state, parent=None):
            self.state = state  # current board configuration
            self.parent = parent  # reference to previous node
            self.g = 0  # Cost from start to this node
            self.h = 0  # Heuristic cost to goal
            self.f = 0  # Total cost

        def __lt__(self, other):
            return self.f < other.f

    def heuristic(state):
        return heuristic_function(state, goal_configuration)

    def get_neighbors(node):
        neighbors = []
        for i in range(len(node.state)):
            for j in range(len(node.state[i])):
                if(node.state[i][j] == 0):
                    x = i
                    y = j

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < len(node.state) and 0 <= new_y < len(node.state[0]):
                new_state = [row[:] for row in node.state]
                new_state[new_x][new_y] = node.state[x][y]
                new_state[x][y] = node.state[new_x][new_y]

                neighbors.append(Node(new_state, node))

        return neighbors

    def reconstruct_path(node):  # Reconstruct the path from start to goal
        path = []
        while node:
            path.append(node.state)
            node = node.parent
        return path[::-1]

    open_list = PriorityQueue()
    closed_set = set()

    start_node = Node(initial_configuration)
    start_node.h = heuristic(start_node.state)
    start_node.f = start_node.g + start_node.h

    open_list.put(start_node)
    explored = 1
    expanded = 0
    closed_set.add(tuple(map(tuple, start_node.state))) 

    while not open_list.empty():
        current_node = open_list.get() # Node with lowest f value

        if current_node.state == goal_configuration:
            print("\nExplored Node: ", explored)
            print("Expanded Node: ", expanded)
            return reconstruct_path(current_node)
        
        expanded += 1
        for neighbor in get_neighbors(current_node):
            neighbor.g = current_node.g + 1
            neighbor.h = heuristic(neighbor.state)
            neighbor.f = neighbor.g + neighbor.h

            if tuple(map(tuple, neighbor.state)) in closed_set:
                continue
            
            better_exists = False
            for node in open_list.queue:
                if  neighbor.f > node.f and tuple(map(tuple, neighbor.state)) == tuple(map(tuple, node.state)):
                    better_exists = True
            if not better_exists:
                open_list.put(neighbor)
                explored += 1
                closed_set.add(tuple(map(tuple, neighbor.state)))


    return None  