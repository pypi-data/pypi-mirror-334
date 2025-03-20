import math
import numpy as np

__all__ = [
    "random_search",
    "calculate_distance",
    "generate_distance_matrix",
    "get_nearest_neighbor",
]

def calculate_distance(city1, city2):
    #Compute the Euclidean distance between two cities.
    return math.sqrt((city2[0] - city1[0])**2 + (city2[1] - city1[1])**2)

def generate_distance_matrix(cities):
    #Generate a distance matrix for a set of cities.
    n = len(cities)
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            D[i, j] = calculate_distance(cities[i], cities[j])
    return D

def get_nearest_neighbor(city, D, visited):
    #Find the nearest unvisited city.
    n = D.shape[0]
    min_distance = np.inf
    nearest = city
    for i in range(n):
        if i == city or i in visited:
            continue
        if D[city, i] < min_distance:
            min_distance = D[city, i]
            nearest = i
    return min_distance, nearest

def random_search(cities):
    #Perform a nearest-neighbor search on the given set of cities.
    D = generate_distance_matrix(cities)
    visited = set()
    current = 0
    path = [current]
    total_cost = 0
    visited.add(current)
    
    while len(visited) < len(cities):
        min_dist, nearest = get_nearest_neighbor(current, D, visited)
        total_cost += min_dist
        current = nearest
        visited.add(current)
        path.append(current)
    
    total_cost += D[current, path[0]]  # add cost to return to starting city
    return path, total_cost