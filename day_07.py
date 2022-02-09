raw_data = open("day_07.dat", "r").readlines()
clean_data = [int (x) for x in raw_data[0].split(",")]

print(clean_data)

def give_sigma(number):
    my_total = 0

    if number < 2:
        return number
    else:
        if number % 2 == 0:
            my_total = ((number + 1) * (int(number / 2)))
        else:
            my_total = ((number + 1) * (int(number / 2)) + (int(number / 2) + 1))

    return my_total


def get_cost(my_data, target):
    total = 0

    # print("pos", target, end=" ")
    for crab in my_data:
        this_cost = abs(crab - target)
        this_cost = give_sigma(this_cost)
        total += this_cost
    # print("Total=", total)

    # print(" =", total)
    return total


largest = 0
costs = []
for i in range(len(clean_data)):
    if clean_data[i] > largest: largest = clean_data[i]

for i in range(largest):
    costs.append(get_cost(clean_data, i))

print(costs)

smallest = 999999999999999999
for i in range(len(costs)):
    if costs[i] < smallest:
        smallest = costs[i]

print("Least Cost:", smallest)

