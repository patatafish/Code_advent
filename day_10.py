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
openers = ['(', '{', '[', '<']
closers = [')', '}', ']', '>']

def part_one():
    # create a list to place incomplete lines for part 2
    incomplete_list = []
    total = 0

    for lines in raw_data:

        # flag to mark end of cleaning
        dirty = True
        corrupted = False

        itemized_string = [*lines]
        # print(itemized_string)

        while dirty:
            # print(*itemized_string)
            changed = False
            for index in range(len(itemized_string) - 1):
                if itemized_string[index] in openers and itemized_string[index + 1] in closers:
                    if my_dict[itemized_string[index]] + my_dict[itemized_string[index+1]] != 10:
                        # print ("Found Corrupt Set")
                        if itemized_string[index+1] == ')':
                            total += 3
                        elif itemized_string[index+1] == ']':
                            total += 57
                        elif itemized_string[index+1] == '}':
                            total += 1197
                        else:
                            total += 25137
                        corrupted = True
                        dirty = False
                        break
                    del itemized_string[index + 1]
                    del itemized_string[index]
                    changed = True
                    break
            if not changed and not corrupted:
                if len(itemized_string):
                    incomplete_list.append(itemized_string)
                dirty = False

        # print(color.YELLOW, color.BOLD, "Total:", total, color.END)

    print("final", total)
    return(incomplete_list)


def part_two(my_incomplete_list):
    totals_list = []

    for lines in my_incomplete_list:
        # print(*lines)
        lines.reverse()
        total = 0
        for chars in lines:
            if chars == '<':
                total = (total * 5) + 4
            elif chars == '{':
                total = (total * 5) + 3
            elif chars == '[':
                total = (total * 5) + 2
            else:
                total = (total * 5) + 1
            # print("CT:", total)
        totals_list.append(total)

    totals_list.sort()
    print(totals_list)
    print(totals_list[int(len(totals_list)/2)])

# define incomplete list, give to part one to return
incomplete_list = part_one()
print("Incomplete lines:", incomplete_list)
part_two(incomplete_list)