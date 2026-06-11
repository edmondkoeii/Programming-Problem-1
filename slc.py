class DisjointSetForest:
    def __init__(self):
        self.parent = {}
        self.rank = {}

    def make_set(self, x):
        self.parent[x] = x
        self.rank[x] = 0

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1


def slc(graph, d, k):
    nodes = list(graph.nodes)
    edges = list(graph.edges)

    edges_sorted = sorted(edges, key=lambda e: d(e))

    dsf = DisjointSetForest()
    for node in nodes:
        dsf.make_set(node)

    num_components = len(nodes)

    for edge in edges_sorted:
        if num_components == k:
            break
        u, v = edge
        if dsf.find(u) != dsf.find(v):
            dsf.union(u, v)
            num_components -= 1

    clusters = {}
    for node in nodes:
        root = dsf.find(node)
        clusters.setdefault(root, set()).add(node)

    return frozenset(frozenset(cluster) for cluster in clusters.values())
