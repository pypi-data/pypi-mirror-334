import numpy as np
import matplotlib.pyplot as plt

__all__ = ['compute_distance_matrix', 'total_distance', 'simulated_annealing']

def compute_distance_matrix(points):
    # Precompute a distance matrix for the given points.
    diff = points[:, np.newaxis, :] - points[np.newaxis, :, :]
    D = np.sqrt(np.sum(diff**2, axis=2))
    return D

def total_distance(tour, D):
    # Compute the total distance of the tour using the precomputed distance matrix.
    return np.sum(D[tour, np.roll(tour, -1)])

def simulated_annealing(D, initial_temperature=10000, cooling_rate=0.995,
                        stopping_temperature=1e-8, iterations_per_temp=100):
    """
    Solve the TSP using simulated annealing with a precomputed distance matrix.

    Returns:
        tuple: (best_tour, best_distance, iteration_count) where:
            - best_tour (np.ndarray): The best found tour as an array of point indices.
            - best_distance (float): The total distance of the best tour.
            - iteration_count (int): Total number of candidate iterations performed.
    """
    n = D.shape[0]
    current_tour = np.arange(n)
    np.random.shuffle(current_tour)
    current_distance = total_distance(current_tour, D)

    best_tour = current_tour.copy()
    best_distance = current_distance
    T = initial_temperature
    iteration_count = 0

    while T > stopping_temperature:
        for _ in range(iterations_per_temp):
            iteration_count += 1
            new_tour = current_tour.copy()
            i, j = np.random.choice(n, 2, replace=False)
            new_tour[i], new_tour[j] = new_tour[j], new_tour[i]

            new_distance = total_distance(new_tour, D)
            delta = new_distance - current_distance

            # Accept the new tour if it's better, or with a probability if it's worse.
            if delta < 0 or np.random.rand() < np.exp(-delta / T):
                current_tour = new_tour
                current_distance = new_distance
                if current_distance < best_distance:
                    best_tour = current_tour.copy()
                    best_distance = current_distance
        T *= cooling_rate  # Cool down
    return best_tour, best_distance, iteration_count

"""
if __name__ == '__main__':
    # Demonstration of simulated annealing usage with randomly generated points.
    np.random.seed(42)  # For reproducibility
    points = np.random.uniform(0, 100, size=(20, 2))
    
    # Precompute the distance matrix.
    D = compute_distance_matrix(points)
    
    # Solve the TSP using simulated annealing.
    best_tour, best_distance, iteration_count = simulated_annealing(D)
    
    print("Best tour:", best_tour)
    print("Best distance:", best_distance)
    print("Total candidate iterations performed:", iteration_count)"
"""