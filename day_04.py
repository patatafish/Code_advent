def check_bingo(my_boards):
    """
    Checks our boards list for any winning row or column

    :param my_boards: list of strings
    :return: None if no winning board found
            index of winning board if found
    """
    global board_size   # import global board size

    # create string to match for winner
    win_string = ""
    for i in range(board_size):
        win_string += "*"

    # loop across starting index of each board
    for current_board in range(0, (len(my_boards)), (board_size ** 2)):

        # check rows
        for i in range(0, (board_size ** 2), board_size):
            # temp string to hold concatted row
            temp_string = ""
            for j in range(board_size):
                # our final target is j, added to i for what
                # row we are in, then added to current_board
                # for what board index we are in
                j = j + i + current_board
                # push current item to a temp string
                temp_string += my_boards[j]
            if temp_string == win_string:  # if the temp string is ALL * we have a winner
                return current_board    # return the index of the winning board

        # check cols, same loops as above but checks
        # down columns instead of acress rows
        for i in range(board_size):
            # temp string
            temp_string = ""
            for j in range(0, board_size ** 2, board_size):
                j = j + i + current_board
                temp_string += my_boards[j]
            if temp_string == win_string:
                return current_board

    # if no match found, return None
    return None


def print_boards(my_boards):
    """
    print_boards will output a formatted version of the boards passed

    :param my_boards: list of strings
    :return: none
    """

    global board_size   # import global board size

    # define variables for formatting of print
    total_length = len(my_boards)

    # generate range of starting values
    # this is a list of the top-left position
    # of each discreet board
    start_points = range(0, total_length, (board_size ** 2))

    # loop through each row, down the board
    for row in range(board_size):
        # loop each start point in our list
        for i in start_points:
            # we should shift (board_size) over each row
            # down we move
            i += (board_size * row)
            # loop through the individual items in each row
            # and output formatted items, 3 wide and right align
            for j in range(board_size):
                print("{:>3}".format(my_boards[j+i]), end="")
            print("   ", end="")    # pad each board with 3 spaces in between
        print("")   # end the row, print endl


# PART 1
#
#
# GLOBAL VARIABLES
# define size of board
board_size = 5
# create blank winner
winning_board = []

print("Part 1 output:")

# read raw data from file
raw_data = open("day_04.dat", "r").readlines()
# print(type(raw_data), raw_data)

# separate calls from boards
raw_calls = raw_data.pop(0)
# print(type(raw_calls), raw_calls)

# split string into int values for calls
clean_calls = [int(x) for x in raw_calls.split(',')]
# print(clean_calls)

# create list of boards
clean_boards = []

# loop through data to create boards
for line in raw_data:
    if line != '\n':    # strip empty lines
        for item in line.split():   # split string into int values for boards
            clean_boards.append(item)

print_boards(clean_boards)

# we will mark our bingo boards by changing the string to '*'
for call in clean_calls:
    last_call = call
    print("Called", last_call)
    for index in range(len(clean_boards)):
        try:
            if int(clean_boards[index]) == call:
                clean_boards[index] = "*"
        except ValueError:
            continue
    print_boards(clean_boards)
    # call check to see if winner
    winner = check_bingo(clean_boards)
    # if winner is found, break loop for calling
    if winner is not None:
        print("\n\nFound winning board at index", winner)
        for i in range(board_size ** 2):
            print("{:>3}".format(clean_boards[i+winner]), end="")
            winning_board.append(clean_boards[i + winner])
            if (i + 1) % board_size == 0:
                print("")
        break

# calculate sum of uncalled spaces
sum_of_winner = 0
for i in range(len(winning_board)):
    try:
        sum_of_winner += int(winning_board[i])
    except ValueError:
        continue
print("\nSumming...", sum_of_winner)
# output final product
print(sum_of_winner, "*", last_call, "=", sum_of_winner * last_call)


# PART TWO
#
#
print("\n\nPart 2 Output:")

# create list of boards
clean_boards = []
winning_board = []

# loop through data to create boards
for line in raw_data:
    if line != '\n':    # strip empty lines
        for item in line.split():   # split string into int values for boards
            clean_boards.append(item)

print_boards(clean_boards)

# we will mark our bingo boards by changing the string to '*'
for call in clean_calls:
    last_call = call
    print("Called", last_call)
    for index in range(len(clean_boards)):
        try:
            if int(clean_boards[index]) == call:
                clean_boards[index] = "*"
        except ValueError:
            continue
    print_boards(clean_boards)

    # this time we loop the winning check to see if there are multiple winner boards
    # this flag will mark when a completed cycle happens with no winner found.
    flag = False
    last_win = False
    while flag == False:
        # call to check for winner
        winner = check_bingo(clean_boards)
        # If this wins AND it is the last board, set exit flag
        if (winner is not None) and (len(clean_boards) == (board_size ** 2)):
            flag = True
            last_win = True
            continue
        # otherwise if we found winner among other boards
        if winner is not None:
            print("Found winning board at index", winner)
            del(clean_boards[winner:(winner+25)])
            print(int(len(clean_boards) / (board_size ** 2)), "boards remain.")
            continue    # if we found a winner head back to while loop top

        # if no winners found after re-check, set flag true to exit while
        print("No further winners, resuming call...")
        flag = True


    if last_win == True:
        print("Last winning board:")
        print_boards(clean_boards)
        # calculate sum of uncalled spaces
        sum_of_winner = 0
        for i in range(len(clean_boards)):
            try:
                sum_of_winner += int(clean_boards[i])
            except ValueError:
                continue
        print("\nSumming...", sum_of_winner)
        # output final product
        print(sum_of_winner, "*", last_call, "=", sum_of_winner * last_call)
        break
