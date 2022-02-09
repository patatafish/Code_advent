raw_data = open("test.dat", "r").readlines()

# print(raw_data)

clean_data = []
for input in raw_data:
    temp_line = input.split("|")
    clean_data.append(temp_line)

# print(clean_data)

count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

for data_packet in clean_data:
    signal = data_packet[0]
    output = data_packet[1]

    clean_output = output.strip()
    temp_items = clean_output.split()
    # print(temp_items)
    for each_item in temp_items:
        my_length = len(each_item)
        count[my_length] += 1

    # print(count)

print(count[2] + count[3] + count[4] + count[7])

for data_packet in clean_data:
    signal = data_packet[0]
    output = data_packet[1]

    clean_output = output.strip()

    print("a:", signal, clean_output)

    clean_signal_list = signal.split()
    clean_output_list = clean_output.split()
    print("b:", clean_signal_list)
    print("c:", clean_output_list)

    # initialize list of lists
    decoder_ring = []
    # we use 0 to 6 as index for A to G
    for i in range(7):
        decoder_ring.append([])

    print("Starting Decoder Ring...")
    print(decoder_ring)

    # first locate the 1 by finding the only 2-long string
    print("looking...", end="")
    for my_item in clean_signal_list:
        if len(my_item) == 2:
            print(" found", my_item)
            # found the 1, update decoder ring
            for letter in my_item:
                decoder_ring[2].append(letter)
                decoder_ring[5].append(letter)
            break   # exit the loop looing for 1
        print(".", end="")

    print(decoder_ring)

    # next locate the 7, and we can find coded "a" from the remaining item
    print("looking...", end="")
    for my_item in clean_signal_list:
        if len(my_item) == 3:
            print(" found", my_item)
            # found the 7, now find what item is not in 1
            for letter in my_item:
                if letter == decoder_ring[2][0] or letter == decoder_ring[2][1]:
                    continue    # if letter is in position from 1, skip comparison and move on
                print(letter, "is the odd man out.")
                # we fond the letter, update decoder ring
                decoder_ring[0].append(letter)
            break
        print(".", end="")
    print(decoder_ring)

    # next locate a 6, we can find coded "c" from the missing item, then find coded "f" as well
    print("looking...", end="")
    for my_item in clean_signal_list:
        if len(my_item) == 6:
            # found a 6 long, start match count
            matches = 0
            # build a temp list to compare which letter is in other, but missing here
            temp_list = []
            temp_list.append(decoder_ring[0][0])
            temp_list.append(decoder_ring[2][0])
            temp_list.append(decoder_ring[2][1])

            # check to see if only 2 or all 3 match
            for letter in my_item:
                if letter in temp_list:
                    matches += 1

            # if we found the one with only 2 matching, we can ID position "c"
            # and also postion "f"
            if matches == 2:
                # save this item for camparison to 6 later
                my_six = my_item
                print(" found", my_item)
                for letter in my_item:
                    if letter in temp_list:
                        temp_list.remove(letter)
                last_letter = temp_list.pop()
                print(last_letter, "is the odd man out.")
                # update the decoder ring
                decoder_ring[2].clear()
                decoder_ring[2].append(last_letter)
                for i in range(2):
                    if decoder_ring[5][i] == last_letter:
                        decoder_ring[5].pop(i)
                        break   # break once popped to avoid going out of bounds on list

                break   # break out of search once we find our 9 and update decoder ring

            print(".", end="")
    print(decoder_ring)

    # find the 6, locate the one difference fromt he 9, and find coded "e"
    print("looking against", my_six, end="...")
    for my_item in clean_signal_list:
        if my_item == my_six:
            continue    # if we found the nine again, keep looking

        if len(my_item) == 6:
            
        print(".", end="")

    break