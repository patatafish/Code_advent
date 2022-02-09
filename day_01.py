raw_data = [int(x) for x in open("day_01.dat", "r").readlines()]
print("Data imported", raw_data[1:5], " ... ", raw_data[-5:-1])

# define variables for counting
depth_count = 0
size = len(raw_data)
print("There are", size, "items in my list.")

# loop list and count < comparisons
for i in range(size-1):
    if raw_data[i] < raw_data[i+1]:
        depth_count += 1

# display final count
print("\nOverall I found", depth_count, "increases in depth.")

# reset depth count for pt. 2
depth_count = 0

# loop the list for counts of 3
for i in range(size-3):
    # since we add [i]+[i1]+[i2] ?< [i1]+[i2]+[i3]
    # then we can cancel out indexes 1 and 2, and only compare
    # [i] ?< [i3] to see the larger sum of the 3 items.
    if(raw_data[i] < raw_data[i+3]):
        depth_count += 1


print("\nOverall I found", depth_count, "increases in depth.")
