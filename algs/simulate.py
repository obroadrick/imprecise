"""
Script for simulating use of scheduling algorithm in alg.py.
"""

from metrics import weighted_avg_metric, max_priority_metric
import numpy as np
from numpy import random as rand
import matplotlib.pyplot as plt
from tqdm import tqdm
from yao import Yao
from dynamic import Dynamic
from greedy import Greedy 

rand.seed(3141596)

def simulate(num_trials, algs, prio_dist='uniform', num_tasks=(2,30)):
    """
    Generates num_trials 'random' scheduling problems and solves them using each of the algorithms
    in the list algs. 
    #Returns num_tasks_list, our_initials, yao_initials, our_maxs, yao_maxs

    Arguments:
        num_trials  - the number of trials (simulated scheduling problems) to generate and run
        algs        - list of algorithm classes to be run on the simulated scheduling problems
        prio_dist   - the distribution from which the priority for each simulated task is drawn
                        as a string ('uniform' and 'beta' are current options but can easily add more)
        num_tasks   - num_tasks[0] is a lower bound and num_tasks[1] an upper bound on the number of tasks 
                        for each simulated scheduling problem (drawn uniformly)
    """
    print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
    num_algs = len(algs)
    # NOTE number of metrics being used to evaluate the schedules (could be played with)
    num_metrics = 2 
    results = []
    for i in range(num_algs):
        results.append(([], []))
        continue
        metric_results = []
        for i in range(num_metrics):
            metric_results.append([])
        results.append(metric_results)

    # Track the number of tasks in each generated trial (since it is selected at random)
    num_tasks_list = []
    trials_per_num_tasks = int(num_trials / (num_tasks[1] - num_tasks[0]))
    cur_num_tasks = num_tasks[0] - 1
    for i in tqdm(range(trials_per_num_tasks*(num_tasks[1] - num_tasks[0]+1))):
        # cur_num_tasks is the number of tasks
        # uniform in the passed range
        if i % trials_per_num_tasks == 0:
            cur_num_tasks += 1
        num_tasks_list.append(cur_num_tasks)

        # stages[i] is the number of stages for task i 
        # constant for now
        num_stages = 6
        stages = [num_stages] * cur_num_tasks

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
        # For now, let all the deadlines be half the total possible run time 
        # to force some dropping of layers but some inclusion of others
        total_mandatory_time = 0
        for i in range(cur_num_tasks):
            # assume we must run the *first* stage of each task
            total_mandatory_time += time[i][0]
        # also note that each task has maximum worst case run time at most 1 and so 
        # we choose a deadline between the minimum necesary for valid scheduling and the maximum worst case run time
        # note that since each task has at most 1 in runtime, cur_num_tasks*1 gives ~the total runtime of all tasks
        deadline_per_task = total_mandatory_time + .5 * (cur_num_tasks - total_mandatory_time)
        dead = [deadline_per_task] * cur_num_tasks

        # the priority associated with each task
        prio = []
        if prio_dist == 'uniform':
            # Sample a uniform priority
            for i in range(cur_num_tasks):
                cur_prio = rand.uniform()
                if cur_prio in prio:
                    print('ahhh!')
                prio.append(cur_prio)
        elif prio_dist == 'beta':
            # Sample from a beta distribution (high at 0 and 1, lower in between)
            a = .1
            b = .1 # paramters that give desired shape
            for i in range(cur_num_tasks):
                cur_prio = rand.beta(a, b)
                prio.append(cur_prio)

        verbose = False
        if verbose:
            # print the inputs
            print("\nINPUTS:")
            print(cur_num_tasks,"tasks with",stages,"stages")
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
            print("\n\nSOLUTION:")

        # Instantiate objects for each of the algorithms
        algorithms = []
        for alg in algs:
            algorithms.append(alg())

        for i, alg in enumerate(algorithms):
            # Call sched for these inputs (for this scheduling problem, run the algorithm)
            depth_sched = alg.sched(cur_num_tasks, stages, time, prec, prio, dead, verbose=False)

            # Evaluate the resulting schedule for both the weighted average metric and the max priority metric
            print(alg.__class__.__name__)
            print('depth_sched',depth_sched)
            weightavg = weighted_avg_metric(depth_sched, cur_num_tasks, stages, time, prec, prio, dead)
            maxprio = max_priority_metric(depth_sched, cur_num_tasks, stages, time, prec, prio, dead)
            if weightavg == -1:
                print('Invalid schedule returned by '+alg.__class__.__name__)

            if verbose:
                print("\n\n Metrics for measuring algorithm performance: how good is this schedule?")
                print("weighted average metric: {}".format(weightavg))
                print("max priority task metric: {}".format(maxprio))
                print("")

            # record both metrics for this (ith) algorithm's schedule
            results[i][0].append(weightavg)
            results[i][1].append(maxprio)
    return num_tasks_list, results

def plot(num_tasks_list, results, alg_names, metric_idx, metric_name):
    """
    Plots simulation results as they are returned by the simulate function.

    Arguments:
        num_tasks_list  - as returned by simulate
        results         - as returned by simulate
        metric_idx      - results may have multiple evaluated "scores" which use different metrics, so
                            this is the index of the metric to plot
        alg_names       - names of the algorithms (in same order as in results)
    """
    markers = ['gx', 'b+', 'r1']
    for idx, algname in enumerate(alg_names):
        plt.plot(num_tasks_list, results[idx][metric_idx], markers[idx], label=algname)
    plt.xlabel('Number of Tasks')
    plt.ylabel(metric_name)
    title = 'Simulation Results by '+metric_name
    plt.title(title)
    plt.legend(loc='lower right')
    plt.grid()
    plt.show()

# Run simulations
num_trials = 150
prio_dist = 'beta'
algs = [Yao, Dynamic, Greedy]
alg_names = ['Unmodified Dynamic Programming (Yao)', 'Dynamic Programming with Modified Reward', 'Greedy Algorithm']
num_tasks_list, results = simulate(num_trials, algs, prio_dist=prio_dist, num_tasks=(2,30))

# Plot results
metric_name = 'Sum of Precisions Weighted by Priorities'
metric_idx = 0
plot(num_tasks_list, results, alg_names, metric_idx, metric_name)
metric_name = 'Precision of Maximum Priority Task'
metric_idx = 1 # max priority
plot(num_tasks_list, results, alg_names, metric_idx, metric_name)

"""
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
"""
