# Data file 'data3.txt' renderer code
import io
import random


# Function to generate random values for tasks and proc nums
def genRandomValues(min_tasks_num, max_tasks_num, min_processors_num, max_processors_num):
    new_gen_task_num = random.randint(min_tasks_num, max_tasks_num)
    new_gen_proc_num = random.randint(min_processors_num, max_processors_num)
    return new_gen_task_num, new_gen_proc_num

def areRandomNumProper(gen_task_num, gen_proc_num):
    return gen_task_num >= 2*gen_proc_num


# CAN CHANGE THESE VALUES!
# Specify used range to generate values (there should be more tasks than processors)
min_tasks_num = 10
max_tasks_num = 50

min_processors_num = 3
max_processors_num = 10

min_task_time = 1
max_task_time = 5

# Declare actual generated values, and first generate
gen_task_num, gen_proc_num = genRandomValues(min_tasks_num, max_tasks_num, min_processors_num, max_processors_num)

# Generate values until conditions are not met
while not areRandomNumProper(gen_task_num, gen_proc_num):
    gen_task_num, gen_proc_num = genRandomValues(min_tasks_num, max_tasks_num, min_processors_num, max_processors_num)

print(f"rendered values:\ngen_task_num: {gen_task_num}\tgen_proc_num: {gen_proc_num}")

# Specify tasks times for particular processors (rows are tasks, columns are processors)
times_for_each_processor = [[0]*gen_proc_num for i in range(gen_task_num)]

# Generate times for each processor
for i in range(gen_task_num):
    for j in range(gen_proc_num):
        times_for_each_processor[i][j] = random.randint(min_task_time, max_task_time)

# Save generated values to file
f = io.open("data3.txt", mode="w", encoding="utf-8")
f.write(str(gen_task_num)+"\n")
f.write(str(gen_proc_num)+"\n")
for i in range(gen_task_num):
    f.write(str(i+1))
    for j in range(gen_proc_num):
        f.write(" "+str(times_for_each_processor[i][j]))
    if i != (gen_task_num-1):
        f.write("\n")
f.close()
