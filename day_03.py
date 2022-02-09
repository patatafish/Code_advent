# establish list for data
raw_data = []

# read file
for line in open("day_03.dat", "r").readlines():  # read each line
    temp = line.split('\n')  # split the newline from the string
    raw_data.append(list(temp[0]))  # put data, temp[0], as list inside raw_data[]

# find length of array
# this assumes all entries are the same length
length = len(raw_data[0])

# find height of array
height = len(raw_data)

# establish list for tally of dominance 1/0
totals = []

# loop across all entries in length of array
for x in range(length):
    # create a new place value for the total counter
    totals.append(0)
    # loop down all entries in height of array
    for y in range(height):
        # we now have x/y coord for array
        # list indexed as y,x to traverse
        # down (y value) before moving to
        # next column (x value)

        # if data is 1, totals[x]++
        # where x is index of what
        # column we are in
        if int(raw_data[y][x]) == 1:
            totals[x] += 1
        # else totals[x]--
        else:
            totals[x] -= 1

print("Final counts:", totals)

# interpret totals list as 0 or 1
# if the number is positive, there has been more 1's in the column
# if the number is negative, there has been more 0's in the column
# if the number is 0 it was a tie (hopefully not possible in our data)
for i in range(len(totals)):
    if int(totals[i]) > 0:
        totals[i] = 1
    elif int(totals[i]) < 0:
        totals[i] = 0
    else:
        raise "Oh snap, it's a tie! This shouldn't happen!"


print("Final Binary:", totals)

# put list into str then base 10
lam_string = ""  # create empty string
for item in totals:  # loop totals[] and
    lam_string += str(item)  # append value in single string
print("Lambda Value:", lam_string)
print("Lambda Base 10:", int(lam_string, 2))

# create gamma binary
gam_string = ""  # create empty string
for i in lam_string:  # loop through lam_string
    if i == "1":  # append opposite value to gamma
        gam_string += "0"
    else:
        gam_string += "1"

print("Gamma Value:", gam_string)
print("Gamma Base 10:", int(gam_string, 2))

print("Final product:", end=" ")
print(int(gam_string, 2) * int(lam_string, 2))


# part 2 start
# #
# #
print("\n\nBegin Part 2 Output")

# find the o2/co2 rating: most/least common bit in list
# we will loop the list through a recursive function
# first make a copy of the raw data to manip:
o2_data = raw_data
co2_data = raw_data


# define the function
def o2_rating(o2_input, my_focus=0):
    """
    recursive function exit criteria:
        when the number of entries is reduced to 1
        we reach an index beyond length of entries (EXCEPTION SHOULDN'T HAPPEN)

    :param o2_input: list of lists, numbers in binary format
    :param my_focus: index of focal bit for search
    :return: returns a single list when recursion completes
    """

    # define local variables
    my_total = 0  # integer used to locate most common digit

    # loop down o2_data[focus]
    for o2_line in o2_input:
        # count the most common digit
        if int(o2_line[my_focus]) == 0:
            my_total -= 1
        else:
            my_total += 1

    # reuse MCD as binary value
    # in O2 value ties become binary 1
    if my_total >= 0:
        my_total = 1
    else:
        my_total = 0

    # built temp list to put valid data in
    o2_temp_list = []
    # eliminate items without MCD
    for o2_line in o2_input:  # loop through all items
        if int(o2_line[my_focus]) == my_total:  # if it matches
            o2_temp_list.append(o2_line)  # then push it to temp list

    # check if only 1 left
    if len(o2_temp_list) == 1:
        return o2_temp_list[0]  # if there is only 1 item, return that item

    # increment focus
    my_focus += 1

    # return(call self)
    return o2_rating(o2_temp_list, my_focus)


# define the function
def co2_rating(co2_input, my_focus=0):
    """
    recursive function exit criteria:
        when the number of entries is reduced to 1
        we reach an index beyond length of entries (EXCEPTION SHOULDN'T HAPPEN)

    :param co2_input: list of lists, numbers in binary format
    :param my_focus: index of focal bit for search
    :return: returns a single list when recursion completes
    """

    # define local variables
    my_total = 0  # integer used to locate most common digit

    # loop down o2_data[focus]
    for co2_line in co2_input:
        # count the most common digit
        if int(co2_line[my_focus]) == 0:
            my_total -= 1
        else:
            my_total += 1

    # reuse MCD as binary value
    # in CO2 value ties become binary 0
    if my_total >= 0:
        my_total = 1
    else:
        my_total = 0

    # built temp list to put valid data in
    co2_temp_list = []
    # eliminate items without MCD
    for co2_line in co2_input:  # loop through all items
        if int(co2_line[my_focus]) != my_total:  # if it doesn't match
            co2_temp_list.append(co2_line)  # then push it to temp list

    # check if only 1 left
    if len(co2_temp_list) == 1:
        return co2_temp_list[0]  # if there is only 1 item, return that item

    # increment focus
    my_focus += 1

    # return(call self)
    return co2_rating(co2_temp_list, my_focus=my_focus)


# call to function
final_o2 = o2_rating(o2_data)
final_co2 = co2_rating(co2_data)
# change list to string
final_o2_string = ""
final_co2_string = ""
for item in range(len(final_o2)):
    final_o2_string += str(final_o2[item])
for item in range(len(final_co2)):
    final_co2_string += str(final_co2[item])


print("O2 Rating:", final_o2_string)
print("02 Base 10:", int(final_o2_string, 2))
print("CO2 Rating:", final_co2_string)
print("CO2 Base 10:", int(final_co2_string, 2))

print("Final product:", int(final_o2_string, 2) * int(final_co2_string, 2))
