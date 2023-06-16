# Same function as main.py, but with specified custom functions for crossing and mutation
import io
import math
import time
import random
from pyeasyga import pyeasyga

# Function to compare unique values in simple list
def isListOfUniqueValues(li):
    return len(set(li)) == len(li)


# Load data from data1.txt file
f = io.open("data3.txt", mode="r", encoding="utf-8")
content = f.read()
f.close()

# Start the timer
start_time = time.time()

# Get each line
lines = content.split("\n")

# Get num of tasks and processors
num_of_tasks = int(lines[0])
num_of_processors = int(lines[1])

# Get lines with times
times = lines[2:]
data = []

# Create list of dictionaries containing data about processors and tasks
for i in range(num_of_tasks):
    row_times = times[i].split(" ")[1:]
    int_row_times = list(map(lambda item: int(item), row_times))

    for j in range(num_of_processors):
        data.append({
            "name": f"p{j + 1}z{i + 1}",
            "processorNum": j + 1,
            "taskNum": i + 1,
            "time": int_row_times[j]
        })

# Initialise the GA with data
ga = pyeasyga.GeneticAlgorithm(data,
                               population_size=1000,
                               generations=20,
                               crossover_probability=0.8,
                               mutation_probability=0.05,
                               elitism=True,
                               maximise_fitness=False)


# Define a fitness function
def fitness(individual, data):
    num_of_processors_for_each_task = [0] * num_of_tasks
    time_for_each_processor = [0] * num_of_processors

    for selected, item in zip(individual, data):
        if selected:
            num_of_processors_for_each_task[item.get('taskNum') - 1] += 1
            time_for_each_processor[item.get('processorNum') - 1] += item.get('time')

    # Check if each task has exactly one processor...
    time_to_ret = 0
    has_proper_processors = True
    for item in num_of_processors_for_each_task:
        if item != 1:
        #if item == 0 or item > 5: #ALTERNATE VERSION OF ABOVE CONDITION (TO FASTEN GOOD INDIVIDUALS ESTABLISHMENT)
            has_proper_processors = False
            break

    # ...if not, then set time_to_ret to sum of all times
    if not has_proper_processors:
        for item in data:
            time_to_ret += item.get('time')
    # ... otherwise get the maximum time of every processor
    else:
        max_time = 0
        for one_time in time_for_each_processor:
            if one_time > max_time:
                max_time = one_time
        time_to_ret = max_time

    return time_to_ret


# Define a individual function
def create_individual(data2):
    # Generate individuals in that manner:
    # Select processor, to which every task is assigned (one task to one processor)
    individuals = [0]*len(data2)
    for task_num in range(1, num_of_tasks+1):
        processor_num = random.randint(1, num_of_processors)
        for i in range(len(data2)):
            item = data2[i]
            if item.get('taskNum') == task_num and item.get('processorNum') == processor_num:
                individuals[i] = 1
        # ** instead of inner for **
        # idx = (task_num-1)*num_of_processors+(processor_num-1)
        # individuals[idx] = 1

    return individuals


# Define a crossover function
def crossover(parent_1, parent_2):
    num_of_indexes = 3
    crossover_indexes = [0] * num_of_indexes
    while not isListOfUniqueValues(crossover_indexes):
        for i in range(num_of_indexes):
            crossover_indexes[i] = random.randrange(1, len(parent_1)) # we don't want first and last indexes to be generated
    crossover_indexes.sort()

    child_1 = parent_1[:crossover_indexes[0]] + \
              parent_2[crossover_indexes[0]:crossover_indexes[1]] + \
              parent_1[crossover_indexes[1]:crossover_indexes[2]] + \
              parent_2[crossover_indexes[2]:]

    child_2 = parent_2[:crossover_indexes[0]] + \
              parent_1[crossover_indexes[0]:crossover_indexes[1]] + \
              parent_2[crossover_indexes[1]:crossover_indexes[2]] + \
              parent_1[crossover_indexes[2]:]
    return child_1, child_2


# Define a mutation function
def mutate(individual):
    num_val_to_mutate = 1
    new_num_val_to_mutate = math.floor(len(individual) / 10)
    if new_num_val_to_mutate > num_val_to_mutate:
        num_val_to_mutate = new_num_val_to_mutate

    mutate_indexes = [0] * num_val_to_mutate

    # Generate mutate indexes
    while not isListOfUniqueValues(mutate_indexes):
        for i in range(num_val_to_mutate):
            mutate_indexes[i] = random.randrange(len(individual))

    # Mutate values under specified indexes
    for i in range(num_val_to_mutate):
        sel_idx = mutate_indexes[i]
        if individual[sel_idx] == 0:
            individual[sel_idx] = 1
        else:
            individual[sel_idx] = 0


# Define a selection function
def selection(population):
    # Gen only fitness values from population 'Chromosome' class objects list
    fitness_values = list(map(lambda item: item.fitness, population))

    # Specify min value of population
    min_fitness_value = fitness_values[0]
    for i in range(len(fitness_values)):
        if fitness_values[i] < min_fitness_value:
            min_fitness_value = fitness_values[i]

    # Select all items in population that has min value
    min_value_population = []
    for item in population:
        item_fitness = item.fitness
        if item_fitness == min_fitness_value:
            min_value_population.append(item)

    # Select item from minimum population
    selected_idx = random.randrange(len(min_value_population))

    # Get selected item
    selected_item = min_value_population[selected_idx]
    return selected_item


# Set the GA's custom functions
ga.fitness_function = fitness
ga.create_individual = create_individual
ga.crossover_function = crossover
ga.mutate_function = mutate
#ga.selection_function = selection

# Run the GA
ga.run()

# Print elapsed time
print("--- %s seconds ---" % (time.time() - start_time))

# Print all individuals
# for individual in ga.last_generation():
#     print(individual)

# Print the best individual result
best_individual = ga.best_individual()
print(f"best individual: {best_individual}")

# Print selected processors and tasks
selected_data = []
for idx, flag in enumerate(best_individual[1]):
    if flag:
        selected_data.append(data[idx])

print("Selected processors and tasks:")
for item in selected_data:
    print(item)
