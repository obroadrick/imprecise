"""
Tests for alg.py, the scheduling algorithm.

At least at first, a short script that works through a toy example.
Ultimately, we will have unit tests for exceptions and known results.
"""

from alg import sched


""" TEST THE CODE ON SOME SIMPLE INPUTS! """
# num_tasks is the number of tasks
num_tasks = 3

# stages[i] is the number of stages for task i
stages = [5,3,4]

# time[i][l] is the runtime for the first l stages of task i (cumulative)
time = [[2,3,5,7,9], [3,4,7], [1,9,9,12]]

# prec[i][l] is the expected prec for completing the first l stages of task i before the deadline
prec = [[12,15,16,17,17], [2,6,6], [3,3,4,6]]

# dead[i] is the deadline for task i 
# (we assume we begin running at time 0, so D[i] is the maximum permissable runtime before task i must have been run)
# Note that these are weakly increasing as per requirement of the algorithm
dead = [18, 19, 23]

# the priority associated with each task
prio = [1, 1, 1]

# print the inputs
print("\nINPUTS:")
print(num_tasks,"tasks with",stages,"stages")
print("with expected runtimes")
for i in range(len(time)):
    print(i,":",time[i])
print("with expected precisions")
for i in range(len(prec)):
    print(i,":",prec[i])
print("with priorities")
for i in range(len(prio)):
    print(i,":",prio[i])
print("with deadlines")
for i in range(len(dead)):
    print(i,":",dead[i])

# call sched for these inputs
verbose = True
print("\n\nSOLUTION:")
sched(num_tasks, stages, time, prec, prio, dead, verbose)
print("")

