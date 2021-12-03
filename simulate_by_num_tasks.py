"""
Script for simulating use of scheduling algorithm in alg.py.
"""

from alg import Algorithm
from metrics import initial_metric, max_priority_metric
import numpy as np
from numpy import random as rand
import matplotlib.pyplot as plt

rand.seed(13456)

num_tasks_list = []
our_initials = []
yao_initials = []
our_maxs = []
yao_maxs = []

num_trials = 100

for i in range(num_trials):
    # num_tasks is the number of tasks
    #num_tasks = 10 # 100, 1000, 10000
    num_tasks = rand.randint(2, 100) # is inclusive
    num_tasks_list.append(num_tasks)

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
    # now prepend a 0 time item for each task corresponding to no completion
    for i in range(len(time)):
        time[i].insert(0,0)
        
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
    # now prepend a 0 prec item for each task corresponding to no completion
    for i in range(len(prec)):
        prec[i].insert(0,0)
     

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


    verbose = False
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

    if verbose:
        print("\n\nSOLUTION:")

    ours = Algorithm()
    yao = Algorithm(yao=True)

    # call sched for these inputs
    if verbose:
        print("\n\nOURS:")

    ours.sched(num_tasks, stages, time, prec, prio, dead, verbose)

    if verbose:
        print("\n\nYAO:")

    yao.sched(num_tasks, stages, time, prec, prio, dead, verbose)

    our_initial = initial_metric(ours.depth_sched, num_tasks, stages, time, prec, prio, dead)
    yao_initial = initial_metric(yao.depth_sched, num_tasks, stages, time, prec, prio, dead)
    our_max = max_priority_metric(ours.depth_sched, num_tasks, stages, time, prec, prio, dead)
    yao_max = max_priority_metric(yao.depth_sched, num_tasks, stages, time, prec, prio, dead)

    if verbose:
        print("\n\n Metrics for measuring algorithm performance: how good are these schedules?")
        print("metric for ours: {}".format(metric_ours))
        print("metric for yao: {}".format(metric_yao))
        print("")

    our_initials.append(our_initial)
    yao_initials.append(yao_initial)
    our_maxs.append(our_max)
    yao_maxs.append(yao_max)

plt.plot(num_tasks_list, yao_initials, 'bo', label='Unmodified Yao Algorithm')
plt.plot(num_tasks_list, our_initials, 'rx', label='Algorithm Accounting for Priority')
plt.xlabel('Number of Tasks')
plt.ylabel('Sum of Precisions Weighted by Priorities')
plt.legend(loc='lower right')
title = 'Simulation Results Evaluated by Weighted Sum of Precisions'
plt.title(title)
plt.grid()
plt.show()

plt.plot(num_tasks_list, yao_maxs, 'bo', label='Unmodified Yao Algorithm')
plt.plot(num_tasks_list, our_maxs, 'rx', label='Algorithm Accounting for Priority')
plt.xlabel('Number of Tasks')
plt.ylabel('Precision of Maximum Priority Task')
plt.legend(loc='lower right')
title = 'Simulation Results Evaluated by Precision of Maximum Priority Task'
plt.title(title)
plt.grid()
plt.show()











