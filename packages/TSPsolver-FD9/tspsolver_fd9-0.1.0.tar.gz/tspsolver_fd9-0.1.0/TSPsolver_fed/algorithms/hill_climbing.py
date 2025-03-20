import numpy as np
import random

__all__ = ['hill_climbing', 'calculate_distance']

def calculate_distance(route):
    """
    Calculate the total distance of a given route.

    Returns:
        float: The total Euclidean distance of the tour.
    """

    # Append the starting city to the end to complete the tour.
    route_extended = np.append(route, [route[0]], axis=0)
    # Compute Euclidean distances between consecutive cities.
    return np.sum(np.sqrt(np.sum(np.diff(route_extended, axis=0)**2, axis=1)))

def create_initial_route(cities):
    """
    Create a random initial route from the provided cities.

    Returns:
        np.ndarray: A randomly shuffled route.
    """
    return np.array(random.sample(list(cities), len(cities)))

def get_neighbors(route):
    """
    Generate all neighbor routes by swapping two cities in the current route.

    Returns:
        list: A list of neighbor routes, each as a NumPy array.
    """
    neighbors = []
    n = len(route)
    for i in range(n):
        for j in range(i + 1, n):
            neighbor = route.copy()
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            neighbors.append(neighbor)
    return neighbors

def hill_climbing(cities):
    """
    Solve the Traveling Salesman Problem using a hill-climbing algorithm.

    Returns:
        tuple: (best_route, best_distance)
            - best_route (np.ndarray): The best route found.
            - best_distance (float): The total distance of the best route.
    """
    current_route = create_initial_route(cities)
    current_distance = calculate_distance(current_route)

    while True:
        neighbors = get_neighbors(current_route)
        next_route = min(neighbors, key=calculate_distance)
        next_distance = calculate_distance(next_route)
        
        if next_distance >= current_distance:
            break
        
        current_route, current_distance = next_route, next_distance

    return current_route, current_distance
