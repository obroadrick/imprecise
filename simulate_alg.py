"""
Script for simulating use of scheduling algorithm in alg.py.
"""

from alg import Algorithm
from metrics import initial_metric, max_priority_metric
import numpy as np
from numpy import random as rand
import matplotlib.pyplot as plt

rand.seed(134156)

def do_trials(num_trials, dist):
    # ours is the alg using weighted prec by prio
    # yao is default yao algorithm
    # initials means the initial results using the normal metric of weighted sum
    # maxs is the metric of maximum priority task's precision
    our_initials = []
    yao_initials = []
    our_maxs = []
    yao_maxs = []
    # we track the number of tasks since it can vary
    num_tasks_list = []

    for i in range(num_trials):
        # num_tasks is the number of tasks
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
        prio = []
        if dist == 'uniform':
            # Sample a uniform priority too
            for i in range(num_tasks):
                cur_prio = rand.uniform()
                prio.append(cur_prio)
        elif dist == 'beta':
            # Sample from a beta distribution (high at 0 and 1, lower in between)
            a = .1
            b = .1 # paramters that give desired shape
            for i in range(num_tasks):
                cur_prio = rand.beta(a, b)
                prio.append(cur_prio)

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
    return num_tasks_list, our_initials, yao_initials, our_maxs, yao_maxs

beta = True
#beta = False

num_trials = 100
dist = 'uniform'
u_num_tasks_list, u_our_initials, u_yao_initials, u_our_maxs, u_yao_maxs = do_trials(num_trials, dist)
if beta:
    dist = 'beta'
    b_num_tasks_list, b_our_initials, b_yao_initials, b_our_maxs, b_yao_maxs = do_trials(num_trials, dist)

# Metric: Weighted sum of prec's by prio's
plt.plot(u_num_tasks_list, u_our_initials, 'bo', label='Modified Alg with Uniform Priority')#, markersize=2)
plt.plot(u_num_tasks_list, u_yao_initials, 'g1', label='Unmodified Alg with Uniform Priority')#, markersize=2)
if beta:
    plt.plot(b_num_tasks_list, b_our_initials, 'm*', label='Modified Alg with Beta Priority')#, markersize=2)
    plt.plot(b_num_tasks_list, b_yao_initials, 'rx', label='Unmodified Alg with Beta Priority')#, markersize=2)
plt.xlabel('Number of Tasks')
plt.ylabel('Sum of Precisions Weighted by Priorities')
title = 'Simulation Results Evaluated by Weighted Sum of Precisions'
plt.title(title)
plt.legend(loc='lower right')
plt.grid()
plt.show()

# Metric: Prec of max prio task
plt.plot(u_num_tasks_list, u_our_maxs, 'bo', label='Modified Alg with Uniform Priority')#, markersize=2)
plt.plot(u_num_tasks_list, u_yao_maxs, 'g1', label='Unmodified Alg with Uniform Priority')#, markersize=2)
if beta:
    plt.plot(b_num_tasks_list, b_our_maxs, 'm*', label='Modified Alg with Beta Priority')#, markersize=2)
    plt.plot(b_num_tasks_list, b_yao_maxs, 'rx', label='Unmodified Alg with Beta Priority')#, markersize=2)
plt.xlabel('Number of Tasks')
plt.ylabel('Precision of Maximum Priority Task')
title = 'Simulation Results Evaluated by Precision of Maximum Priority Task'
plt.title(title)
plt.legend(loc='upper left')
plt.grid()
plt.show()

# Percent improvement by number of tasks (weighted sums)
plt.plot(u_num_tasks_list, 100 * np.array(u_our_initials) / np.array(u_yao_initials), 'bo', label='Uniform Priority')
plt.plot(b_num_tasks_list, 100 * np.array(b_our_initials) / np.array(b_yao_initials), 'rx', label='Beta Priority')
plt.xlabel('Number of Tasks')
plt.ylabel('Percent Improvement')
title = 'Percent Improvement (Weighted Sum of Precisions)'
plt.title(title)
plt.legend(loc='upper right')
plt.grid()
plt.show()

# Percent improvement by number of tasks (maxs)
plt.plot(u_num_tasks_list, 100 * np.array(u_our_maxs) / np.array(u_yao_maxs), 'bo', label='Uniform Priority')
plt.plot(b_num_tasks_list, 100 * np.array(b_our_maxs) / np.array(b_yao_maxs), 'rx', label='Beta Priority')
plt.xlabel('Number of Tasks')
plt.ylabel('Percent Improvement')
title = 'Percent Improvement (Precision of Maximum Priority Task)'
plt.title(title)
plt.legend(loc='upper right')
plt.grid()
plt.show()
