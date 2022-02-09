import copy

# file handling
with open("day_09.dat") as inf:
    data = [line for line in inf.read().split("\n")]

# change strings to int for easier use
int_data = []
for i in range(len(data)):
    int_data.append([])
    for j in range(len(data[i])):
        int_data[i].append(int(data[i][j]))

data = int_data
del(int_data, i, j)
print(data)



# print a 2d array of the data
def print_map(my_data):
    for i in range(len(my_data)):
        for j in range(len(my_data[i])):
            print(my_data[i][j], end="")
        print()


# part one: find the score of lowest points
def part_one():
    lowest_points = []
    lower_score = 0
    for i in range(len(data)):
        temp_array = []
        # print("********** ROW", i)
        for j in range(len(data[i])):
            print("\033[92m", data[i][j], "\033[0m", sep="", end="")
            # print("\n(", i, ",", j, ")", data[i][j], end="--")
            if int(data[i][j]) == 9: continue
            if i - 1 >= 0:
                # print("u", data[i-1][j], end=" ")
                if int(data[i][j]) > int(data[i-1][j]):
                    continue
            if j + 1 < len(data[i]):
                # print("r", data[i][j+1], end=" ")
                if int(data[i][j]) > int(data[i][j+1]):
                    continue
            if i + 1 < len(data):
                # print("d", data[i+1][j], end=" ")
                if int(data[i][j]) > int(data[i+1][j]):
                    continue
            if j -1 >= 0:
                # print("l", data[i][j-1], end=" ")
                if int(data[i][j]) > int(data[i][j-1]):
                    continue

            print("\b\033[1m", data[i][j], "\033[0m", sep="", end="")
            temp_array.append(data[i][j])
            lowest_points.append([i, j])
            lower_score += int(data[i][j]) + 1
            # print("Lowest pt at", i, j, "score", lower_score, end="")
        print(" found:", *temp_array, " total:", lower_score, sep="")
    return lowest_points


# part 2, find the size of basins and locate biggest 3
def find_basin_size(my_data, starting_point):
    my_basin_size = 0
    my_x = int(starting_point[0])
    my_y = int(starting_point[1])
    # print("Looking at (" + str(my_x) + "," + str(my_y) + "), basin size at " + str(my_basin_size))

    if my_x - 1 >= 0 and my_data[my_x-1][my_y] > my_data[my_x][my_y]:
        if my_data[my_x-1][my_y] != 9:
            # print("Found", my_data[my_x-1][my_y], "at", my_x - 1, my_y)
            my_basin_size += find_basin_size(my_data, [my_x - 1, my_y])
    if my_y - 1 >= 0 and my_data[my_x][my_y-1] > my_data[my_x][my_y]:
        if my_data[my_x][my_y-1] != 9:
            # print("Found", my_data[my_x][my_y-1], "at", my_x, my_y - 1)
            my_basin_size += find_basin_size(my_data, [my_x, my_y - 1])
    if my_x + 1 < len(my_data) and my_data[my_x + 1][my_y] > my_data[my_x][my_y]:
        if my_data[my_x+1][my_y] != 9:
            # print("Found", my_data[my_x + 1][my_y], "at", my_x + 1, my_y)
            my_basin_size += find_basin_size(my_data, [my_x + 1, my_y])
    if my_y + 1 < len(my_data[0]) and my_data[my_x][my_y+1] > my_data[my_x][my_y]:
        if my_data[my_x][my_y+1] != 9:
            # print("Found", my_data[my_x][my_y+1], "at", my_x, my_y + 1)
            my_basin_size += find_basin_size(my_data, [my_x, my_y + 1])

    # print("Cleaning up at", my_x, my_y, "count is", my_basin_size)
    my_data[my_x][my_y] = 9
    # print_map(my_data)
    return(my_basin_size + 1)

def part_two(my_lowest_points):
    lowest_sizes = []
    my_data = copy.deepcopy(data)
    for pairs in my_lowest_points:
        lowest_sizes.append(find_basin_size(my_data, pairs))
    lowest_sizes.sort(reverse=True)
    return(lowest_sizes)

# calls for part 1
lowest_points = part_one()
print(sum([int(data[r[0]][r[1]]) + 1 for r in lowest_points]))

# calls for part 2
lowest_basins = part_two(lowest_points)
print(lowest_basins)
print("Final Product:", lowest_basins[0] * lowest_basins[1] * lowest_basins[2])