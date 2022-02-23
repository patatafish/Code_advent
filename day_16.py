# file io
def read_file(filename='test.dat'):
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
        clean_signal = []
        clean_signal.append([0, 0, f'signal is {len(signal)} bits'])
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

    while my_signal:
        member_count += 1
        this_type = bin_to_dec(my_signal[3:6])
        if this_type == 4:
            my_end = 11
            while my_signal[my_end-5] is '1':
                my_end += 4

            my_signal = my_signal[my_end:]
        else:
            this_len = my_signal[6]
            if this_len is '1':
                member_number = my_signal[7:18]
                member_number = bin_to_dec(member_number)
                # member_count += member_number
                my_signal = my_signal[18+scan_len(my_signal, 18, member_number):]
            else:
                my_sub_len = bin_to_dec(my_signal[7:22])
                # member_count += scan_count(my_signal[22:22+my_sub_len])
                my_signal = my_signal[22+my_sub_len:]


    return member_count

def scan_len(signal, my_start, my_number):
    counted_subs = 0
    my_sub_len = 0 + my_start
    while counted_subs < my_number:
        temp1 = signal[my_start:my_start+6]
        counted_subs += 1
        my_type = signal[my_start+3:my_start+6]
        my_start += 6
        if my_type == '100':
            while True:
                temp = signal[my_start:my_start+5]
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
                    temp3 = signal[my_start:my_start+15]
                    my_start += 15
                    temp3 = bin_to_dec(temp3)
                    my_start += temp3
                elif index == '1':
                    temp4 = bin_to_dec(signal[my_start:my_start+11])
                    my_start += 11
                    target_len = scan_len(signal, my_start, temp4)
                    my_start += target_len

    return my_start - my_sub_len

def get_type(signal, my_ending_bit):
    my_version = signal[my_ending_bit:my_ending_bit+3]
    my_type = signal[my_ending_bit+3:my_ending_bit+6]
    return my_ending_bit + 6, my_version, my_type


def index_subs(my_clean_signal, parent_index):
    child_index_list = []

    my_sub_count = my_clean_signal[parent_index][3]
    current_index = parent_index + 1

    # the next item is always a sub of our current item,
    # add it to the sub index and count it
    child_index_list.append(current_index)
    my_sub_count -= 1

    while my_sub_count:

        # if we are looking at a literal, increase the index and count
        # straight across the index (don't skip)
        if my_clean_signal[current_index][1] == 4:
            current_index += 1
            child_index_list.append(current_index)
            my_sub_count -= 1
            continue
        # if we are looking at an operator packet, skip the content it has
        # until we surface out of its sub list
        # we do this by calling ourselves, and adding the index
        # of the last item on our own sub list
        else:
            skip_list = index_subs(my_clean_signal, current_index)
            current_index = skip_list[-1] + 1
            child_index_list.append(current_index)
            my_sub_count -= 1
            continue

    return child_index_list


def parse_clean(my_clean_signal, instruction_string = '', eval_total = 0):

    if not instruction_string:
        # remove the summary from the head of the list
        my_clean_signal.pop(0)

    print(my_clean_signal)
    print(instruction_string)

    current_type = my_clean_signal[0][1]
    current_sub_count = my_clean_signal[0][3]

    for i in range(len(my_clean_signal)):
        if len(my_clean_signal[i]) == 4:
            my_clean_signal[i][3] = index_subs(my_clean_signal, i)

    print(my_clean_signal)

    do_me = [my_clean_signal[0]]

    output = []

    while do_me:
        print(do_me)
        if len(do_me[-1]) == 4 :
            for subs in do_me[-1][3]:
                do_me.append(my_clean_signal[subs])
            continue

        last_instruction = len(do_me) - 1

        # back up to the last operator packet in our list of literals
        while len(do_me[last_instruction]) == 3:
            last_instruction -= 1

        # perform the operation and put answer in output
        my_operator = do_me[last_instruction][1]
        if my_operator == 0:
            this_sum = 0
            for i in range(last_instruction+1, len(do_me)):
                this_sum += do_me[i][2]
            do_me = do_me[:last_instruction]
            output.append(this_sum)
            continue


        # you need to create parallel lists here.
        # keep the literal values in each and process them
        # puch the stack the same but with consolodated values
        # at index of operator packet instead of in a total int







if __name__ == '__main__':
    signal = read_file()
    print(signal)
    signal = process_signal(signal)
    print(signal)

    clean_signal = run_signal(signal, [0, len(signal)])
    print(clean_signal)

    parse_clean(clean_signal)

    sum = 0;
    for item in clean_signal:
        sum += item[0]
    print('Packet Version Sum:', sum)
