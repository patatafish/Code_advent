# input the data
raw_data = open("day_02.dat", "r").readlines()

# init position data
length_pos = 0
depth_pos = 0

for line in raw_data:
    direction = line.split()
    # print(direction[0], "--", direction[1])
    if direction[0] == "forward":
        length_pos += int(direction[1])
        continue
    if direction[0] == "down":
        depth_pos += int(direction[1])
        continue
    if direction[0] == "up":
        depth_pos -= int(direction[1])


print("Final Length:", length_pos)
print("Final depth:", depth_pos)
print("Product:", depth_pos * length_pos)

# second calculations
length_pos = 0
depth_pos = 0
aim = 0

for line in raw_data:
    direction = line.split()
    if direction[0] == "forward":
        length_pos += int(direction[1])
        depth_pos += aim * int(direction[1])
        continue
    if direction[0] == "down":
        aim += int(direction[1])
        continue
    if direction[0] == "up":
        aim -= int(direction[1])

print("Final Length:", length_pos)
print("Final depth:", depth_pos)
print("Product:", depth_pos * length_pos)