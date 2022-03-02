
# file i/o
def read_data(my_file='test.dat'):
    """
    read_data() opens a file and returns an array of strings for each line in the file
    :param my_file: string, file name to read, default value is given in params
    :return: [str1, str2, str3.... strx]
    """
    with open(my_file, 'r') as inf:
        raw_data = [line.strip() for line in inf.readlines()]
    return raw_data


def solve(my_homework):
    """
    solve() loops line by line through numbers to eval
    :param my_homework:  [str1, str2, str3... strx]
        list of strings that have the snail fish numbers nested
    :return:
        None
    """
    # start by looping through the homework
    # we are only ever working on the first line (index 0)
    while my_homework:
        # for the line we are looking at start by reducing across left to right
        my_homework[0] = reduced(my_homework[0])
        # once a line is reduced, check to see if there is another line below
        # if there is a line below append it to the first line and then remove it
        if len(my_homework) > 1:
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
    print(my_homework)


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
    string_list = [i for i in list(my_string)]

    # start a while true loop so we can start back at index 0 while reducing
    # we do this so we can reduce more than one item in our string
    while True:
        # flag for exit while loop
        reduced_flag = False
        # variable to track how deep in sub-numbers we are, this is for checking
        # if we need to explode a number that is four levels deep
        level = 0
        # start looking character by character in the list
        for char in string_list:
            if char is '[':
                level += 1
            elif char is ']':
                level -= 1

            # if we are at 5 opening brackets we are in level 4, and need to explode
            if level == 5:

                explode(string_list)
                # set the reduced flag to repeat while(True) loop from the top
                reduced_flag = True
                # break the for char loop and repeat from the top
                break


        # if we've moved across the string and haven't reduced at all,
        # we are done with the larger loop, break while(True)
        if not reduced_flag:
            break

    # copy the adjusted string_list to a single string variable for return
    for i in string_list:
        reduced_string += i

    return reduced_string

if __name__ == '__main__':

    homework = read_data()

    solve(homework)

    print('\r\r\rexiting...')