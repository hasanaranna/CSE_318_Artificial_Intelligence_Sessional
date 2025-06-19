from semi_greedy_2105027 import semiGreedyMaxCut

def local_search(S, S_bar, edges, adjacency_list, n):
    
    # S and S_bar are from semiGreedyMaxCut
    assert S.isdisjoint(S_bar), "S and S_bar must be disjoint sets"

    improved = True
    iteration = 0
    # Initialize sigma values for all unassigned vertices
    sigmaValues = {}
    for v in range(1, n + 1):
        sigmaS = sigmaS_bar = 0
        for neighbour, w in adjacency_list[v]:
            if neighbour in S:
                sigmaS += w
            elif neighbour in S_bar:
                sigmaS_bar += w
        sigmaValues[v] = (sigmaS, sigmaS_bar)
    
    while improved:
        
        improved = False
        best_delta= 0
        best_v = None
        move_to = None

        for v in range(1, n + 1):
            sigmaS, sigmaS_bar = sigmaValues[v]

            # Delta is the difference in cut value if we move v to S or S_bar or vice versa
            if v in S:
                delta = sigmaS - sigmaS_bar
                if delta > best_delta:
                    best_delta = delta
                    best_v = v
                    move_to = 'S_bar'
            else:
                delta = sigmaS_bar - sigmaS
                if delta > best_delta:
                    best_delta = delta
                    best_v = v
                    move_to = 'S'

        # Make the best move found
        if best_delta > 0 and best_v is not None:
            improved = True
            if move_to == 'S':
                S_bar.remove(best_v)
                S.add(best_v)
        
                for neighbour, w in adjacency_list[best_v]:
                    sigmaS, sigmaS_bar = sigmaValues[neighbour]
                    sigmaValues[neighbour] = (sigmaS + w, sigmaS_bar - w)
            else:
                S.remove(best_v)
                S_bar.add(best_v)
                
                for neighbour, w in adjacency_list[best_v]:
                    sigmaS, sigmaS_bar = sigmaValues[neighbour]
                    sigmaValues[neighbour] = (sigmaS - w, sigmaS_bar + w)

    # Calculate the max cut value
    max_cut = 0 
    for v1, v2, w in edges:
        if (v1 in S and v2 in S_bar) or (v1 in S_bar and v2 in S):
            #print(f"Edge ({v1}, {v2}) contributes to max cut with weight {w}")
            max_cut += w

    return S, S_bar, max_cut
