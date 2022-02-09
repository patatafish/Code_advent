import time
import tkinter as tk

# file i/o
def get_data(file_name='day_15.dat'):
    with open(file_name, 'r') as inf:
        raw_data = [line for line in inf.read().split('\n')]
    my_data = []
    for lines in raw_data:
        my_data.append([int(item) for item in lines])
    return my_data


def traverse_map(my_map=None, shortest_route=None, local_route=None):
    if not shortest_route:
        shortest_route = [len(my_map) * len(my_map) * 9]
    if not local_route:
        local_route = [0, [0,0]]


    box_size = len(my_map)
    x = local_route[-1][0]
    y = local_route[-1][1]

    # on call, if our current route total is more than the shortest
    # found route, do not finish path, just break loop
    if local_route[0] > shortest_route[0]:
        print('.', end='')
        return shortest_route

    # on call, if we've reached the bottom right, this is the end of the route
    # check on the length and compare to the current shortest found
    if x == y and x == box_size-1:
        if local_route[0] < shortest_route[0]:
            shortest_route = local_route
        print()
        show_grid(my_map, local_route, shortest_route[0])
        return shortest_route



    if x+1 < box_size and ([x+1, y] not in local_route):
        local_copy = []
        for pairs in local_route:
            local_copy.append(pairs)
        local_copy[0] += my_map[y][x+1]
        local_copy.append([x+1, y])
        shortest_route = traverse_map(my_map, shortest_route, local_copy)
    if y+1 < box_size and ([x, y+1] not in local_route):
        local_copy = []
        for pairs in local_route:
            local_copy.append(pairs)
        local_copy[0] += my_map[y+1][x]
        local_copy.append([x, y+1])
        shortest_route = traverse_map(my_map, shortest_route, local_copy)
    if x-1 >= 0 and ([x-1, y] not in local_route):
        local_copy = []
        for pairs in local_route:
            local_copy.append(pairs)
        local_copy[0] += my_map[y][x-1]
        local_copy.append([x-1, y])
        shortest_route = traverse_map(my_map, shortest_route, local_copy)
    if y-1 >= 0 and ([x, y-1] not in local_route):
        local_copy = []
        for pairs in local_route:
            local_copy.append(pairs)
        local_copy[0] += my_map[y-1][x]
        local_copy.append([x, y-1])
        shortest_route = traverse_map(my_map, shortest_route, local_copy)

    return shortest_route


def show_grid(my_map, my_route, my_max):
    x = my_route[-1][0]
    y = my_route[-1][1]
    print('Current length:', my_route[0])
    for i in range(len(my_map)):
        for j in range(len(my_map[i])):
            if y == i and x == j:
                print(f'\x1b[6;30;43m{my_map[i][j]:>2}\x1b[0m', end='')
            elif [j, i] in my_route:
                print(f'\x1b[0;30;47m{my_map[i][j]:>2}\x1b[0m', end='')
            else:
                print(f'{my_map[i][j]:>2}', end='')

        print()
    print('Current Shortest:', my_max)
    print('***************************************\n')



if __name__ == "__main__":

    data = get_data()

    quickest = traverse_map(data)

    print(quickest)