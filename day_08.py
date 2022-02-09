def ring_remove(decoder_ring, outer_ring, inner_ring):
    if inner_ring in decoder_ring[outer_ring]:
        decoder_ring[outer_ring].remove(inner_ring)
    return decoder_ring

def decode_output(decoder_ring, output_list):

    my_keys = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    my_translation = dict(zip(decoder_ring, my_keys))

    # print(my_translation)

    temp_list = []
    for number in output_list:
        temp_string = ""
        for letter in number:
            temp_string += my_translation[letter]

        # temp_string = "".join(sorted(temp_string))
        temp_list.append(temp_string)

    del(number, letter, temp_string)

    translated_list = []
    for number in temp_list:
        if len(number) == 7:
            translated_list.append(8)
        elif len(number) == 2:
            translated_list.append(1)
        elif len(number) == 4:
            translated_list.append(4)
        elif len(number) == 3:
            translated_list.append(7)
        elif len(number) == 5:
            if 'b' in number:
                translated_list.append(5)
            elif 'e' in number:
                translated_list.append(2)
            else:
                translated_list.append(3)
        else:
            if 'd' not in number:
                translated_list.append(0)
            elif 'c' in number:
                translated_list.append(9)
            else:
                translated_list.append(6)

    return translated_list



raw_data = open("day_08.dat", "r").readlines()

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

# variable clean up
del (raw_data, input, temp_line)
del (signal, output, temp_items)
del (count, each_item, my_length)

# define total for end output
total = 0

for data_packet in clean_data:
    signal = data_packet[0]
    output = data_packet[1]

    clean_output = output.strip()

    # print("a:", signal, clean_output)

    clean_signal_list = signal.split()
    clean_output_list = clean_output.split()
    # print("b:", clean_signal_list)
    # print("c:", clean_output_list)

    # initialize list of lists
    decoder_ring = []
    # we use 0 to 6 as index for A to G
    for i in range(7):
        decoder_ring.append(['a', 'b', 'c', 'd', 'e', 'f', 'g'])
    del(i)

    # print("Starting Decoder Ring...")
    # print(decoder_ring)


    # first locate the 1 by finding the only 2-long string
    # print("looking...", end="")
    for my_item in clean_signal_list:
        if len(my_item) == 2:
            # print(" found", my_item)
            # found the 1, update decoder ring
            decoder_ring[2].clear()
            decoder_ring[5].clear()
            for letter in my_item:
                decoder_ring = ring_remove(decoder_ring, 0, letter)
                decoder_ring = ring_remove(decoder_ring, 1, letter)
                decoder_ring[2].append(letter)
                decoder_ring = ring_remove(decoder_ring, 3, letter)
                decoder_ring = ring_remove(decoder_ring, 4, letter)
                decoder_ring[5].append(letter)
                decoder_ring = ring_remove(decoder_ring, 6, letter)
            break   # exit the loop looing for 1
        # print(".", end="")

    # print(decoder_ring)

    # next locate the 7, and we can find coded "a" from the remaining item
    # print("looking...", end="")
    for my_item in clean_signal_list:
        if len(my_item) == 3:
            # print(" found", my_item)
            # found the 7, now find what item is not in 1
            for letter in my_item:
                if letter == decoder_ring[2][0] or letter == decoder_ring[2][1]:
                    continue    # if letter is in position from 1, skip comparison and move on
                # print(letter, "is the odd man out.")
                # we found the letter, update decoder ring
                decoder_ring[0].clear()
                decoder_ring[0].append(letter)
                decoder_ring = ring_remove(decoder_ring, 1, letter)
                decoder_ring = ring_remove(decoder_ring, 2, letter)
                decoder_ring = ring_remove(decoder_ring, 3, letter)
                decoder_ring = ring_remove(decoder_ring, 4, letter)
                decoder_ring = ring_remove(decoder_ring, 5, letter)
                decoder_ring = ring_remove(decoder_ring, 6, letter)
            break
        # print(".", end="")

    # print(decoder_ring)

    # next locate a 6, we can find coded "c" from the missing item, then find coded "f" as well
    # print("looking...", end="")
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
                # print(" found", my_item)
                for letter in my_item:
                    if letter in temp_list:
                        temp_list.remove(letter)
                last_letter = temp_list.pop()
                # print(last_letter, "is the odd man out.")
                # update the decoder ring
                decoder_ring[2].clear()
                decoder_ring[2].append(last_letter)
                for i in range(2):
                    if decoder_ring[5][i] == last_letter:
                        decoder_ring[5].pop(i)
                        break   # break once popped to avoid going out of bounds on list

                break   # break out of search once we find our 9 and update decoder ring

            # print(".", end="")

    del(temp_list, matches, last_letter, i)

    # print(decoder_ring)

    # locate the 4, compare to the 7
    # print("looking...", end="")
    for my_item in clean_signal_list:
        if len(my_item) == 4:
            # print(" found", my_item)
            # we found the 4, find the 2 items not like the 7
            # build a temp list to compare which letter is in other, but missing here
            temp_list = []
            for letter in my_item:
                temp_list.append(letter)
            temp_list.remove(decoder_ring[2][0])
            temp_list.remove(decoder_ring[5][0])
            # print(temp_list[0], "and", temp_list[1], "are the odd men out.")
            # we have our list, update decoder ring
            decoder_ring[1].clear()
            decoder_ring[3].clear()
            for letter in temp_list:
                decoder_ring[1].append(letter)
                decoder_ring[3].append(letter)
                decoder_ring = ring_remove(decoder_ring, 4, letter)
                decoder_ring = ring_remove(decoder_ring, 6, letter)
            break

        # print(".", end="")

    del(temp_list)

    # print(decoder_ring)

    # find a 5, this will not have code "c"
    # print("looking...", end="")
    for my_item in clean_signal_list:
        if len(my_item) == 5 and decoder_ring[2][0] not in my_item:
            # print(" found", my_item)
            # we found a five, we can now know code g from remaining letters
            for letter in decoder_ring[6]:
                if letter in my_item:
                    # print(letter, "is the bottom item.")
                    # we found code g, update decoder ring
                    decoder_ring[6].clear()
                    decoder_ring[6].append(letter)
                    decoder_ring = ring_remove(decoder_ring, 4, letter)
            break
        # print(".", end="")

    # print(decoder_ring)


    # find a 3, this will have code "c" and code "f"
    # print("looking...", end="")
    for my_item in clean_signal_list:
        if len(my_item) == 5 and decoder_ring[2][0] in my_item and decoder_ring[5][0] in my_item:
            # print(" found", my_item)
            # found the 3, build a temp list to compare items to
            temp_list = []
            temp_list.append(decoder_ring[0][0])
            temp_list.append(decoder_ring[2][0])
            temp_list.append(decoder_ring[4][0])
            temp_list.append(decoder_ring[5][0])
            temp_list.append(decoder_ring[6][0])

            for letter in my_item:
                if letter in temp_list:
                    continue
                # print(letter, "is the odd man out.")
                # found the coded item for code "d", update the decoder ring
                decoder_ring[3].clear()
                decoder_ring[3].append(letter)
                decoder_ring = ring_remove(decoder_ring, 1, letter)
                break
            break
        # print(".", end="")

    del(temp_list)


    # clean up list of lists for ring
    for i in range(len(decoder_ring)):
        decoder_ring[i] = decoder_ring[i][0]

    # print("Final ring:")
    # print(decoder_ring)

    translated_numbers = decode_output(decoder_ring, clean_output_list)
    temp_number_string = ""
    for i in range(len(translated_numbers)):
        temp_number_string += str(translated_numbers[i])

    translated_numbers = int(temp_number_string)

    print(clean_output_list, "->", translated_numbers)

    total += translated_numbers

print(total)
