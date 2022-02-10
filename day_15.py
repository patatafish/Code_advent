import math
# define positive infinity for distances in dijkstra
import random

positive_infinity = float('inf')

# file i/o
def get_data(file_name='test.dat'):
    with open(file_name, 'r') as inf:
        raw_data = [line for line in inf.read().split('\n')]
    my_data = []
    for lines in raw_data:
        my_data.append([int(item) for item in lines])
    return my_data

class Node():

    def __init__(self):
        # print('creating empty node...')
        self.name = None
        self.cost = None
        self.edges = []

    def build_edge(self, my_x, my_y, max):
        print('discovering valid edges for', self.name, end = ' ')
        if my_x > 0:
            self.edges.append((my_x-1, my_y))
        if my_y > 0:
            self.edges.append((my_x, my_y-1))
        if my_x < max-1:
            self.edges.append((my_x+1, my_y))
        if my_y < max-1:
            self.edges.append((my_x, my_y+1))
        print('I think', self.edges, 'are valid...')

class Map():

    def __init__(self, my_data=None):
        if not my_data:
            print('created an empty map...')
        else:
            self.nodes = []
            self.size = 0
            print('building map from data...')
            max = len(my_data)
            print('building nodes and adjacencies...', end='')
            for i in range(max):
                for j in range(max):
                    print('.', end='')
                    # create the empty node
                    new_node = Node()
                    # name coords
                    new_node.name = (j, i)
                    # record cost to enter node
                    new_node.cost = my_data[i][j]
                    # establish edges
                    new_node.build_edge(i, j, max)
                    self.nodes.append(new_node)
                    self.size += 1
            print(' new map with', self.size, 'nodes')

class PQ():

    def __init__(self):
        self.queue = []

    def insert(self, new_coord, new_cost):
        print('adding', new_coord, new_cost, 'to PQ...')
        self.queue.append([new_coord, new_cost])
        self.swim(len(self.queue)-1)

    def print(self):
        print('\nThis queue contains:')
        for i in range(len(self.queue)):
            print(self.queue[i])
            if i % 11 == 0 and i != 0:
                print()

    def swim(self, node):
        print('swimming at node', node)
        if node == 0:
            print('at head, returning')
            return
        while True:
            print('trying to swim with', self.queue[node][1])
            parent_index = math.ceil((node/2)-1)
            print('checking parent', self.queue[parent_index])
            if self.queue[node][1] < self.queue[parent_index][1]:
                print('swimming upstream...')
                temp = self.queue[node]
                self.queue[node] = self.queue[parent_index]
                self.queue[parent_index] = temp
                node = parent_index
                continue
            break


def dijk(my_map):
    global positive_infinity
    print('entering dijkstra...', end='')
    vis = [False] * my_map.size
    prev = [None] * my_map.size
    dist = [positive_infinity] * my_map.size
    dist[0] = 0
    my_q = PQ()
    my_q.insert((0,0), 0)
    while my_q:
        index = my_q.queue.

    my_q.print()






if __name__ == "__main__":

    data = get_data()
    map = Map(data)

    dijk(map)


    print('\n\nExiting...')
