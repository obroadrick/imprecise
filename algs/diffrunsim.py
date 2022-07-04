"""
This script runs simulations of imprecise computation model scheduling.
"""

from simulate import simulate, plot, plot_avgs, plot_improvements
from diffsimulate import diffsimulate, plot, plot_avgs, plot_improvements, plot_times
from metrics import weighted_avg_metric, max_priority_metric
import numpy as np
from numpy import random as rand
import matplotlib.pyplot as plt
from tqdm import tqdm
from yao import Yao
from dynamic import Dynamic
from greedy import Greedy 
from greedyprime import GreedyPrime
from greedylookahead import GreedyLookAhead
from newgreedy import NewGreedy
import random



# Set the seed for the pseudonrandom number generator used for the simulations
rand.seed(3141592)

# Run simulations
num_trials = 1000
prio_dist = 'uniform'
#prio_dist = 'skew_right'
#prio_dist = 'skew_left'
#prio_dist = 'normal'
#algs = [Yao, Dynamic, Greedy, GreedyPrime]
#alg_names = ['Unmodified Dynamic Programming (Yao)', 'Dynamic Programming with Modified Reward', 'Greedy Algorithm', 'GreedyPrime Algorithm']
#algs = [Dynamic, Greedy, GreedyPrime]
deltas = [.2, .1, .01]
algs = [Dynamic(deltas[0]), Dynamic(deltas[1]), Dynamic(deltas[2]), Greedy(), GreedyPrime(), NewGreedy()]
#alg_names = ['Dynamic Programming with Modified Reward', 'Greedy Algorithm', 'GreedyPrime Algorithm']
#alg_names = ['Dynamic Programming with Modified Reward', 'Greedy Algorithm', 'GreedyPrime Algorithm', 'Greedy With Look Ahead'];
alg_names = ['Dynamic '+str(deltas[0]), 
            'Dynamic '+str(deltas[1]), 
            'Dynamic '+str(deltas[2]), 
            'Simple Greedy', 
            'Sweeps Greedy', 
            'New Greedy'];
num_tasks_list, results, avg_results, elapsed = diffsimulate(num_trials, algs, prio_dist=prio_dist, num_tasks=(2,30))
print(elapsed)

"""
# Plot all results
metric_name = 'Sum of Precisions Weighted by Priorities'
metric_idx = 0
plot(num_tasks_list, results, alg_names, metric_idx, metric_name)
metric_name = 'Precision of Maximum Priority Task'
metric_idx = 1 # max priority
plot(num_tasks_list, results, alg_names, metric_idx, metric_name)
"""

"""
# Plot average results
metric_name = 'Sum of Precisions Weighted by Priorities'
metric_idx = 0 # weighted sum of precs
plot_avgs(num_tasks_list, avg_results, alg_names, metric_idx, metric_name)
metric_name = 'Precision of Maximum Priority Task'
metric_idx = 1 # max priority
plot_avgs(num_tasks_list, avg_results, alg_names, metric_idx, metric_name)
"""

# Plot percent improvements
metric_name = 'Sum of Precisions Weighted by Priorities'
metric_idx = 0 # weighted sum of precs
plot_improvements(num_tasks_list, avg_results, alg_names, metric_idx, metric_name)
metric_name = 'Precision of Maximum Priority Task'
metric_idx = 1 # max priority
plot_improvements(num_tasks_list, avg_results, alg_names, metric_idx, metric_name)

# Plot average time spent by each algorithm
plot_times(num_tasks_list, elapsed, alg_names, num_trials)
