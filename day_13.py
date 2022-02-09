# file i/o
with open('day_13.dat', 'r') as inf:
    raw_data = [line for line in inf.read().split('\n')]
# print(raw_data)
# block to clean and process data for program
# find the index of the split line
split = raw_data.index('')
# print(split)
# make new lists of coordinates and folds
raw_coord_data = raw_data[:split]
raw_fold_data = raw_data[split+1:]
# print(raw_coord_data)
# print(raw_fold_data)
# split coordinates into pairs
coord_data = []
for line in raw_coord_data:
    x, y = line.split(',')
    coord_data.append([int(x), int(y)])
    del(line, x, y)
# coord_data = [item.split(',') for item in raw_coord_data]
# print(coord_data)
# clean fold data for processing
fold_data = []
for line in raw_fold_data:
    string, integer = line.split('=')
    fold_data.append([string[-1], int(integer)])
    del(line, string, integer)
# print(fold_data)
# data cleaning
del(inf, raw_data, raw_coord_data, raw_fold_data, split)

height = 0
length = 0
for line in coord_data:
    if line[0] > length:
        # print('new max len', line[0])
        length = line[0]
    if line[1] > height:
        # print('new max hih', line[1])
        height = line[1]

# add one to each length and height for indexing
height += 1
length += 1

# print('len', length, 'hih', height)

clean_grid = []
for y in range(height):
    clean_grid.append([])
    for x in range(length):
        clean_grid[y].append('.')

for line in coord_data:
    my_x = line[0]
    my_y = line[1]
    clean_grid[my_y][my_x] = '*'


def show_grid(my_grid):
    count = 0
    for y in range(height):
        print('{:>4}'.format(y), end=' ')
        for x in range(length):
            print(my_grid[y][x], end='')
            if my_grid[y][x] == '*':
                count += 1
        print()
    print("Count:", count)


def fold_y(my_grid, axis):
    global length
    global height


    for i in range(length):
        my_grid[axis][i] = '-'
    show_grid(my_grid)

    for i in range(axis):
        top_line = 0+i
        bottom_line = height-1-i

        combined_line = []
        for j in range(length):
            if my_grid[top_line][j] == '*' or my_grid[bottom_line][j] == '*':
                combined_line.append('*')
            else:
                combined_line.append('.')

        my_grid[top_line] = combined_line


    del my_grid[axis:]
    height = axis
    return my_grid


def fold_x(my_grid, axis):
    global length
    global height

    for i in range(height):
        my_grid[i][axis] = '|'
    show_grid(my_grid)

    for i in range(axis):
        left_line = 0+i
        right_line = length-1-i

        # print('com', left_line, right_line)

        for j in range(height):
            if my_grid[j][left_line] == '*' or my_grid[j][right_line] == '*':
                my_grid[j][left_line] = '*'
            del my_grid[j][right_line]

    length = axis

    return my_grid


show_grid(clean_grid)
for pairs in fold_data:
    if pairs[0] == 'y':
        clean_grid = fold_y(clean_grid, pairs[1])
    else:
        clean_grid = fold_x(clean_grid, pairs[1])
    show_grid(clean_grid)

print('\n\nExiting...')
