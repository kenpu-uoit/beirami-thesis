import numpy as np
import matplotlib.pyplot as pyplot

def make_queries():
    Q = np.vstack([
        np.random.normal(4, 4, (20, 1)),
        np.random.normal(40, 4, (20, 1))
        ])
    a, b = np.min(Q), np.max(Q)
    Q = np.vstack([Q, np.random.uniform(a, b, (10, 1))])
    Q = Q - np.min(Q)
    return np.squeeze(Q)

def make_snapshots(Q):
    a, b = np.min(Q), np.max(Q)
    return np.random.uniform(a, b, 5)


def time_cost(Q, S):
    S = np.array(S)
    nQ = Q.shape[0]
    nS = S.shape[0]
    d = np.zeros((nQ, nS))
    for i in range(nQ):
        q = Q[i]
        d[i, :] = np.abs(S - q)
    c = np.min(d, axis=1)
    return np.sum(c)

#
# Plot cost for a single snapshot placement
#
def plot_queries(Q):
    pyplot.figure()
    pyplot.plot(Q, np.zeros(Q.shape), '*')
    pyplot.savefig('Q.png')


#
# Plot cost for |S| = 1
#
def plot_k1(Q):
    tmax = np.max(Q) * 1.5
    ts = np.linspace(0, tmax, 100)
    cost = [time_cost(Q, [s]) for s in ts]
    pyplot.figure()
    pyplot.plot(Q, np.zeros(Q.shape), '*')
    pyplot.plot(ts, cost, '--')
    pyplot.savefig('K1.png')


#
# Plot cost for adding one more s
#
def plot_add_one(Q, S):
    tmax = np.max(Q) * 1.5
    ts = np.linspace(0, tmax, 100)
    cost = [time_cost(Q, np.concatenate([S, [t]])) for t in ts]
    pyplot.figure()
    pyplot.plot(Q, np.zeros(Q.shape), '*')
    pyplot.plot(S, np.ones(S.shape), '+', color='red')
    pyplot.plot(ts, cost, '--')
    pyplot.savefig('add_one.png')

Q = make_queries()
S = make_snapshots(Q)

plot_queries(Q)
plot_k1(Q)
plot_add_one(Q, S)


