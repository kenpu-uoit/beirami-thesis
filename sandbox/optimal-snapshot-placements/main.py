import numpy as np

def single_snapshot(Q):
    if len(Q) == 0:
        return 0
    else:
        n = len(Q)
        s = sorted(Q)[n // 2]
        cost = 0.0
        for q in Q:
            cost += abs(q - s)
        return (cost, s)

INF = 10000.0

def optimal_snapshots(Q, m):
    Q = sorted(Q)
    n = len(Q)
    table = {}
    for i in range(n):
        table[(i, 0)] = (INF, [])

    for num_snapshots in range(1, m):
        table[(0, num_snapshots)] = (0.0, [])
        for j in range(1, n):
            #
            # look for the best cut-point
            # for the last segment
            #
            best_i = None
            best_cost = None
            best_snapshots = None
            for i in range(0, j):
                new_cost, new_s = single_snapshot(Q[i:j])
                prev_cost, prev_s = table[(i, num_snapshots-1)]
                cost = new_cost + prev_cost
                if best_cost == None or cost < best_cost:
                    best_i = i
                    best_cost = cost
                    best_snapshots = prev_s + [new_s]
            # print("Computed: (%d, %d) = %.2f" % (j, num_snapshots, best_cost))
            table[(j, num_snapshots)] = (best_cost, best_snapshots)
        print("Done with m=%d" % num_snapshots)
    return table

import time
import sys
n = int(sys.argv[1])
m = int(sys.argv[2])
Q = np.random.uniform(0, 100, n).tolist()
start = time.time()
table = optimal_snapshots(Q, m)
cost, snapshots = table[(n-1, m-1)]
t = time.time() - start
print("n=%d\tm=%d\tt=%.4f\tcost=%.2f" % (n, m, t, cost))
