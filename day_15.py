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


class PQ():

    def __init__(self, new_map=None):
        if not new_map:
            print('cant create empty queue')
            return None
        else:
            self.queue = []
            self.list = []
            self.cost = []
            self.pos = []
            self.inv = []
            self.max = len(new_map)
            for y in range(len(new_map)):
                for x in range(len(new_map)):
                    self.list.append((x,y))
                    self.cost.append(new_map[x][y])

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

    def poll(self):
        last_index = len(self.queue)-1
        temp = self.queue[0]
        self.queue[0] = self.queue[last_index]
        self.queue[last_index] = temp
        self.queue.pop(-1)
        self.sink(0)

    def sink(self, node):
        print('sinking node', node)
        if node == len(self.queue)-1:
            print('at end, exiting')
            return
        lc = (2*node)+1
        rc = (2*node)+2

        if rc >= len(self.queue):
            rc = None
            less = lc
        elif self.queue[lc][1] <= self.queue[rc][1]:
            less = lc
        else:
            less = rc
        while True:
            if self.queue[node][1] < self.queue[less][1]:
                None
            break


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

def valid_edges(my_coord, max):
    my_x = my_coord[0]
    my_y = my_coord[1]
    neighbor = []
    if my_x > 0:
        neighbor.append((my_x-1, my_y))
    if my_x < max-1:
        neighbor.append((my_x+1, my_y))
    if my_y > 0:
        neighbor.append((my_x, my_y-1))
    if my_y < max-1:
        neighbor.append((my_x, my_y+1))
    return neighbor


def dijk(my_map):
    global positive_infinity
    print('entering dijkstra...', end='')
    vis = [False] * len(my_map)**2
    prev = [None] * len(my_map)**2
    dist = [positive_infinity] * len(my_map)**2
    dist[0] = 0
    my_q = PQ(my_map)
    my_q.insert((0,0), 0)
    while my_q.queue:
        ind = my_q.list.index(my_q.queue[0][0])
        min_val = my_q.cost[ind]
        vis[ind] = True
        neighbors = valid_edges(my_q.list[ind], my_q.max)
        for item in neighbors:
            item_ind = my_q.list.index(item)
            item_dist = dist[ind] + min_val
            if vis[item_ind] is True:
                continue
            if item_dist < dist[item_ind]:
                dist[item_ind] = item_dist
                my_q.insert(my_q.list[item_ind], my_q.cost[item_ind])
        my_q.poll()

    my_q.print()






if __name__ == "__main__":

    data = get_data()
    dijk(data)


    print('\n\nExiting...')
