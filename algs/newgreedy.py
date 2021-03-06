"""
Simple greedy algorithm for the single processor, indepedent tasks model.
Assumes same deadline for all tasks.

Schedules mandatory parts then simply adds optional parts in order of priority.
"""

import numpy as np
import math

POS_INF = 10**10 

class NewGreedy():
    # The maintained list of optimal depths. 
    # That is, depth_sched[i] is the number of stages to be run for task i in the selected schedule.
    # i.e. this is where the solution for the current optimal schedule gets stored
    depth_sched = []

    def __init__(self):
        self.depth_sched = []

    def sched(self, num_tasks, stages, time, prec, prio, dead, verbose=False):
        """
        Schedules the passed tasks with associated metadata

        num_tasks   number of tasks
        stages      stages[i] is number of stages for task i
        time        time[i][l] is the expected runtime for the first l stages of task i (cumulative)
        prec        prec[i][l] is the expected precision achieved by running the first l stages of task i
        prio        prio[i] is the priority for task i
        dead        dead[i] is the deadline for task i

        """

        # Check for correct inputs
        if not isinstance(num_tasks, int) or num_tasks < 0:
            raise ValueError("num_tasks should be a positive integer")
        if not len(stages) == num_tasks:
            raise ValueError("stages should have length num_tasks")
        if not len(time) == num_tasks:
            raise ValueError("time should have length num_tasks")
        for task_idx, time_list in enumerate(time):
            if not len(time_list) == stages[task_idx]:
                raise ValueError("time[i] should have length stages[i]")
        for task_idx, prec_list in enumerate(prec):
            if not len(prec_list) == stages[task_idx]:
                raise ValueError("prec[i] should have length stages[i]")
        if not len(prec) == num_tasks:
            raise ValueError("prec should have length num_tasks")
        if not len(prio) == num_tasks:
            raise ValueError("prio should have length num_tasks")
        if not len(dead) == num_tasks:
            raise ValueError("dead should have length num_tasks")

        # intially, we need to schedule the mandatory components
        depth_sched = [0] * num_tasks

        # check how much time is needed by mandatory parts of tasks
        mand_time = 0
        for i in range(len(time)):
            mand_time += time[i][0] #first stage encapsulates all mandatory work for a task

        # if extra time, we keep scheduling
        deadline = dead[0] #assume same deadline for all tasks
        if mand_time > deadline:
            return None
        time_used = mand_time

        # get the indexes of the highest priority tasks
        prio = np.array(prio)
        highest_prio_tasks = np.argsort(-1*prio)

        # simple greedy strategy at a high level:
        # 1. compute a heuristic for each possible stage based on cumulative addition/scheduling of that stage
        # 2. sort all stages by this heuristic
        # 3. add as many stages as possible in order of this heuristic ranking

        # now these steps are implemented below
        # 1. compute a heuristic for each possible stage based on cumulative addition/scheduling of that stage
        heur_table = [];
        for i in range(num_tasks):
            heur_table.append([])
            for j in range(stages[i]):
                heur_table[i].append(heuristic(prec[i][j], prio[i], time[i][j]))

        # 2. sort all stages by this heuristic
        heur_table = np.array(heur_table)
        i = (-1*heur_table).argsort(axis=None, kind='mergesort')
        j = np.unravel_index(i, heur_table.shape)
        sortedStages = np.vstack(j).T
        #print(sortedStages.shape)
        #print(sortedStages)

        # 3. add as many stages as possible in order of this heuristic ranking
        for i in range(len(sortedStages)):
            tn,sn = sortedStages[i]
            # confirm that this stage has not already been added to the depth schedule 
            # (eg if a later stage than this had already been added for this task)
            if depth_sched[tn] >= sn:
                continue
            previous_depth = depth_sched[tn]
            new_time_added = time[tn][sn] - time[tn][previous_depth]
            # see if there is enough time remaining to schedule this stage
            if time_used + new_time_added > deadline:
                continue
            # now add this stage to the depth schedule
            depth_sched[tn] = sn
            time_used += new_time_added

        # Return the depth schedule (EDF is used for the server to dispatch tasks)
        self.depth_sched = depth_sched
        return depth_sched

def heuristic(precision, priority, time):
    """ Returns a heuristic for how the 'goodness' of a potential stage. """
    return precision * priority / time
