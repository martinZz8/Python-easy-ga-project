import io
import time
from pyeasyga import pyeasyga

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
                               mutation_probability=0.08,
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


# Set the GA's fitness function
ga.fitness_function = fitness

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
