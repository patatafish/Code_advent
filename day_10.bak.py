# file i/o
with open("day_10.dat") as inf:
    raw_data = [line for line in inf.read().split("\n")]

# formatting visuals
class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


# define translation dictionary
my_dict = {'{': 1, '}': 9, '[': 2, ']': 8, '(': 3, ')': 7, '<': 4, '>': 6}


def part_one():
    check_score = 0
    corrupted_list = []
    incomplete_list = []
    for my_line in raw_data:
        item_list = [*my_line]
        print(len(item_list), *item_list)

        openers = ['(', '{', '[', '<']
        closers = [')', '}', ']', '>']

        group_list = []
        for open_index in range(len(item_list)):
            if item_list[open_index] in openers:
                for close_index in range(open_index + 1, len(item_list)):
                    if item_list[close_index] in closers:
                        group_list.append(item_list[open_index:close_index+1])

        valid_list = []
        for lists in group_list:
            # abandon items that lead with valid open/close
            if my_dict[lists[0]] + my_dict[lists[1]] == 10:
                continue
            ocount = 0
            ccount = 0
            for items in lists:
                if items in openers: ocount += 1
                elif items in closers: ccount += 1
            if ocount == ccount:
                valid_list.append(lists)

        flag = True
        for lists in valid_list:
            print(*lists, end=" ")
            paren = 0
            brak = 0
            curl = 0
            carr = 0
            for index in range(len(lists)):
                if lists[index] is '(': paren += 1
                elif lists[index] is ')': paren -= 1
                elif lists[index] is '[': brak += 1
                elif lists[index] is ']': brak -= 1
                elif lists[index] is '{': curl += 1
                elif lists[index] is '}': curl -= 1
                elif lists[index] is '<': carr += 1
                elif lists[index] is '>': carr -= 1
            print(paren, brak, curl, carr, end=" ")
            if paren != 0 or brak != 0 or curl != 0 or carr != 0:
                print("corrupted, expected", end=" ")
                if paren > 0: print("( ", end="")
                if brak > 0: print("[ ", end="")
                if curl > 0: print("{ ", end="")
                if carr > 0: print("< ", end="")
                print("found", end=" ")
                if paren < 0:
                    print(")")
                    check_score += 3
                if brak < 0:
                    print("]")
                    check_score += 57
                if curl < 0:
                    print("}")
                    check_score += 1197
                if carr < 0:
                    print(">")
                    check_score += 25137
                flag = False
                break
            print()

        if flag == False:
            corrupted_list.append(my_line)
        else:
            incomplete_list.append(my_line)

    print("Corrupted:")
    print(*corrupted_list, sep="\n")
    print()
    print("Incomplete:")
    print(*incomplete_list, sep="\n")
    print("\n", check_score)






part_one()




===================
# flag to break loops, is/is not corrupted bool
flag = False
print("Starting pair", my_line[clean_start:clean_end + 1])
# start to loop from initial pair, using while(True) to
# loop outwards until either found valid or corrupted
while (flag == False):
    # set a second inner loop
    while (flag == False):
        # CHECK FOR CORRUPTION HERE
        # this is sees if the open char matches the close char
        if my_dict[my_line[clean_start]] + my_dict[my_line[clean_end]] != 10:
            if my_dict[my_line[clean_end - 1]] + my_dict[my_line[clean_end]] == 10:
                print("Consecutive Sets", my_line[clean_start:clean_end + 1])
            else:
                print(color.YELLOW, color.BOLD, "Found corrupted set", color.END, my_line[clean_start:clean_end + 1])
                corrupted_list.append([my_line, [clean_start, clean_end]])
                flag = True
                continue
        # if the pairs do match, we have a valid set
        else:
            print("Valid set", my_line[clean_start:clean_end + 1])

        # CHECK FOR SPECIAL CASE: TWO
        if clean_end + 2 < len(my_line):
            # check to see if the right two is an open/close pair
            if my_line[clean_end + 1] in openers:
                if my_dict[my_line[clean_end + 1]] + my_dict[my_line[clean_end + 2]] == 10:
                    clean_end += 2
                    # if all items are true, we found valid pair,
                    # return to the top of while(true) loop and see if next
                    # pair is also valid
                    continue
        break
    # END OF INSIDE FOR TRUE LOOP
    if clean_start - 1 >= 0 and clean_end + 1 < len(my_line) and flag == False:
        if my_line[clean_start - 1] in openers and my_line[clean_end + 1] in closers:
            clean_start -= 1
            clean_end += 1
            print("Found containing pair", my_line[clean_start:clean_end + 1])
            continue
    break
if flag == True: break


================================================================

# cycle one line at a time
for my_line in raw_data:
    # print(*my_line)
    # create list to record open/close pairs when next to eachother
    # this will establish starting points to expand from when checking
    # for valid open/close pairs to find corrupted lines
    starting_pairs = []
    # create empty lists of start and end points for valid sets
    # this will be for checking for neighboring valid sets and to
    # marry valid sets to expand window for checking
    valid_start_index = []
    valid_end_index = []
    # loop through string and locate all neighboring open/close pairs
    # these will be the starting points, where we check from
    # inside to out for validity
    for i in range(len(my_line) - 1):
        # if two consecutive items are open then close
        if my_line[i] in openers and my_line[i + 1] in closers:
            # record index of pairs in list
            starting_pairs.append([i, i + 1])
    # show the found list
    # print(starting_pairs)
    # flag for loop exit is or is not corrupted
    corrupt = False
    # loop the list of neighboring pairs
    for pairs in starting_pairs:
        # check to see if we've returned from a corrupted line
        # if so we don't check any more pairs
        if corrupt:
            break

        # index of the current start and end pair
        # we start by initializing this to pair[0] and pair[1] but expand
        # inside the while loop
        index_start = pairs[0]
        index_end = pairs[1]

        # push initial starting index to checking list for marry
        # and validity check
        valid_start_index.append(index_start)
        valid_end_index.append(index_end)

        # start of loop to check initial pairs
        while not corrupt:

            # show what set we are looking at
            # print(":", my_line[index_start:index_end+1])

            if my_dict[my_line[index_start]] + my_dict[my_line[index_end]] != 10:
                # special case: we are single sets consecutively, do not check these items
                if my_dict[my_line[index_end - 1]] + my_dict[my_line[index_end]] != 10:
                    # print(color.YELLOW, "Found corrupted set!", color.BOLD, my_line[index_start:index_end+1], color.END)
                    # record the corrupted line, and the index of the corrupted item
                    corrupted_list.append([my_line, index_end])
                    # set flag and exit loop
                    corrupt = True
                    continue
            else:
                # if valid, record the index for possible set marrying
                # print("Valid Set")
                # avoid redundantly adding items to valid index set list
                if index_start != valid_start_index[-1] and index_end != valid_end_index[-1]:
                    valid_start_index.append(index_start)
                    valid_end_index.append(index_end)
                    # print("Added to valid:", valid_start_index[-1], valid_end_index[-1])

            # check to see that our index will not leave the string length when expanded
            if index_start - 1 < 0 or index_end + 1 >= len(my_line):
                # tried to look out of ends of string, break while loop and move on
                # print("Tried to check out of bounds")
                break

            # see if our valid set is neighboring a valid set to the left
            if index_start - 1 in valid_end_index:
                # print("Touching sets, attempting to marry")
                # found a valid set to the left, move starting point of
                # validlist to the start of that set, catting the two
                # valid lists together
                index_start = valid_start_index[valid_end_index.index(index_start - 1)]
                # print(my_line[index_start:index_end+1])

                # we don't want to break to top of loop because we have
                # consecutive sets like ()[]. We know they are both valid, so
                # instead we go ahead and check for a containing pair, and exit
                # loop with valid if no other containers

            # check to see if we have a surrounding set
            if my_line[index_start - 1] in openers and my_line[index_end + 1] in closers:
                # we found a pair surrounding our current pair, move ends and send
                # back to top of loop to check validity
                index_start -= 1
                index_end += 1
                # print("Found surrounding pair", my_line[index_start:index_end+1])
                continue

            # break while loop if we've reached the end of all checks
            break

    # if we found an incomplete line (not corrupted)
    # then log it in a list for part 2
    # this checks a line past the end of the list, so
    # we check for length>0 before appending
    if not corrupt and len(my_line):
        # print("Incomplete List")
        incomplete_list.append(my_line)

print("Corrupted lines:", *corrupted_list)

total = 0
for pairs in corrupted_list:
    my_string = pairs[0]
    my_index = pairs[1]
    my_close = my_string[my_index]
    # print(my_close)
    if my_close == ')':
        total += 3
    elif my_close == ']':
        total += 57
    elif my_close == '}':
        total += 1197
    else:
        total += 25137
    # print(total)
