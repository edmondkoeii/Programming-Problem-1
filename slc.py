# Disjoint Set Forest (from course-provided gist)
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
    """
    Single linkage clustering using Kruskal's algorithm.

    Builds an MST by greedily adding the cheapest edge that connects
    two different components. Stops early when exactly k components remain,
    returning those components as the clusters.

    Args:
        graph: dsc40graph.UndirectedGraph instance
        d: distance function that takes a tuple (u, v) and returns a number
        k: desired number of clusters

    Returns:
        frozenset of k frozensets, each representing one cluster
    """
    nodes = list(graph.nodes)
    edges = list(graph.edges)

    # Sort edges by distance
    edges_sorted = sorted(edges, key=lambda e: d(e))

    # Initialize DSF — one component per node
    dsf = DisjointSetForest()
    for node in nodes:
        dsf.make_set(node)

    num_components = len(nodes)

    # Kruskal's: merge components until we have exactly k
    for edge in edges_sorted:
        if num_components == k:
            break
        u, v = edge
        if dsf.find(u) != dsf.find(v):
            dsf.union(u, v)
            num_components -= 1

    # Collect nodes into clusters by their root
    clusters = {}
    for node in nodes:
        root = dsf.find(node)
        clusters.setdefault(root, set()).add(node)

    return frozenset(frozenset(cluster) for cluster in clusters.values())
