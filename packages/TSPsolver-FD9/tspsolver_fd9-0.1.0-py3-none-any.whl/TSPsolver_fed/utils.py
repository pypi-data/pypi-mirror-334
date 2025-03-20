"""
Module: utils
Part of the TSPsolver_fd9 package.

This module provides utility functions for the TSP solver,
including loading TSP data from a CSV file, plotting TSP tours,
and generating random points for testing.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def load_points_from_csv(csv_filename, columns=('x', 'y')):
    #Load TSP points from a CSV file.
    if os.path.exists(csv_filename):
        try:
            df = pd.read_csv(csv_filename)
            # Check if the expected columns exist.
            if all(col in df.columns for col in columns):
                points = df[list(columns)].to_numpy()
                print(f"Loaded {len(points)} points from {csv_filename}.")
                return points
            else:
                raise ValueError(f"CSV file does not contain the expected columns: {columns}")
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return None
    else:
        print(f"CSV file '{csv_filename}' not found.")
        return None

def generate_random_points(num_points=20, lower=0, upper=100):
    # Generate a random set of points for TSP testing.
    return np.random.uniform(lower, upper, size=(num_points, 2))

def get_points(csv_filename, num_points=20, lower=0, upper=100, columns=('x', 'y')):
    # Attempt to load TSP points from a CSV file. If the file is not found or an error occurs,
    # generate a set of random points.
    points = load_points_from_csv(csv_filename, columns)
    if points is None:
        print("Generating random points instead.")
        points = generate_random_points(num_points, lower, upper)
    return points

#Plot a TSP tour given the set of points and the tour order.
def plot_tour(points, tour, title="TSP Tour", figsize=(8, 6)):
    # Create the tour by appending the starting point to the end.
    tour_points = np.vstack((points[tour], points[tour[0]]))
    plt.figure(figsize=figsize)
    plt.plot(tour_points[:, 0], tour_points[:, 1], marker='o', linestyle='-')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(title)
    plt.show()

"""
if __name__ == '__main__':
    # Demo for the utility functions.
    print("Utility Module Demo:")
    
    # Attempt to load points from a CSV file; if not found, random points will be generated.
    csv_file = "TSP_Large_Dataset__500_Cities__-_Primary.csv"
    points = get_points(csv_file, num_points=10)
    print("Points used:")
    print(points)
    
    # Plot the tour with the points in their natural order.
    tour = np.arange(len(points))
    plot_tour(points, tour, title="Demo TSP Tour")
"""