This project solves problem with binary (0 or 1) decision-making variables.

To change project to accept integer decision-making variables proceed these steps:
1. Change "data" list of dictionaries to inlude dictionary for each task (with fields: name, taskNum, time - list of times for each processor).
2. Rewrite "fitness" function, where every individual has number of selected processor (from 1 to max_proc_num).
We don't have to count here "num_of_processors_for_each_task", so delete it and don't check it.
Count "time_for_each_processor" that way:
time_for_each_processor[selected-1] += item.get('time')[selected-1]

Other elements are preserved.
3. Rewrite "create_individual" function. Each individual has to get random processor num value "processor_num = random.randint(1, num_of_processors)". That's all.
4. Change mutate function, to change specified element.
Compute new element like: "newEl = max - (currEl - min)". For example: min=1, max=5, currEl = 2, newEl = 5-(2-1) = 5-1 = 4
