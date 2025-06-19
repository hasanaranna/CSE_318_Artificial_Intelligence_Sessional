import os
import csv
from greedy_2105027 import greedyMaxCut
from randomized_2105027 import randomizedMaxCut
from semi_greedy_2105027 import semiGreedyMaxCut
from local_2105027 import local_search
from grasp_2105027 import grasp

# Known best solutions for specific graphs
known_best_solutions = {
    "G1": 12078, "G2": 12084, "G3": 12077, "G11": 627, "G12": 621, "G13": 645,
    "G14": 3187, "G15": 3169, "G16": 3172, "G22": 14123, "G23": 14129, "G24": 14131,
    "G32": 1560, "G33": 1537, "G34": 1541, "G35": 8000, "G36": 7996, "G37": 8009,
    "G43": 7027, "G44": 7022, "G45": 7020, "G48": 6000, "G49": 6000, "G50": 5988
}

def particular_graph(file_path):
    # Read the input from the file
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Parse the first line to get n and m
    n, m = map(int, lines[0].strip().split())

    # Initialize the graph as an adjacency list
    edges = []
    adjacency_list = {i: [] for i in range(1, n + 1)}
    for i in range(m):
        v1, v2, w = map(int, lines[i + 1].strip().split())
        edges.append((v1, v2, w))
        adjacency_list[v1].append((v2, w))
        adjacency_list[v2].append((v1, w))
    
    # Call the randomized function
    SimpleRandomized = randomizedMaxCut(edges, n)
    print(f"SimpleRandomized: {SimpleRandomized}")
    # Call the greedy function
    _, _, SimpleGreedy = greedyMaxCut(edges,adjacency_list, n)
    print(f"SimpleGreedy: {SimpleGreedy}")

    # Call the semi-greedy function
    S, S_bar, SemiGreedy = semiGreedyMaxCut(edges,adjacency_list, n, 0.5)
    print(f"SemiGreedy: {SemiGreedy}")

    average_value = 0
    # Call the local search function
    for i in range(5):
        S, S_bar, _ = semiGreedyMaxCut(edges,adjacency_list, n, 0.5)
        _, _, cut_value = local_search(S, S_bar, edges, adjacency_list, n)
        average_value += cut_value
    average_value /= 5
    print(f"SimpleLocal: {average_value}") 

    # Call the GRASP function
    _, _, GraspBestValue = grasp(edges,adjacency_list, n, maxIteration=50)
    print(f"GraspBestValue: {GraspBestValue}")

    # Return the results
    return n, m, SimpleRandomized, SimpleGreedy, SemiGreedy, 5, average_value, 50, GraspBestValue

def main():
    # Folder containing the graph files
    folder_path = "graph_GRASP/set1"
    output_csv = "2105027.csv"

    # Prepare the CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        # Header
        csvwriter.writerow([
            "Graph_name", "n", "m", "Randomized-1", "Greedy-1", 
            "Semi-greedy-2", "Local_iteration", "Local_avg_value", 
            "Grasp_iteration", "Grasp_Best_Value", "Known best solution"
        ])

        for i in range(1, 55):
            file_name = f"G{i}.rud"
            file_path = os.path.join(folder_path, file_name)
            if os.path.exists(file_path):
                
                print(f"Processing {file_name}...")

                n, m, SimpleRandomized, SimpleGreedy, SemiGreedy, LS_iteration, SimpleLocal, Grasp_iteration, GraspBestValue = particular_graph(file_path)

                graph_name = f"G{i}"

                known_best = known_best_solutions.get(graph_name, "N/A")

                csvwriter.writerow([
                    graph_name, n, m, SimpleRandomized, SimpleGreedy, 
                    SemiGreedy, LS_iteration, SimpleLocal, 
                    Grasp_iteration, GraspBestValue, known_best
                ])

    print(f"Results saved to {output_csv}")

if __name__ == "__main__":
    main()