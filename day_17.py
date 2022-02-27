
def get_target(my_file='day_17.dat'):
    """
    get_target() opens the dat file and returns two (x1, x2) coordinate pairs
    as tuples in a list format.

    default file name to open is established in params, can be passed if different
    file name is wanted

    :return:
    return is interpreted as [(min x, max x), (min y, max y)]
    """
    # file I/O
    with open(my_file, 'r') as inf:
        target_string = inf.read().strip()
    # target string is led with 'target area: ' we strip that
    target_string = target_string[13:]
    # split the string around the comma between x and y values
    x_target, y_target = target_string.split(',')
    # take the numerical values out of the string for x and y
    # the y value has a leading space from the above split
    # so we strip 3 characters
    x_target = x_target[2:]
    y_target = y_target[3:]
    # separate the int values
    x1, x2 = x_target.split('..')
    y1, y2 = y_target.split('..')
    # convert string values to integers
    x1, y1, x2, y2 = [int(i) for i in [x1, y1, x2, y2]]
    # re-use variable names here
    # create the tuples of coordinates to return
    x_target = (x1, x2)
    # reverse order of y tuple because of negative values and the "maximum"
    # value being bigger in integer space
    y_target = (y2, y1)

    # returns list of tuples
    return [x_target, y_target]

def aim(my_target):
    """
    aim() loops across the firing space to find the optimal firing angle
    optimal in this case is defined as highest arc we can create while
    still passing into target area

    this function calls show_shot() to display the firing patterns

    :param my_target: [(min x, max x), (min y, max y)]
            a list of tuples that contains the min/max values defining our target rectangle
    :return:
    None
    """

    # display the empty field
    show_shot(my_target)

    # define aim, trajectory, and best aim lists
    my_aim = [0,my_target[1][1]]
    best_aim = [0, -1, 0]
    hit_list = []

    # loop to test aim values, will loop until break
    while True:
        # use my_aim as a top-level item that records where
        # we started from. use this_shot as a variable that
        # tracks our shot as we find trajectory in each try
        this_shot = [0, 0]
        inertia = [my_aim[0], my_aim[1]]
        trajectory = []
        hit = False
        # build trajectory list for current aim
        while True:
            # record current point
            # append new list, not a copy of aim[] to avoid changing recorded values
            trajectory.append([this_shot[0], this_shot[1]])
            # check if we are past the target, if so exit trajectory loop
            # we know our target will be in positive x space, and negative y space
            if this_shot[0] > my_target[0][1] or this_shot[1] < my_target[1][1]:
                break
            # we already know we aren't past the target, so check if we are in it
            if (my_target[0][0] <= this_shot[0] <= my_target[0][1] and
                my_target[1][0] >= this_shot[1] >= my_target[1][1]):
                hit = True
                break
            # adjust values
            # as dedined by: x approaches 0 by 1 each loop (inertia slows horizontal move)
            #               y fall rate increases by 1 each loop (gravity increases fall rate)
            this_shot[0] += inertia[0]
            this_shot[1] += inertia[1]
            # adjust horizontal inertail value
            if inertia[0] < 0:
                inertia[0] += 1
            elif inertia[0] > 0:
                inertia[0] -= 1
            # adjust vertical inertial value
            inertia[1] -= 1



        # display the result of the last shot try
        # if hit:
            # print("\x1b[0:31:40m")
        # print(f'Firing at ({my_aim[0]}, {my_aim[1]})')
        # show_shot(my_target, trajectory)
        # if hit:
            # print('\x1b[0m')

        # this aim adjustment creates a cycle of overshoot/undershoot
        # we check to see if the "found" max is the same as what we have
        # which would mean we checked the whole space. Return the found
        # max
        if my_aim[1] > abs(my_target[1][1]):
            break

        # we have left the firing loop, check to see why
        if hit:

            # display the result of the last shot try
            # print(f'Firing at ({my_aim[0]}, {my_aim[1]})')
            # show_shot(my_target, trajectory)

            # record the initial velocities of valid firing coordinates:
            hit_list.append([my_aim[0], my_aim[1]])

            # we hit the target, check the values to see if we've maxed out
            for pairs in trajectory:
                if pairs[1] > best_aim[0]:
                    best_aim[0] = pairs[1]
                    best_aim[1] = my_aim[0]
                    best_aim[2] = my_aim[1]
            # adjust aim back and left
            # my_aim[1] += 1
            my_aim[0] += 1
        elif this_shot[0] > my_target[0][1]:
            # we overshot in the x direction, adjust our my_aim variable
            # by raising the y direction and start our x over at 1
            if my_aim[1] >= 0:
                my_aim[1] += 1
                my_aim[0] = 1
            else:
                my_aim[0] += 1
                if my_aim[0] > my_target[0][1]:
                    my_aim[1] += 1
                    my_aim[0] = 1
        elif this_shot[1] < my_target[1][1]:
            # we didn't reach the target in x direction before we dropped below it
            # adjust our my_aim variable by raising the x direction
            my_aim[0] += 1


    # we have broken the whileTrue loop that scans the firing space,
    # we are now able to print the best shot.
    print(f'Best trick shot has a height of {best_aim[0]}, aimed at ({best_aim[1]}, {best_aim[2]})')
    print(f'There are {len(hit_list)} valid options for firing:')
    for i in range(len(hit_list)):
        print(hit_list[i], end=', ')
        i += 1
        if (i % 10) == 0:
            print()
    print()

def show_shot(my_target, my_shot=[[0,0]]):
    """
    show_shot() builds a string to display an origin and target, if a trajectory
    list is passed in my_shot then we will also display the arc of the shot, if not
    then we show the empty field with target
    :param my_target: [(min x, max x), (min y, max y)]
            a list of tuples that contains the min/max values defining our target rectangle
    :param my_shot: [[a, a1], [b, b1], [c, c1], ... [z, z1]]
            a list of list pairs showing the coordinates of the firing arc
    :return:
        None
    """
    # define the bottom right values to draw boundaries
    max_x = my_target[0][1] + 1
    # y value will always be a negative
    min_y = my_target[1][1] - 1
    # if we have a shot trajectory, find the max/min y in the shot list
    max_y = 1
    for item in my_shot:
        max_y = max(item[1], max_y)
        min_y = min(item[1], min_y)\
    # adjust the min and max y by one for border during print
    max_y += 1
    min_y -= 1


    # loop through full range of items, printing appropriate character
    for i in reversed(range(min_y, max_y+1)):
        temp_string = ''
        for j in range(-1, max_x+1):
            if [j, i] in my_shot:
                temp_string += 'O'
            elif (my_target[0][0] <= j <= my_target[0][1] and
                my_target[1][0] >= i >= my_target[1][1]):
                temp_string += ','
            else:
                temp_string += '.'
        temp_string += f' {i}'

        if 'O' in temp_string:
            print(temp_string)

    print()

if __name__ == '__main__':




    # get the min/max of our target area from input file
    target = get_target()

    # call the loop to test shots
    aim(target)

    print('exiting...')
