"""
Script for simulating use of scheduling algorithm in alg.py.

At first, we assume that the times, precisions, and priorities are uniform [0,1].
Deadlines all 1 (end of current period).
"""

from alg import Algorithm
import numpy as np
from numpy import random as rand

rand.seed(5112)


# num_tasks is the number of tasks
num_tasks = 3 #rand.randint(2,10) # at some point...

# stages[i] is the number of stages for task i
stages = [2] * num_tasks

# time[i][l] is the runtime for the first l stages of task i (cumulative)
time = []
for task_idx, num_stages in enumerate(stages):
    cur_times = []
    for stage_idx in range(num_stages):
        # Sample times uniformly then sort
        sampled_time = rand.uniform()
        cur_times.append(sampled_time)
    cur_times.sort()
    time.append(cur_times)
    
# prec[i][l] is the expected prec for completing the first l stages of task i before the deadline
# prec = [[12,15,16,17,17], [2,6,6], [3,3,4,6]]
prec = []
for task_idx, num_stages in enumerate(stages):
    cur_precs = []
    for stage_idx in range(num_stages):
        # Sample precisions uniformly then sort
        sampled_prec = rand.uniform()
        cur_precs.append(sampled_prec)
    cur_precs.sort()
    prec.append(cur_precs)
 

# dead[i] is the deadline for task i 
# (we assume we begin running at time 0, so D[i] is the maximum permissable runtime before task i must have been run)
# Note that these are weakly increasing as per requirement of the algorithm
# For now, let all the deadlines be the one second period
dead = [1]*num_tasks

# the priority associated with each task
# Sample a uniform priority too
prio = []
for i in range(num_tasks):
    cur_prio = rand.uniform()
    prio.append(cur_prio)
#prio = [1]*num_tasks

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
a = Algorithm()
a.sched(num_tasks, stages, time, prec, prio, dead, verbose)
print("")

