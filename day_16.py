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
                clean_signal.append([my_ver, my_type, f'val:{new_literal}'])
                if my_end < target[1]:
                    clean_signal = run_signal(signal, [my_end, target[1]], clean_signal)
                    return clean_signal
        else:
            my_len = signal[my_end]
            my_end += 1
            if my_len == '0':
                sub_len = bin_to_dec(signal[my_end:my_end+15])
                my_end += 15
                clean_signal.append([my_ver, my_type, f's_len:{sub_len} bits'])
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
                clean_signal.append([my_ver, my_type, f's_len:{sub_len} members ({sub_bit_len} bits)'])

                clean_signal = run_signal(signal, [my_end, my_end+sub_bit_len], clean_signal)
                my_end += sub_bit_len
                if my_end < target[1]:
                    clean_signal = run_signal(signal, [my_end, target[1]], clean_signal)
                    return clean_signal

    return clean_signal

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

if __name__ == '__main__':
    signal = read_file()
    print(signal)
    signal = process_signal(signal)
    print(signal)

    clean_signal = run_signal(signal, [0, len(signal)])

    sum = 0;
    for item in clean_signal:
        sum += item[0]
    print('Packet Version Sum:', sum)
