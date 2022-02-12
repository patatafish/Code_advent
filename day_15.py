import math
import datetime
# define positive infinity for distances in dijkstra
positive_infinity = float('inf')

# file i/o
def get_data(file_name='day_15.dat'):
    with open(file_name, 'r') as inf:
        raw_data = [line for line in inf.read().split('\n')]
    my_data = []
    for lines in raw_data:
        my_data.append([int(my_item) for my_item in lines])
    return my_data


class PQ:

    def __init__(self, new_map=None):
        if not new_map:
            print('cant create empty queue')
            return
        else:
            self.queue = []
            self.list = []
            self.cost = []
            self.pos = []
            self.prev = []
            self.neighbors = []
            self.max = len(new_map)
            for y in range(len(new_map)):
                for x in range(len(new_map)):
                    self.list.append((x, y))
                    self.cost.append(new_map[y][x])
                    self.neighbors.append(valid_edges((x, y), self.max))
                    self.prev.append(-1)

    def show_myself(self):
        print('len of queue:', len(self.queue))
        print('len of list:', len(self.list))
        print('len of cost:', len(self.cost))
        print('len of pos:', len(self.pos))
        print('len of prev:', len(self.prev))
        print('len of neighbors:', len(self.neighbors))

    def insert(self, new_coord, new_cost):
        # print('adding', new_coord, new_cost, 'to PQ...')
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
        if last_index:
            temp = self.queue[0]
            self.queue[0] = self.queue[last_index]
            self.queue[last_index] = temp
            self.queue.pop(-1)
            self.sink(0)
        else:
            self.queue.pop()

    def sink(self, node):
        # print('sinking node', node, end='... ')
        if node == len(self.queue)-1:
            # print('at end, exiting')
            return
        while True:
            # print('sinking value', self.queue[node][1], end='... ')
            ll = (4 * node) + 1
            lc = (4 * node) + 2
            rc = (4 * node) + 3
            rr = (4 * node) + 4

            if ll >= len(self.queue):
                # print('no children!')
                return
            less = self.less(ll, lc, rc, rr)

            # print('checking against node:', less, 'value:', self.queue[less][1], end='... ')
            if self.queue[node][1] > self.queue[less][1]:
                # print('sinking down...')
                temp = self.queue[node]
                self.queue[node] = self.queue[less]
                self.queue[less] = temp
                node = less
                continue
            # print('done sinking.')
            break

    def less(self, a, b, c, d):
        least = a
        for x in a, b, c, d:
            if x < len(self.queue):
                if self.queue[x][1] < self.queue[least][1]:
                    least = x
            else:
                return least
        return least

    def swim(self, node):
        # print('swimming at node', node, end='... ')
        if node == 0:
            # print('at head, returning')
            return
        while True:
            # print('trying to swim with', self.queue[node][1], end='... ')
            parent_index = math.ceil((node/4)-1)
            # print('checking parent', self.queue[parent_index], end='... ')
            if self.queue[node][1] < self.queue[parent_index][1]:
                # print('swimming upstream...')
                temp = self.queue[node]
                self.queue[node] = self.queue[parent_index]
                self.queue[parent_index] = temp
                node = parent_index
                continue
            # print('done swimming.')
            break

    def show_route(self, target=None):
        if not target:
            prev = self.prev[-1]
        else:
            my_index = target[0] + (self.max * target[1])
            prev = self.prev[my_index]
        route = []
        while prev != -1:
            route.append(prev)
            prev = self.prev[prev]

        for i in range(len(self.cost)):
            if i in route:
                print(f'\x1b[6:30:42m{self.cost[i]}', end='')
            else:
                print(f'\x1b[0m{self.cost[i]}', end='')
            if i % self.max == self.max - 1:
                print('\x1b[0m')
        print()


def valid_edges(my_coord, my_max):
    my_x = my_coord[0]
    my_y = my_coord[1]
    neighbor = []
    if my_x > 0:
        neighbor.append((my_x-1, my_y))
    if my_x < my_max-1:
        neighbor.append((my_x+1, my_y))
    if my_y > 0:
        neighbor.append((my_x, my_y-1))
    if my_y < my_max-1:
        neighbor.append((my_x, my_y+1))
    return neighbor


def dijk(my_map):
    global positive_infinity
    runtime = []
    print('entering dijkstra...')
    vis = [False] * len(my_map)**2
    dist = [positive_infinity] * len(my_map)**2
    count = 0
    dist[0] = 0
    item_ind = 0
    my_q = PQ(my_map)
    my_q.insert((0, 0), 0)
    avg = datetime.datetime.now()
    while my_q.queue:
        ind = my_q.list.index(my_q.queue[0][0])
        min_val = dist[ind]
        vis[ind] = True
        if count == 5000:
            new = datetime.datetime.now()
            avg = new - avg
            count = 0
            my_q.show_route(my_q.list[ind])
            print('cost to this point:', dist[ind])
            print('size of PQ:', len(my_q.queue))
            print('time per 5k:', avg)
            my_q.show_myself()
            runtime.append([len(my_q.queue), avg])
            avg = datetime.datetime.now()
        count += 1
        for my_item in my_q.neighbors[ind]:
            item_ind = my_item[0] + (my_item[1] * len(my_map))
            if vis[item_ind] is True:
                continue
            item_dist = my_q.cost[item_ind] + min_val
            if item_dist < dist[item_ind]:
                dist[item_ind] = item_dist
                my_q.prev[item_ind] = ind
                my_q.insert(my_q.list[item_ind], item_dist)
        if item_ind == len(my_map)**2-1:
            print('I think I found the exit node.')
            break
        my_q.poll()

    my_q.show_route()
    print('exit cost:', dist[-1])
    print('cost table:')
    for line in runtime:
        print(line)


def grow_data(my_map):
    print('growing data...')
    factor = 4
    row_len = len(my_map[0])
    for row in my_map:
        for i in range(factor):
            temp = row[-row_len:]
            for my_item in temp:
                my_next = my_item+1
                if my_next > 9:
                    my_next = 1
                row.append(my_next)

    target = len(my_map)*factor
    count = 0
    while count < target:
        new_row = []
        for my_item in my_map[count]:
            my_next = my_item + 1
            if my_next > 9:
                my_next = 1
            new_row.append(my_next)
        my_map.append(new_row)
        count += 1

    return my_map


if __name__ == "__main__":

    start_time = datetime.datetime.now()

    print('starting at', start_time)
    data = get_data()

    # if input('Should I expand the map? y/n?') is 'y':
    data = grow_data(data)

    dijk(data)

    end_time = datetime.datetime.now()
    elapsed_time = end_time - start_time

    print('finished at', end_time)
    print('total seconds elapsed:', elapsed_time)

    print('\n\nExiting...')
