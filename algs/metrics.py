"""
Functions for computing metrics on schedules.
These metrics give various ways to answer the question: how "good" is this schedule?
"""

import numpy as np

def is_valid_sched(depth_sched, num_tasks, stages, time, prec, prio, dead):
    """
    Confirms that the schedule implied by depth_sched is a valid schedule, meaning
    that all tasks finish execution before their deadline.
    """
    #TODO implement checks on valid inputs (assumes correct right now)

    cum_time = 0
    for i in range(num_tasks):
        cum_time += time[i][depth_sched[i]]
        if cum_time > dead[i]:
            print('Invalid depth schedule: must have total runtime at most the deadline')
            return False
    for i in range(len(depth_sched)):
        if depth_sched[i] < 0:
            print('Invalid depth schedule: must run the mandatory part of task',i)
            return False
    return True

def weighted_avg_metric(depth_sched, num_tasks, stages, time, prec, prio, dead):
    """
    Returns the sum of reward for all tasks under the given schedule, where
    reward is given by the function reward below.
    """
    # If the passed schedule is invalid, return 0.
    if not is_valid_sched(depth_sched, num_tasks, stages, time, prec, prio, dead):
        return -1

    cum_reward = 0
    for i in range(num_tasks):
        curprec = prec[i][depth_sched[i]]
        curprio = prio[i]
        cum_reward += reward(curprec, curprio)
    
    return cum_reward

def max_priority_metric(depth_sched, num_tasks, stages, time, prec, prio, dead):
    """
    Returns the precision achieved by the maximum priority task for this schedule.
    """
    # If the passed schedule is invalid, return 0.
    if not is_valid_sched(depth_sched, num_tasks, stages, time, prec, prio, dead):
        return 0

    #max_prio_task = np.argmax(prio)
    prio = np.array(prio)
    highest_prio_tasks = np.argsort(-1*prio)
    max_prio_task = highest_prio_tasks[0]
    return prec[max_prio_task][depth_sched[max_prio_task]]

def simple_precision_metric(depth_sched, num_tasks, stages, time, prec, prio, dead):
    """
    Returns the precision achieved by the maximum priority task for this schedule.
    """
    # If the passed schedule is invalid, return 0.
    if not is_valid_sched(depth_sched, num_tasks, stages, time, prec, prio, dead):
        return 0

    cum_reward = 0
    for i in range(num_tasks):
        curprec = prec[i][depth_sched[i]]
        curprio = prio[i]
        cum_reward += reward(curprec, curprio)
    
    return cum_reward

def reward(prec, prio):
    """
    Computes 
        reward= prec * prio
    where prec, prio in [0,1].
    Returns reward.
    """
    # Each prec and prio should be in [0,1)
    if prec < 0 or prec >= 1:
        raise ValueError("precision {} should have: 0 <= p < 1".format(prec))
    if prio < 0 or prio > 1:
        raise ValueError("priority {} should have: 0 <= p <= 1".format(prio))

    return prec * prio
