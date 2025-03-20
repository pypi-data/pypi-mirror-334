""""
=====================
A library for solving the Traveling Salesman Problem using various algorithms.
=====================
"""

__version__ = "1.0.0"

# Import core algorithm functions from the subpackage.
from .algorithms.hill_climbing import hill_climbing, calculate_distance
from .algorithms.simulated_annealing import simulated_annealing, compute_distance_matrix, total_distance
from .algorithms.random_search import random_search, calculate_distance, generate_distance_matrix, get_nearest_neighbor
from .algorithms.Asearch import astar_tsp

# Optionally, if you have additional algorithm modules, you can import them here:
# PLACEHOLDER

# Import utilities (if any) from the utils module.
from . import utils

# Define the public API for the package.
__all__ = [
    "hill_climbing",
    "calculate_distance",
    "simulated_annealing",
    "compute_distance_matrix",
    "total_distance",
    "random_search",
    "calculate_distance",
    "generate_distance_matrix",
    "get_nearest_neighbor",
    "astar_tsp",
    "utils"
]