import random

def randomizedMaxCut(edges, n):
    totalCutWeight = 0
    for _ in range(1, n + 1):
        X = set()
        Y = set()
        for j in range(1, n + 1):
            if random.random() >= 0.5:
                X.add(j)
            else:
                Y.add(j)
        cutWeight = 0
        for edge in edges:
            v1, v2, w = edge
            if (v1 in X and v2 in Y) or (v1 in Y and v2 in X):
                cutWeight += w
        totalCutWeight += cutWeight

    averageCutWeight = totalCutWeight / n
    return averageCutWeight