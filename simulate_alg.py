"""
Script for simulating use of scheduling algorithm in alg.py.
"""

from alg import Algorithm
import numpy as np
from numpy import random as rand

rand.seed(123456)

# num_tasks is the number of tasks
num_tasks = 10 # 100, 1000, 10000

# stages[i] is the number of stages for task i
stages = [3] * num_tasks

# time[i][l] is the runtime for the first l stages of task i (cumulative)
time = []
for task_idx, num_stages in enumerate(stages):
    cur_times = []
    for stage_idx in range(num_stages):
        # Sample times uniformly then sort
        if stage_idx == 0:
            sampled_time = rand.uniform(0, 1)
        else:
            sampled_time = rand.uniform(cur_times[-1], 1)
        cur_times.append(sampled_time)
    time.append(cur_times)
    
# prec[i][l] is the expected prec for completing the first l stages of task i before the deadline
# prec = [[12,15,16,17,17], [2,6,6], [3,3,4,6]]
prec = []
for task_idx, num_stages in enumerate(stages):
    cur_precs = []
    for stage_idx in range(num_stages):
        # Sample precisions uniformly then sort
        if stage_idx == 0:
            sampled_prec = rand.uniform()
        else:
            sampled_prec = rand.uniform(cur_precs[-1], 1)
        cur_precs.append(sampled_prec)
    prec.append(cur_precs)
 

# dead[i] is the deadline for task i 
# (we assume we begin running at time 0, so D[i] is the maximum permissable runtime before task i must have been run)
# Note that these are weakly increasing as per requirement of the algorithm
# For now, let all the deadlines be the one second period
deadline_per_task = .5 * num_tasks
dead = [deadline_per_task]*num_tasks

# the priority associated with each task
# Sample a uniform priority too
prio = []
for i in range(num_tasks):
    cur_prio = rand.uniform()
    prio.append(cur_prio)
#prio = [1]*num_tasks

verbose = True
if verbose:
    # print the inputs
    print("\nINPUTS:")
    print(num_tasks,"tasks with",stages,"stages")
    print("\nWith expected runtimes:")
    for i in range(len(time)):
        print(i,":",time[i])
    print("\nWith expected precisions:")
    for i in range(len(prec)):
        print(i,":",prec[i])
    print("\nWith priorities:")
    for i in range(len(prio)):
        print(i,":",prio[i])
    print("\nWith deadlines:")
    for i in range(len(dead)):
        print(i,":",dead[i])

    # call sched for these inputs
    verbose = True
    print("\n\nSOLUTION:")
    ours = Algorithm()
    yao = Algorithm(yao=True)
    print("\n\nOURS:")
    ours.sched(num_tasks, stages, time, prec, prio, dead, verbose)
    print("\n\nYAO:")
    yao.sched(num_tasks, stages, time, prec, prio, dead, verbose)
    print("")

