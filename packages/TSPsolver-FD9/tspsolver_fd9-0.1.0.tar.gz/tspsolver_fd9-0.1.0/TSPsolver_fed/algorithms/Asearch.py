import numpy as np
import heapq

__all__ = ['astar_tsp']

def mst_cost(unvisited, D):
    # Compute MST cost for unvisited nodes using Prim's algorithm.
    if not unvisited:
        return 0
    nodes = list(unvisited)
    mst, total = {nodes[0]}, 0
    rem = set(nodes[1:])
    while rem:
        best, best_node = float('inf'), None
        for u in mst:
            for v in rem:
                if D[u, v] < best:
                    best, best_node = D[u, v], v
        total += best
        mst.add(best_node)
        rem.remove(best_node)
    return total

def heuristic(curr, unvisited, D, start):
    # Estimate remaining cost: MST cost + min edge from current + min edge from start.
    if not unvisited:
        return D[curr, start]
    return mst_cost(unvisited, D) + min(D[curr, u] for u in unvisited) + min(D[start, u] for u in unvisited)

def astar_tsp(D, start=0):
    n = D.shape[0]
    # Each state: (priority, cost_so_far, current_city, visited_set, route)
    init_state = (heuristic(start, set(range(n)) - {start}, D, start), 0, start, frozenset({start}), [start])
    pq = [init_state]
    best_cost, best_route = float('inf'), None
    while pq:
        prio, cost, curr, visited, route = heapq.heappop(pq)
        if len(visited) == n:  # All cities visited; add cost to return to start.
            total = cost + D[curr, start]
            if total < best_cost:
                best_cost, best_route = total, route + [start]
            continue
        for city in set(range(n)) - visited:
            new_cost = cost + D[curr, city]
            new_visited = visited | {city}
            new_route = route + [city]
            new_prio = new_cost + heuristic(city, set(range(n)) - new_visited, D, start)
            if new_prio < best_cost:
                heapq.heappush(pq, (new_prio, new_cost, city, new_visited, new_route))
    return best_route, best_cost