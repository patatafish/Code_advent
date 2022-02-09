raw_data = open("day_06.dat", "r").readlines()
print(raw_data)


def count_fish(population, days):
    if days % 5 == 0:
        print("Days:", days, "pop:", len(population))
    # count days down
    days -= 1

    # check 0's
    babies = 0
    for fish in range(len(population)):
        if population[fish] == 0:
            population[fish] = 6
            population.append(8)
        else:
            population[fish] -= 1

    if days == 0:
        return(len(population))

    return(count_fish(population, days))

# make 2 data sets to do part 1 and 2
clean_data = [int(x) for x in raw_data[0].split(',')]
copy_clean = [int(x) for x in raw_data[0].split(',')]
print(clean_data)
total_pop = count_fish(clean_data, 80)
print(total_pop)
# print(copy_clean)
# total_pop = count_fish(copy_clean, 256)
# print(total_pop)