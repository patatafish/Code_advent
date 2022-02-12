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

if __name__ == '__main__':
    signal = read_file()
    print(signal)
    signal = process_signal(signal)
    print(signal)
    while signal:
        this_byte = signal[0:4]

        while True:
            if len(this_byte) < 4:
                this_byte += signal[0:4]
                signal = signal[4:]

            version = bin_to_dec(signal[0:3])

            type = bin_to_dec(signal[3:6])
        signal = signal[6:]
        print(f'Incoming signal: V.{version} T.{type}')
        if type == 4:
            literal = []
            while True:
                literal.append(signal[1:5])
                if signal[0] == '1':
                    signal = signal[5:]
                    continue
                else:
                    signal = signal[5:]
                    break

        break

