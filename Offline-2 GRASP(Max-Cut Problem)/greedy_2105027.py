def greedyMaxCut(edges, adjacency_list, n):
    x = set()
    y = set()

    # Finding the max edge and adding it to separate sets
    max_weight = -1
    max_edge = None

    for edge in edges:
        v1, v2, w = edge
        if w > max_weight:
            max_weight = w
            max_edge = edge

    x.add(max_edge[0])
    y.add(max_edge[1])
    current_partial_cut = max_weight
    
    unassigned = set(range(1, n + 1)) - {max_edge[0], max_edge[1]}
    
    # While there are unassigned vertices
    while unassigned:
        u = unassigned.pop()
        weightX = 0
        weightY = 0
        
        for neighbour, w in adjacency_list[u]:
            if neighbour in x:
                weightY += w
            elif neighbour in y:
                weightX += w
        if weightX > weightY:
            x.add(u)
            current_partial_cut += weightX
        else:
            y.add(u)
            current_partial_cut += weightY

    return x, y, current_partial_cut