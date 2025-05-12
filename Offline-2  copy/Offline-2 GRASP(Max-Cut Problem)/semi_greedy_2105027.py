import random

def semiGreedyMaxCut(edges,adjacency_list, n, alpha=0.5):
    x = set()
    y = set()

    # Finding the max edge and adding it to separate sets
    max_weight = -1
    max_edge = None
    for v1, v2, w in edges:
        if w > max_weight:
            max_weight = w
            max_edge = (v1, v2)

    if max_edge:
        u, v = max_edge
        x.add(u)
        y.add(v)

    unassigned = set(range(1, n + 1)) - x - y

    # Initialize sigma values for all unassigned vertices
    sigma_values = {}
    for v in unassigned:
        sigmaX = sigmaY = 0
        for neighbour, w in adjacency_list[v]:
            if neighbour in x:
                sigmaX += w
            elif neighbour in y:
                sigmaY += w
        sigma_values[v] = (sigmaX, sigmaY)

    while unassigned:
        wmin = float('inf')
        wmax = float('-inf')

        for sigmaX, sigmaY in sigma_values.values():
            wmin = min(wmin, sigmaX, sigmaY)
            wmax = max(wmax, sigmaX, sigmaY)

        if wmax == wmin:
            mu = wmin
        else:
            mu = wmin + alpha * (wmax - wmin)

        rcl = []
        for v in unassigned:
            sigmaX, sigmaY = sigma_values[v]
            greedyFunctionValue = max(sigmaX, sigmaY)
            if greedyFunctionValue >= mu:
                rcl.append(v)
        
        # If RCL is empty, break the loop
        if not rcl:
            break

        randomVertex = random.choice(rcl)
        sigmaX_rand, sigmaY_rand = sigma_values[randomVertex]

        if sigmaX_rand > sigmaY_rand:
            y.add(randomVertex)
        else:
            x.add(randomVertex)

        unassigned.remove(randomVertex)
        del sigma_values[randomVertex]  

        for neighbour, w in adjacency_list[randomVertex]:
            if neighbour in unassigned:
                sigmaX, sigmaY = sigma_values[neighbour]
                if randomVertex in x:
                    sigma_values[neighbour] = (sigmaX + w, sigmaY)
                else:
                    sigma_values[neighbour] = (sigmaX, sigmaY + w)


    max_cut = 0
    for v1, v2, w in edges:
        if (v1 in x and v2 in y) or (v1 in y and v2 in x):
            max_cut += w

    return x, y, max_cut