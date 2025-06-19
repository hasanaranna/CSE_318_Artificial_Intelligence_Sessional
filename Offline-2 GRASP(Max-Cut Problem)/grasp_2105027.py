from semi_greedy_2105027 import semiGreedyMaxCut
from local_2105027 import local_search
def grasp(edges,adjacency_list, n, maxIteration = 50):
    
    # Initialize variables
    best_cut = 0
    best_partition = None
    
    for i in range(1, maxIteration+1):
        #print(f"Iteration {i} of {maxIteration}")
        x, y, cut_value = semiGreedyMaxCut(edges,adjacency_list, n, alpha=0.5)
        
        # Local search to improve the solution
        S, S_bar, cut_value = local_search(x, y, edges, adjacency_list, n)

        if i == 1:
            best_cut = cut_value
            best_partition = (S, S_bar)
        else:
            if cut_value > best_cut:
                best_cut = cut_value
                best_partition = (S, S_bar)
    
    return best_partition[0], best_partition[1], best_cut