raw_data = open("day_05.dat", "r").readlines()

def find_largest(my_list):
    big = 0
    for num in my_list:
        if num > big:
            big = num
    return big

def show_map(my_map):
    for i in range(len(my_map)):
        for j in range(len(my_map[0])):
            print(my_map[i][j], end="")
        print("")


def find_line(x1, y1, x2, y2):
    # empty list for x,y coords
    my_line = []
    # special case: single pt
    if x1 == x2 and y1 == y2:
        my_line.append(x1)
        my_line.append(y1)
        return my_line
    # determine vert or horiz
    if x1 == x2:
        if(y1 > y2):
            y1,y2 = y2,y1
        for i in range(y1, y2+1):
            my_line.append([x1, i])
        return my_line
    if y1 == y2:
        if(x1 > x2):
            x1,x2 = x2,x1
        for i in range(x1, x2+1):
            my_line.append([i, y1])
        return my_line
    # end case is diagonal line
    # we check the slope of the line,
    # we always work left to right
    if x1 > x2:
         x1, x2, y1, y2 = x2, x1, y2, y1
    # are we ascending or descending?
    if y1 < y2:
        for i in range((x2 - x1) + 1):
            my_line.append([x1 + i, y1 + i])
        return my_line
    else:
        for i in range((x2 - x1) + 1):
            my_line.append([x1 + i, y1 - i])
        return my_line

def draw_line(my_map, my_line):
    for pairs in my_line:
        try:
            my_map[pairs[1]][pairs[0]] += 1
        except TypeError:
            my_map[pairs[1]][pairs[0]] = 1



# strip the non int character from list
clean_data = []
for i in raw_data:
    i = i.split("\n")   # take newline off
    split_pairs = i[0].split("->")  # split coordinates across arrow
    from_coord, to_coord = split_pairs[0].split(","), split_pairs[1].split(",") # split into ints
    clean_data.append(int(from_coord[0]))
    clean_data.append(int(from_coord[1]))
    clean_data.append(int(to_coord[0]))
    clean_data.append(int(to_coord[1]))

print(clean_data)

# define the range of the data
biggest = find_largest(clean_data)

# create basic map of data
# 2D array filled with . to be empty
floor_map = []
for i in range(biggest+1):
    temp = []
    for j in range(biggest+1):
        temp.append(".")
    floor_map.append(temp)

for i in range(0, len(clean_data), 4):
    temp_line = find_line(clean_data[i], clean_data[i+1], clean_data[i+2], clean_data[i+3])
    if temp_line is not None:
        draw_line(floor_map, temp_line)
        # show_map(floor_map)

show_map(floor_map)

counter = 0
for i in range(len(floor_map)):
    for j in range(len(floor_map)):
        try:
            if int(floor_map[i][j]) > 1:
                counter += 1
        except ValueError:
            continue

print("\n\nCount:", counter)
