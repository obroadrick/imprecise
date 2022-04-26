"""
Sample algorithm class that can be used as a template for future 
scheduling algorithms.
"""

import numpy as np
import math

POS_INF = 10**10 

class Algorithm():
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

        # Return the depth schedule (EDF is used for the server to dispatch tasks)
        # For this sample algorith, we just return '0' which is the index of just the 
        # first stage (the mandatory component of the task) for each task, a valid,
        # but not very advantageous schedule, leaving room for improved precisions.
        self.depth_sched = [0] * num_tasks
        return self.depth_sched
