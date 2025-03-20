import numpy as np
from TSPsolver_fed.algorithms.random_search import random_search
from TSPsolver_fed.algorithms.hill_climbing import hill_climbing
from TSPsolver_fed.algorithms.simulated_annealing import simulated_annealing, compute_distance_matrix
from TSPsolver_fed.algorithms.Asearch import astar_tsp

if __name__ == "__main__":
    # Example list of cities as (x, y) coordinates.
    cities = [(0, 0), (2, 3), (5, 4), (6, 1), (8, 3), (1, 6)]
    cities_array = np.array(cities)

    # Random Search: Nearest-neighbor approach.
    rs_path, rs_cost = random_search(cities_array)
    
    # Hill Climbing algorithm.
    hc_route, hc_cost = hill_climbing(cities_array)
    
    # Simulated Annealing:
    # Compute the distance matrix first.
    D = compute_distance_matrix(cities_array)
    sa_route, sa_cost, sa_iterations = simulated_annealing(D, initial_temperature=1000, cooling_rate=0.995)
    
    # A* Search:
    a_route, a_cost = astar_tsp(D)

    # Print the results.
    print("Random Search:", (rs_path, rs_cost))
    print("Hill Climbing:", (hc_route, hc_cost))
    print("Simulated Annealing:", (sa_route, sa_cost))
    print("A* Search:", (a_route, a_cost))

    # Display example usage (as documentation).
    print('''Example Usage

    from TSPsolver_fd9.utils import generate_random_cities
    from TSPsolver_fd9.algorithms.random_search import random_search
    from TSPsolver_fd9.algorithms.hill_climbing import hill_climbing
    from TSPsolver_fd9.algorithms.simulated_annealing import simulated_annealing
    from TSPsolver_fd9.algorithms.Asearch import astar_tsp

    cities = [(0, 0), (2, 3), (5, 4), (6, 1), (8, 3), (1, 6)]

    print("Random Search:", random_search(cities))
    print("Hill Climbing:", hill_climbing(cities))
    print("Simulated Annealing:", simulated_annealing(cities, temp=1000, cooling_rate=0.995))
    print("A* Search:", astar_tsp(cities))
    ''')
