raw_data = open("day_06.dat", "r").readlines()
clean_data = [int(x) for x in raw_data[0].split(',')]
print(clean_data)

# build initial counts
population = []
for i in range(9):
    population.append(0)

print(population)

for fish in clean_data:
    population[fish] += 1

print(population)

# days count
day_count = 256

# while loop for each day
while day_count > 0:
    day_count -= 1

    babies = population[0]

    population[0] = population[1]
    population[1] = population[2]
    population[2] = population[3]
    population[3] = population[4]
    population[4] = population[5]
    population[5] = population[6]
    population[6] = population[7] + babies
    population[7] = population[8]
    population[8] = babies

total_pop = 0
for i in population:
    total_pop += i

print("Total:", total_pop)