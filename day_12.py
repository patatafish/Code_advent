# file i/o
with open("day_12.dat", "r") as inf:
    raw_data = [line for line in inf.read().split('\n')]
del inf
# print(raw_data)
# parse data to list of lists
# format is [ [start node, end node], [start node, end node], ... [start node, end node] ]
map_data = []
raw_item = None
for raw_item in raw_data:
    # print(item)
    map_data.append([x for x in raw_item.split('-')])
del(raw_item, raw_data)


print(map_data)


class Node:

    def __init__(self, my_name=None):
        self.name = my_name
        if self.name == 'start' or self.name == 'end':
            self.type = self.name
        else:
            if self.name.isupper():
                self.type = 'MAJ'
            else:
                self.type = 'MIN'
        self.link = []

    def add_link(self, my_link=None):
        if my_link is None:
            print("Must supply link to add!")
        # we don't ever consider revisiting start, so don't link it here
        elif my_link.name == 'start':
            return
        else:
            self.link.append(my_link)


class Map:

    def __init__(self, my_name=None):
        if my_name is None:
            raise Exception('You must name the map')
        else:
            self.name = my_name
            self.content = []
            self.start = None
            self.end = None

    def __contains__(self, item):
        if not self.content:
            return False
        # print('called in')
        for my_node in self.content:
            # print(f' checking {my_node.name}')
            if item == my_node.name:
                return True
        return False

    def append(self, new_node=None):
        if new_node is None:
            raise Exception('You cannot add empty node')
        elif type(new_node) is not Node:
            raise Exception('You cannot add a non-node type')
        else:
            self.content.append(new_node)
            if new_node.type == 'start':
                self.start = new_node
            if new_node.type == 'end':
                self.end = new_node

    def address(self, node_name=None):
        for nodes in self.content:
            if node_name == nodes.name:
                return nodes
        return None


def list_routes(my_map, current_node=None, trail=''):
    global path_count
    global small_revisit
    global all_items

    # if we are entering the loop for the first time, set current node as start of map
    if current_node is None:
        current_node = my_map.start

    # get the list of items the current node is linked to
    my_links = current_node.link

    # append the name of the current node to our trail
    trail += current_node.name

    # if we reached the end of the map, exit the loop and return
    if current_node is not my_map.end:
        trail += '->'
    else:
        path_count += 1
        all_items.append(trail)
        print(trail)
        return

    # if we are not at the end, loop through all links of current node
    for next_node in my_links:
        # first check that we are not revisiting small caves
        if next_node.type == 'MIN' and next_node.name in trail:
            if small_revisit is True:
                continue
            else:
                small_revisit = True
                list_routes(my_map, next_node, trail)
                small_revisit = False
        # we are not looking at a small cave we've seen,
        # check we are not looping big caves
        # elif trail[-12:-10] == trail[-4:-2] and trail[-8:-6] == next_node.name:
            # continue
        else:
            list_routes(my_map, next_node, trail)


# list of established nodes with links
my_map = Map('my map')

# global for path count
path_count = 0
small_revisit = False
all_items = []

# loop through data to create map nodes
for pairs in map_data:
    # print(f'creating {pairs[0]} and {pairs[1]}')
    for each in pairs:
        if each not in my_map:
            # print(f'{each} is new item')
            my_map.append(Node(each))
        # else:
            # print(f'{each} node already defined')

# loop through data to create node links
for pairs in map_data:
    # print(f'linking {pairs[0]} and {pairs[1]}')
    for node in my_map.content:
        if node.name == pairs[0]:
            node.add_link(my_map.address(pairs[1]))
        if node.name == pairs[1]:
            node.add_link(my_map.address(pairs[0]))


# start loop to find routes through map
list_routes(my_map)
print(path_count)
print(len(all_items))


print('\n\nexiting')
