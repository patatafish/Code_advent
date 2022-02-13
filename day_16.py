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


def type_4(signal, my_ending_bit):
    my_literal = ''
    while True:
        my_literal += (signal[my_ending_bit+1:my_ending_bit+5])
        my_ending_bit += 5
        if signal[my_ending_bit-5] == '1':
            continue
        else:
            return my_literal, my_ending_bit


def filter_signal(signal, my_ending_bit):
    my_ending_bit += 4 - (my_ending_bit % 4)
    print(signal[my_ending_bit:my_ending_bit+4])
    while signal[my_ending_bit:my_ending_bit+4] == '0000':
        my_ending_bit += 4
    return my_ending_bit


if __name__ == '__main__':
    signal = read_file()
    print(signal)
    signal = process_signal(signal)
    print(signal)
    i=0
    for char in signal:
        i += 1
        print(char, end='')
        if i % 3 == 0:
            print()
    processed_signal = []
    while signal:
        ending_bit = 6
        version = bin_to_dec(signal[0:3])
        packet_type = bin_to_dec(signal[3:6])
        print(f'Incoming signal: V.{version} T.{packet_type}')
        if packet_type == 4:
            literal, ending_bit = type_4(signal, ending_bit)
            literal = bin_to_dec(literal)
            processed_signal.append([version, packet_type, literal])
        else:
            done = False
            sub_count = [0]
            while not done:
                if packet_type != 4:
                    length_id = signal[ending_bit]
                    ending_bit += 1
                if length_id is '0':
                    sub_packet_length = bin_to_dec(signal[ending_bit:ending_bit+15])
                    # sub_count.append(sub_packet_length)
                    ending_bit += 15
                    target = ending_bit + sub_packet_length
                    processed_signal.append([version, packet_type, f'length: {sub_packet_length} bits'])
                    while ending_bit != target:
                        sub_packet_version = bin_to_dec(signal[ending_bit:ending_bit+3])
                        sub_packet_type = bin_to_dec(signal[ending_bit+3:ending_bit+6])
                        ending_bit += 6
                        print(f'Sub packet found: V.{sub_packet_version} T.{sub_packet_type}')
                        if sub_packet_type != 4:
                            version = sub_packet_version
                            packet_type = sub_packet_type
                            sub_count[-1] -= 1
                            break
                        literal, ending_bit = type_4(signal, ending_bit)
                        literal = bin_to_dec(literal)
                        processed_signal.append([sub_packet_version, sub_packet_type, literal])
                        # do we need to adjust ending bit if we're sub packet?
                        # ending_bit = filter_signal(signal, ending_bit)
                        continue
                    done = True
                else:
                    sub_packet_length = bin_to_dec(signal[ending_bit:ending_bit+11])
                    sub_count.append(sub_packet_length)
                    ending_bit += 11
                    processed_signal.append([version, packet_type, f'length: {sub_packet_length} packets'])
                    for i in range(sub_packet_length):
                        sub_packet_version = bin_to_dec(signal[ending_bit:ending_bit+3])
                        sub_packet_type = bin_to_dec(signal[ending_bit+3:ending_bit+6])
                        ending_bit += 6
                        print(f'Sub packet found: V.{sub_packet_version} T.{sub_packet_type}')
                        if sub_packet_type != 4:
                            version = sub_packet_version
                            packet_type = sub_packet_type
                            break
                        literal, ending_bit = type_4(signal, ending_bit)
                        literal = bin_to_dec(literal)
                        processed_signal.append([sub_packet_version, sub_packet_type, literal])
                        sub_count[-1] -= 1
                        # don't adjust ending bit for sub-packets
                        # ending_bit = filter_signal(signal, ending_bit)
                        if not sub_count[-1]:
                            sub_count.pop(-1)
                            done = True
                    # i think we need adjustment here,
                    # but only if we've used type 4 and are "done"
                    if done:
                        ending_bit = filter_signal(signal, ending_bit)


        signal = signal[ending_bit:]

    sum = 0;
    for item in processed_signal:
        sum += item[0]
    print('Packet Version Sum:', sum)
