
# file i/o
def read_data(my_file='test.dat'):
    """
    read_data() opens a file and returns an array of strings for each line in the file
    :param my_file: string, file name to read, default value is given in params
    :return: [str1, str2, str3.... str x]
    """
    with open(my_file, 'r') as inf:
        raw_data = [line.strip() for line in inf.readlines()]
    return raw_data


def solve(my_homework):
    """
    solve() loops line by line through numbers to eval
    :param my_homework:  [str1, str2, str3... str x]
        list of strings that have the snail fish numbers nested
    :return:
        None
    """
    # start by looping through the homework
    # we are only ever working on the first line (index 0)
    while my_homework:
        # for the line we are looking at start by reducing across left to right
        print(f'Evaluating {my_homework[0]}...')
        my_homework[0] = reduced(my_homework[0])
        # once a line is reduced, check to see if there is another line below
        # if there is a line below append it to the first line and then remove it
        if len(my_homework) > 1:
            print(f'\x1b[0:30:44mFound new line, adding {my_homework[0]} + {my_homework[1]}\x1b[0m')
            temp_string = ''
            temp_string += '['
            temp_string += my_homework[0]
            temp_string += ','
            temp_string += my_homework[1]
            temp_string += ']'
            # we assembled the connected string, now send it to index 0
            my_homework[0] = '' + temp_string
            # delete the index we just concatenated
            del my_homework[1]
        # if there were no more lines, exit the loop
        else:
            break
    # show the final reduced form
    print(my_homework[0])

    # call the function to check magnitude of final number
    # we are passing the untangled string as a list of items
    # so we can perform operations easier in recursion
    find_magnitude(untangle(my_homework[0]))


def find_magnitude(my_string, current_index=0):
    my_final_sum = 0
    # look at our current index,
    # check if there is a sub-bracket in left item
    # if there is, call ourselves with the sub
    # if not, times by 3
    # check if there is sub-bracket in right item
    # if there is, call ourselves with the sub
    # if not, times by 2
    # add the two items from multiplications
    # return the result of the addition

    return my_final_sum

def untangle(my_string):
    """
    untangle() takes a string and returns a list of char and int
    :param my_string: 'str'
        the string, consists of [,] and 0-9 char
    :return:
        a list of individual items, either char (if [,]) or int (if a numeral)
    """
    untangled_string_list = []
    while my_string:
        temp_string = my_string[0]
        my_string = my_string[1:]
        if '0' <= temp_string <= '9':
            while '0' <= my_string[0] <= '9':
                temp_string += my_string[0]
                my_string = my_string[1:]
            temp_string = int(temp_string)

        untangled_string_list.append(temp_string)

    return untangled_string_list


def reduced(my_string):
    """
    reduced() scans through one line of snail fish numbers to check if it
    needs to be reduced. this function will return True if it
    :param my_string: 'str'
        a string of nested snail fish numbers
    :return:
        the reduced string, this may be unchanged
    """
    reduced_string = ''

    # split the string to individual characters so we can read left ot right easier
    string_list = untangle(my_string)

    # start a while true loop so we can start back at index 0 while reducing
    # we do this so we can reduce more than one item in our string
    while True:
        print('Trying to reduce:')
        error_check = 0
        error_list = []
        deepest_level = 0
        for item in string_list:
            if item is '[':
                error_check += 1
                error_list.append(error_check)
            elif item is ']':
                error_list.append(error_check)
                error_check -= 1
            else:
                error_list.append(' ')
            if error_check > deepest_level:
                deepest_level = error_check
            print(item, end='')
        print()
        for item in error_list:
            print(item, end='')
        print()
        # flag for exit while loop
        reduced_flag = False
        # variable to track how deep in sub-numbers we are, this is for checking
        # if we need to explode a number that is four levels deep
        level = 0
        # start looking character by character in the list
        for i in range(len(string_list)):
            if string_list[i] is '[':
                level += 1
            elif string_list[i] is ']':
                level -= 1

            # if we are at 5 opening brackets we are in level 4, and need to explode
            if level == deepest_level and level > 4:
                # print(f'Found item to explode...')
                string_list = explode(string_list, i)
                # set the reduced flag to repeat while(True) loop from the top
                reduced_flag = True
                # break the for char loop and repeat from the top
                break

            if type(string_list[i]) is int and string_list[i] >= 10 and deepest_level < 5:
                # print('Found item to split')
                string_list = go_split(string_list, i)
                reduced_flag = True
                break

        # if we've moved across the string and haven't reduced at all,
        # we are done with the larger loop, break while(True)
        if not reduced_flag:
            break

    # copy the adjusted string_list to a single string variable for return
    for i in string_list:
        try:
            reduced_string += i
        except TypeError:
            reduced_string += str(i)

    print(f'\x1b[0;30;41mFinal reduction is {reduced_string}\x1b[0m')

    return reduced_string


def go_split(string_list, index):
    """
    go_split() performs the split reduction on the numbers
    :param string_list: [char, char/int, char/int... ]
        the list of chars that make up our number
    :param index: int
        the index of the char in the list to split
    :return:
        list of strings after reduction
    """
    # print(string_list[index], '->', end='')
    # split the int value to two ints, rounding down on the first item
    left_value = int(string_list[index] / 2)
    right_value = string_list[index] - left_value

    # break the list into two so we can insert new items
    left_list = string_list[:index]
    right_list = string_list[index + 1:]
    insert_list = ['[', left_value, ',', right_value, ']']
    # print(insert_list)

    string_list = left_list
    for i in insert_list:
        string_list.append(i)
    for i in right_list:
        string_list.append(i)

    return string_list


def explode(string_list, index):
    """
    explode() performs the explode reduction on the numbers
    :param string_list: [char, char/int, char/int... ]
        the list of chars that make up our number
    :param index: int
        the index of the char in the list to begin explode operation
    :return:
        list of strings after reduction
    """
    # print(f'Exploding at index {index}...')
    while string_list[index+1] is '[':
        # print('Oops, found sub-item, moving to split that one!')
        index += 1
    # print(f'I think I am looking at {string_list[index:index+5]}')
    end_pair_index = index + 4
    # get the initial values in our pair for later addition
    left_int = string_list[index+1]
    right_int = string_list[index+3]

    # find the index of the left and right numeral, if they exist
    explode_left, explode_right = None, None
    # start at left bracket, look left (-1 index) for the neighbor int
    i = index
    while i > 0:
        i -= 1
        if type(string_list[i]) is int:
            explode_left = i
            break
    # start at right bracket, look right (+1 index) for the neighbor int
    i = end_pair_index
    while i < len(string_list)-1:
        i += 1
        if type(string_list[i]) is int:
            explode_right = i
            break

    # we have left and right indexes now. If there was no int left or right, that value is (None)
    if explode_left is not None:
        string_list[explode_left] = string_list[explode_left] + left_int
    if explode_right is not None:
        string_list[explode_right] = string_list[explode_right] + right_int

    # replace the entire bracketed substring with a 0
    string_list[index] = 0
    del string_list[index + 1: end_pair_index + 1]

    return string_list


if __name__ == '__main__':

    homework = read_data()

    solve(homework)

    print('\r\r\rexiting...')
