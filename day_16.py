# file io
def read_file(filename='day_16.dat'):
    with open(filename, 'r') as inf:
        raw_data = [line for line in inf.read()]
    return raw_data


# global dictionary for hex to binary
to_bin = {'0': '0000',
          '1': '0001',
          '2': '0010',
          '3': '0011',
          '4': '0100',
          '5': '0101',
          '6': '0110',
          '7': '0111',
          '8': '1000',
          '9': '1001',
          'A': '1010',
          'B': '1011',
          'C': '1100',
          'D': '1101',
          'E': '1110',
          'F': '1111'}


def process_signal(my_hex):
    global to_bin
    my_bin = ''
    for bit in my_hex:
        my_bin += to_bin[bit]
    return my_bin


def bin_to_dec(my_bin):
    my_dec = 0
    base = 1

    while my_bin:
        my_dec += int(my_bin[-1]) * base
        my_bin = my_bin[:-1]
        base *= 2

    return my_dec


def run_signal(signal, target, clean_signal=None):
    if not clean_signal:
        clean_signal = [0, 0, f'signal is {len(signal)} bits']
    print('called run_', target, clean_signal)
    print(target[0], signal[target[0]:target[1]], target[1])
    my_end = target[0]
    while '1' in signal[my_end:target[1]]:

        my_end, my_ver, my_type = get_type(signal, target[0])
        my_type = bin_to_dec(my_type)
        my_ver = bin_to_dec(my_ver)
        if my_type == 4:
            new_literal = ''
            while True:
                my_len = signal[my_end]
                new_literal += signal[my_end+1:my_end+5]
                my_end += 5
                if my_len == '0':
                    break
            new_literal = bin_to_dec(new_literal)
            clean_signal.append([my_ver, my_type, int(new_literal)])
            if my_end < target[1]:
                clean_signal = run_signal(signal, [my_end, target[1]], clean_signal)
                return clean_signal
        else:
            my_len = signal[my_end]
            my_end += 1
            if my_len == '0':
                sub_len = bin_to_dec(signal[my_end:my_end+15])
                my_end += 15
                my_sub_count = scan_count(signal[my_end:my_end+sub_len])
                clean_signal.append([my_ver, my_type, sub_len, my_sub_count])
                clean_signal = run_signal(signal, [my_end, my_end+sub_len], clean_signal)
                my_end += sub_len
                if my_end < target[1]:
                    clean_signal = run_signal(signal, [my_end, target[1]], clean_signal)
                    return clean_signal
            elif my_len == '1':
                sub_len = bin_to_dec(signal[my_end:my_end+11])
                my_end += 11
                sub_bit_len = scan_len(signal, my_end, sub_len)
                # target_length = sub_bit_len - my_end
                clean_signal.append([my_ver, my_type, sub_bit_len, sub_len])

                clean_signal = run_signal(signal, [my_end, my_end+sub_bit_len], clean_signal)
                my_end += sub_bit_len
                if my_end < target[1]:
                    clean_signal = run_signal(signal, [my_end, target[1]], clean_signal)
                    return clean_signal

    return clean_signal


def scan_count(my_signal):
    member_count = 0
    print('counting members of ', my_signal)
    my_start = 0

    while my_signal:
        member_count += 1
        this_type = my_signal[3:6]
        my_start += 6
        if this_type == '100':
            while my_signal[my_start] is '1':
                my_start += 5
            my_start += 5

            my_signal = my_signal[my_start:]
            my_start = 0
        else:
            this_len = my_signal[my_start]
            my_start += 1
            if this_len is '0':
                member_number = my_signal[my_start:my_start+15]
                member_number = bin_to_dec(member_number)
                my_start += 15 + member_number
                # member_count += member_number
                my_signal = my_signal[my_start:]
                my_start = 0
                # my_signal = my_signal[18+scan_len(my_signal, 18, member_number):]
            else:
                my_sub_len = bin_to_dec(my_signal[my_start:my_start+11])
                my_start += 11
                my_start += scan_len(my_signal, my_start, my_sub_len)
                # member_count += scan_count(my_signal[22:22+my_sub_len])
                my_signal = my_signal[my_start:]
                my_start = 0

    return member_count


def scan_len(signal, my_start, my_number):
    counted_subs = 0
    my_sub_len = 0 + my_start
    while counted_subs < my_number:
        print(f'Counting subs: {counted_subs+1}/{my_number}', end=' ')
        counted_subs += 1
        my_type = signal[my_start+3:my_start+6]
        my_start += 6
        if my_type == '100':
            while True:
                index = signal[my_start]
                if index == '1':
                    my_start += 5
                    continue
                my_start += 5
                break
        else:
            index = signal[my_start]
            my_start += 1

            if index == '0':
                this_signal_len = signal[my_start:my_start+15]
                my_start += 15
                my_start += this_signal_len
            elif index == '1':
                print()
                this_signal_count = bin_to_dec(signal[my_start:my_start+11])
                my_start += 11
                target_len = scan_len(signal, my_start, this_signal_count)
                my_start += target_len
        print()

    return my_start - my_sub_len


def get_type(signal, my_ending_bit):
    my_version = signal[my_ending_bit:my_ending_bit+3]
    my_type = signal[my_ending_bit+3:my_ending_bit+6]
    return my_ending_bit + 6, my_version, my_type


def index_subs(my_clean_signal, parent_index, reset=0):
    global furthest_skip
    try:
        furthest_skip
    except NameError:
        furthest_skip = 0
    child_index_list = []

    if reset:
        furthest_skip = 0

    my_sub_count = my_clean_signal[parent_index][3]
    current_index = parent_index

    # we are entering the while loop with the first child already
    # recorded, and the sub count reduced appropraitely.
    # we need to look at the next packet listed to see if it has
    # subs
    while my_sub_count:
        # append the next item to our sub list while we still
        # have them to add
        current_index += 1
        child_index_list.append(current_index)
        print(f'{current_index}')
        # if the last item added has subs, create a skip list to see how
        # many indexes we need to step over before continuing our
        # count. We do this by calling ourselves and referencing the
        # largest number in the subs list returned
        print(my_clean_signal[current_index])
        if my_clean_signal[current_index][1] != 4:
            this_skip = max(index_subs(my_clean_signal, current_index, 1))
            furthest_skip = max(furthest_skip, this_skip)
            if furthest_skip <= len(my_clean_signal):
                current_index = furthest_skip
        my_sub_count -= 1

    return child_index_list


def parse_clean(my_clean_signal, instruction_string=''):

    if not instruction_string:
        # remove the summary from the head of the list
        my_clean_signal.pop(0)

    print(my_clean_signal)
    print(instruction_string)

    operator_list = []

    for i in range(len(my_clean_signal)):
        my_clean_signal[i].append(i)
        if len(my_clean_signal[i]) == 5:
            my_clean_signal[i][3] = index_subs(my_clean_signal, i)
            operator_list.append(None)
        else:
            operator_list.append(my_clean_signal[i][2])

    print(my_clean_signal)

    do_me = [my_clean_signal[0]]
    new_flag = True

    while do_me:
        if new_flag:
            line_tab = '\n'
            for to_dos in do_me:
                print(f'{line_tab}{to_dos[4]}:', end=' ')
                if to_dos[1] == 0:
                    print('Sum of', end=' ')
                elif to_dos[1] == 1:
                    print('Product of', end=' ')
                elif to_dos[1] == 2:
                    print('Minium of', end=' ')
                elif to_dos[1] == 3:
                    print('Maximum of', end=' ')
                elif to_dos[1] == 5:
                    print('Is > of', end=' ')
                elif to_dos[1] == 6:
                    print('Is < of', end=' ')
                else:
                    print('Is ==', end=' ')
                print(to_dos[3], end=' ')
                line_tab += ' '

        if len(do_me[-1]) == 5 and new_flag:
            new_flag = False
            for subs in do_me[-1][3]:
                if operator_list[subs] is None:
                    do_me.append(my_clean_signal[subs])
                    new_flag = True
            continue

        new_flag = True

        # perform the operation and put answer in output
        my_operator = do_me[-1][1]
        if my_operator == 0:
            print(f'{line_tab}Adding indexes {do_me[-1][3]}', end=' ')
            my_target_index = do_me[-1][4]
            my_sum = 0
            for i in do_me[-1][3]:
                print(f'+{operator_list[i]}', end='')
                my_sum += operator_list[i]
            do_me = do_me[:-1]
            operator_list[my_target_index] = my_sum
            print(f'{line_tab}Operator at index {my_target_index} now holds value {operator_list[my_target_index]}')
            continue

        elif my_operator == 1:
            print(f'{line_tab}Multiplying indexes {do_me[-1][3]}', end=' ')
            my_target_index = do_me[-1][4]
            my_prodcut = 1
            for i in do_me[-1][3]:
                print(f'*{operator_list[i]}', end='')
                my_prodcut *= operator_list[i]
            do_me = do_me[:-1]
            operator_list[my_target_index] = my_prodcut
            print(f'{line_tab}Operator at index {my_target_index} now holds value {operator_list[my_target_index]}')
            continue

        elif my_operator == 2:
            print(f'{line_tab}Minimum of indexes {do_me[-1][3]}', end=' ')
            my_target_index = do_me[-1][4]
            my_minimum = 999999999
            for i in do_me[-1][3]:
                if operator_list[i] < my_minimum:
                    print(f'{line_tab}New lowest found: {operator_list[i]}', end='')
                    my_minimum = operator_list[i]
            do_me = do_me[:-1]
            operator_list[my_target_index] = my_minimum
            print(f'{line_tab}Operator at index {my_target_index} now holds value {operator_list[my_target_index]}')
            continue

        elif my_operator == 3:
            print(f'{line_tab}Maximum of indexes {do_me[-1][3]}', end=' ')
            my_target_index = do_me[-1][4]
            my_maximum = -1
            for i in do_me[-1][3]:
                if operator_list[i] > my_maximum:
                    print(f'{line_tab}New greatest found: {operator_list[i]}', end='')
                    my_maximum = operator_list[i]
            do_me = do_me[:-1]
            operator_list[my_target_index] = my_maximum
            print(f'{line_tab}Operator at index {my_target_index} now holds value {operator_list[my_target_index]}')
            continue

        elif my_operator == 5:
            my_target_index = do_me[-1][4]
            value_a = operator_list[do_me[-1][3][0]]
            value_b = operator_list[do_me[-1][3][1]]
            print(f'{line_tab}Evaluating {value_a} > {value_b}')
            operator_list[my_target_index] = int(value_a > value_b)
            do_me = do_me[:-1]
            print(f'{line_tab}Operator at index {my_target_index} now holds value {operator_list[my_target_index]}')
            continue

        elif my_operator == 6:
            my_target_index = do_me[-1][4]
            value_a = operator_list[do_me[-1][3][0]]
            value_b = operator_list[do_me[-1][3][1]]
            print(f'{line_tab}Evaluating {value_a} < {value_b}')
            operator_list[my_target_index] = int(value_a < value_b)
            do_me = do_me[:-1]
            print(f'{line_tab}Operator at index {my_target_index} now holds value {operator_list[my_target_index]}')
            continue

        else:
            my_target_index = do_me[-1][4]
            value_a = operator_list[do_me[-1][3][0]]
            value_b = operator_list[do_me[-1][3][1]]
            print(f'{line_tab}Evaluating {value_a} == {value_b}')
            operator_list[my_target_index] = int(value_a == value_b)
            do_me = do_me[:-1]
            print(f'{line_tab}Operator at index {my_target_index} now holds value {operator_list[my_target_index]}')
            continue

    print(f'\n\nFinal value of {operator_list[0]}\n\n')


if __name__ == '__main__':
    new_signal = read_file()
    print(new_signal)
    new_signal = process_signal(new_signal)
    print(new_signal)

    main_signal = run_signal(new_signal, [0, len(new_signal)])
    print(main_signal)

    parse_clean(main_signal)

    packet_sum = 0
    for item in main_signal:
        packet_sum += item[0]
    print('Packet Version Sum:', sum)
