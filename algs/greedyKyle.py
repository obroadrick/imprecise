"""
Simple greedy algorithm for the single processor, indepedent tasks model.
Assumes same deadline for all tasks.

Schedules mandatory parts then simply adds optional parts in order of priority.
"""

import numpy as np
import math

POS_INF = 10**10 

class GreedyKyle():
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

        ####### KVC: WOULD A BETTER ASSUMPTION BE THAT IT IS THE MINIMUM IN THE DEADLINE ARRAY?##########

        deadline = dead[0] #assume same deadline for all tasks
        if mand_time > deadline:
            return None

        # get the indexes of the highest priority tasks
        prio = np.array(prio)
        highest_prio_tasks = np.argsort(-1*prio)
 
        # now we add as many optional layers as possible, in order of greedy heuristic(s)
        time_used = mand_time
        idx = 0
        taskidx = highest_prio_tasks[idx]
        leftheur = 0
        left = 0
        no_more = 0

        ###### KVC: DO WE NEED TO ADJUST STAG? MIGHT NOT MAKE SENSE THAT WE ARE ADDRESSING LAYERS FAR DOWN THE PIPELINE FOR TASKS WITH 
        ###### KVC: UNSCHEDULED EARLIER TASKS ########

        while left < num_tasks:

          if idx >= num_tasks:
              idx = left
        
          taskidx = highest_prio_tasks[idx]

          if idx == left and (depth_sched[taskidx] + 1 >= stages[taskidx] or time_used + (time[taskidx][depth_sched[taskidx]+1]) > deadline):
              left += 1
              idx = left

          elif idx == left:
              leftheur = heuristic(prec[taskidx][depth_sched[taskidx] + 1] - prec[taskidx][depth_sched[taskidx]], prio[taskidx], time[taskidx][depth_sched[taskidx] + 1] - time[taskidx][depth_sched[taskidx]])
              time_used = time_used + time[taskidx][depth_sched[taskidx] + 1] - time[taskidx][depth_sched[taskidx]]
              depth_sched[taskidx] += 1
              idx += 1

          else:
              if depth_sched[taskidx] + 1 < stages[taskidx] and time_used + (time[taskidx][depth_sched[taskidx]+1]) <= deadline:
                  curheur = heuristic(prec[taskidx][depth_sched[taskidx] + 1] - prec[taskidx][depth_sched[taskidx]], prio[taskidx], time[taskidx][depth_sched[taskidx] + 1] - time[taskidx][depth_sched[taskidx]])
                  if curheur > leftheur:
                      time_used = time_used + time[taskidx][depth_sched[taskidx] + 1] - time[taskidx][depth_sched[taskidx]]
                      depth_sched[taskidx] += 1
                      idx += 1

                  else:
                      idx += 1

              else:
                  idx += 1


        # Return the depth schedule (EDF is used for the server to dispatch tasks)
        self.depth_sched = depth_sched
        return depth_sched

def heuristic(precision, priority, time):
    """ Returns a heuristic for how the 'goodness' of a potential stage. """
    return precision * priority / time
