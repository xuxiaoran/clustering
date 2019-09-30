"""
Author: Xiaoran Xu
BU: xiaorxu
CS506 - Extra Credit
"""


from collections import defaultdict
from math import inf
import random
import csv
import math


def point_avg(points):
    """
    Accepts a list of points, each with the same number of dimensions.
    (points can have more dimensions than 2)
    
    Returns a new point which is the center of all the points.
    """

    #https://stackoverflow.com/questions/3223043/how-do-i-sum-the-columns-in-2d-list
    sum_pts = [sum(x) for x in zip(*points)]
    return [col_sum /len(points) for col_sum in sum_pts]

def update_centers(data_set, assignments):
    """
    Accepts a dataset and a list of assignments; the indexes 
    of both lists correspond to each other.
    Compute the center for each of the assigned groups.
    Return `k` centers in a list
    """

    cluster_points = {}
    for point, assignment in zip(data_set, assignments):
        if not assignment in cluster_points.keys():
            cluster_points[assignment] = []
        cluster_points[assignment].append(point)

    centers = []
    for k in cluster_points.keys():
        centers.append(point_avg(cluster_points[k]))

    return centers


def assign_points(data_points, centers):
    """
    """
    assignments = []
    for point in data_points:
        shortest = inf  # positive infinity
        shortest_index = 0
        for i in range(len(centers)):
            val = distance(point, centers[i])
            if val < shortest:
                shortest = val
                shortest_index = i
        assignments.append(shortest_index)
    return assignments


def distance(a, b):
    """
    Returns the Euclidean distance between a and b
    """
    temp = 0
    for i,j in zip(a,b):
        temp += (i-j)**2
    return math.sqrt(temp)


def generate_k(data_set, k):
    """
    Given `data_set`, which is an array of arrays,
    return a random set of k points from the data_set
    """
    return random.sample(data_set, k)


def get_list_from_dataset_file(dataset_file):
    data = []
    with open(dataset_file, newline = '') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            data.append([int(r) for r in row])
    return data

def cost_function(clustering):
    cost = 0
    for k,points in clustering.items():
        center = point_avg(points)
        for point in points:
            cost += distance(center, point)
    return cost


def k_means(dataset_file, k):
    dataset = get_list_from_dataset_file(dataset_file)
    k_points = generate_k(dataset, k)
    assignments = assign_points(dataset, k_points)
    old_assignments = None
    while assignments != old_assignments:
        new_centers = update_centers(dataset, assignments)
        old_assignments = assignments
        assignments = assign_points(dataset, new_centers)
    clustering = defaultdict(list)
    for assignment, point in zip(assignments, dataset):
        clustering[assignment].append(point)
    return clustering
