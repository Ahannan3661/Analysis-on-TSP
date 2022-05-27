import os
import random
import math

import matplotlib.pyplot as plt
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree
from tsp import TSPSolver


RESULTS_DIR = 'results'
DATA_DIR = 'tsp'
operations = 0

class TSPSolver(object):
    global operations
    nodes = set()
    operations += 1
    partial_tour = []
    operations += 1
    distances = {}
    operations += 1

    def __init__(self, nodes, distances):
        global operations
        self.nodes = nodes
        operations += 1
        self.distances = distances
        operations += 1
        self.partial_tour = []
        operations += 1

    def initialize(self):
        raise NotImplementedError

    def select(self):
        raise NotImplementedError

    def insert(self):
        raise NotImplementedError

    def run(self):
        global operations
        self.partial_tour = []
        operations += 1
        self.initialize()
        while len(self.partial_tour) < len(self.nodes):
            selected = self.select()
            self.insert(selected)
        self.solution = self.partial_tour + [self.partial_tour[0]]
        operations += 1
        return self.solution

    def get_remaining_nodes(self):
        global operations
        operations += 1
        return self.nodes - set(self.partial_tour)

    def get_nearest_remaining_node(self, given_node):
        global operations
        remaining_nodes = self.get_remaining_nodes()
        node_distances = self.distances[given_node]
        operations += 1
        remaining_distances =  {node:node_distances[node] for node in remaining_nodes}
        operations += len(remaining_nodes)
        return min(remaining_distances, key=remaining_distances.get)

class NearestInsertionSolver(TSPSolver):
    def initialize(self):
        global operations
        starting_node = random.choice(tuple(self.nodes))
        operations += 1
        self.partial_tour.append(starting_node)
        operations += 1
        next_node = self.get_nearest_remaining_node(starting_node)
        self.partial_tour.append(next_node)
        operations += 1

    def select(self):
        global operations
        remaining_nodes = self.get_remaining_nodes()
        operations += 1
        return random.choice(tuple(remaining_nodes))

    def get_insertion_metric(self, node, insert_after, insert_before):
        global operations
        metric = self.distances[node][insert_after] + self.distances[node][insert_before] - self.distances[insert_after][insert_before]
        operations += 1
        return metric

    def insert(self, node):
        global operations
        insert_index = 1
        operations += 1
        metrics = []
        operations += 1
        minimized_metric = self.get_insertion_metric(node, self.partial_tour[0], self.partial_tour[1])
        for i in range(0,len(self.partial_tour)-1):
            metric = self.get_insertion_metric(node, self.partial_tour[i], self.partial_tour[i+1])
            metrics.append(metric)
            operations += 1
            if metric < minimized_metric:
                minimized_metric = metric
                operations += 1
                insert_index = i + 1
                operations += 1
        self.partial_tour.insert(insert_index, node)

def euclidean_dist(location1, location2):
  global operations
  operations += 1
  return math.sqrt(float(((location1[0] - location2[0])**2) + ((location1[1] - location2[1])**2)))

def read_data(size):
    
  points = {}
  
  for counter in range(size):
      points[counter] = (random.randrange(0, 50), random.randrange(0, 50))
      

  distances = {}
  
  
  for point1, location1 in points.items():
      for point2, location2 in points.items():
          distance = euclidean_dist(location1, location2)
          if not point1 in distances:
              distances[point1] = {}
              
          if not point2 in distances:
              distances[point2] = {}
              
          distances[point1][point2] = distance
          
          distances[point2][point1] = distance
          
  return (points, distances)

def solve_and_plot(size):
    
    global operations
    
    node_locations, node_distances = read_data(size)

    node_labels = set(node_locations.keys())
    operations += 1
    ni_solver = NearestInsertionSolver(node_labels, node_distances)
    ni_solution = ni_solver.run()
    
        
    #print(ni_solution)
    
		

if __name__ == "__main__":
    
    limitt = 500
    
    inputSize = 3
    
    inputs = []
    steps = []
    
    for i in range(limitt):
        solve_and_plot(inputSize)
        inputs.append(inputSize)
        steps.append(operations)
        inputSize += 1
        operations = 0
    
    plt.plot(inputs, steps, 'r', label='Operations', linewidth=2) 
    
    plt.xlabel('Size Of Input') 

    plt.ylabel('Operations')

    plt.title('Complexity')
 
    plt.savefig("output.png")
    
    plt.show()