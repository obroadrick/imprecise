"""
This script runs simulations of imprecise computation model scheduling.
"""

from simulate import simulate, plot, plot_avgs, plot_improvements
from metrics import weighted_avg_metric, max_priority_metric
import numpy as np
from numpy import random as rand
import matplotlib.pyplot as plt
from tqdm import tqdm
from yao import Yao
from dynamic import Dynamic
from greedy import Greedy 
import random



# Set the seed for the pseudonrandom number generator used for the simulations
rand.seed(31415926)

# Run simulations
num_trials = 1000
#prio_dist = 'uniform'
prio_dist = 'normal'
#prio_dist = 'skew_right'
algs = [Yao, Dynamic, Greedy]
alg_names = ['Unmodified Dynamic Programming (Yao)', 'Dynamic Programming with Modified Reward', 'Greedy Algorithm']
num_tasks_list, results, avg_results = simulate(num_trials, algs, prio_dist=prio_dist, num_tasks=(2,30))

"""
# Plot all results
metric_name = 'Sum of Precisions Weighted by Priorities'
metric_idx = 0
plot(num_tasks_list, results, alg_names, metric_idx, metric_name)
metric_name = 'Precision of Maximum Priority Task'
metric_idx = 1 # max priority
plot(num_tasks_list, results, alg_names, metric_idx, metric_name)
"""

# Plot average results
metric_name = 'Sum of Precisions Weighted by Priorities'
metric_idx = 0 # weighted sum of precs
plot_avgs(num_tasks_list, avg_results, alg_names, metric_idx, metric_name)
metric_name = 'Precision of Maximum Priority Task'
metric_idx = 1 # max priority
plot_avgs(num_tasks_list, avg_results, alg_names, metric_idx, metric_name)

# Plot percent improvements
metric_name = 'Sum of Precisions Weighted by Priorities'
metric_idx = 0 # weighted sum of precs
plot_improvements(num_tasks_list, avg_results, alg_names, metric_idx, metric_name)
metric_name = 'Precision of Maximum Priority Task'
metric_idx = 1 # max priority
plot_improvements(num_tasks_list, avg_results, alg_names, metric_idx, metric_name)

