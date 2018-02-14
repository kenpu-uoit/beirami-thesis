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

def optimal_snapshots(Q, m):
    Q = sorted(Q)
    n = len(Q)
    table = {}
    for i in range(n):
        table[(i, 0)] = (0.0, [])

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
                print("debug: %s, %s => %.2f" % (i, j, new_cost))
                prev_cost, prev_s = table[(i, num_snapshots-1)]
                cost = new_cost + prev_cost
                if best_cost == None or cost < best_cost:
                    best_i = i
                    best_cost = cost
                    best_snapshots = prev_s + [new_s]
            print("Computed: (%d, %d) = %.2f" % (j, num_snapshots, best_cost))
            table[(j, num_snapshots)] = (best_cost, best_snapshots)
    return table

n = 10
m = 10
Q = np.random.uniform(0, 100, n).tolist()
table = optimal_snapshots(Q, m)
print("Done")
