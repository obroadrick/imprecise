"""
Simple greedy algorithm for the single processor, indepedent tasks model.
Assumes same deadline for all tasks.

Schedules mandatory parts then simply adds optional parts in order of priority.
"""

import numpy as np
import math

POS_INF = 10**10 

class GreedyPrime():
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

        # get the indexes of the highest priority tasks
        prio = np.array(prio)
        highest_prio_tasks = np.argsort(-1*prio)

        # get the tasks sorted in order of priority
        prio = np.array(prio)
        highest_prio_tasks = np.argsort(-1*prio)

 
        # now we add as many optional layers as possible, in order of greedy heuristic(s)
        time_used = mand_time
        idx = 0
        taskidx = highest_prio_tasks[idx]
        nextheur = 0
        left = 0
        no_more = 0
        # before looping around the search space, let's build up a table of heuristic evaluations of each stage
        """
        heurTable = [];
        for i in range(num_tasks):
            heurTable.append([])
            for j in range(stages[i]):
                if j > 0:
                    heurTable[i].append(heuristic(prec[i][j], priority[i], time[i][j] - time[i][j-1]):
                else:
        """
        while True:
            # now we consider adding stage stag to the schedule for task taskidx
            stag = depth_sched[taskidx] + 1
            if stag >= stages[taskidx]:
                # all the stages have been added already for this left-most task

                #### Kyle Comment: How do we know that we are at the left-most task? did we not just run it back to the top?
                #### Does this mean that we accidentally start to consider tasks later down the priority chain?

                left += 1
                if left >= num_tasks:
                    break
                no_more += 1
                idx = left
                taskidx = highest_prio_tasks[idx]

                #### Kyle Comment: does this continue make it so we reset if something later on does not fit, but reset one more to right?
                #### Basically a continuation of the concern above

                continue
            # if this stage doesn't fit in the schedule, move on
            if time_used + (time[taskidx][stag] - time[taskidx][stag-1]) > deadline:
                # couldn't add this stage since runtime would exceed the deadline

                #### Kyle Comment: This scares me that we may be recounting tasks that have been addressed as "no_more" since if it is not the left,
                #### it would still be in the queue on a later iteration
                
                no_more += 1
                if no_more >= num_tasks:
                    # once all tasks can't fit another stage, we are done scheduling
                    break
                # if this was the leftmost, move that over one too
                if idx == left:
                    left += 1
                    if left >= num_tasks:
                        break
                    idx = left
                # otherwise just move over 1
                else:
                    idx += 1
                if idx >= num_tasks:
                    idx = left
                taskidx = highest_prio_tasks[idx]
                continue
            #print('left:',left,'taskidx:',taskidx,'depth_sched:',depth_sched,'time_used:',time_used,'deadline:',deadline)
            # check if this stage is better than going back to the beginning for a new sweep (nextheur)
            curheur = heuristic(prec[taskidx][stag] - prec[taskidx][stag-1], prio[taskidx], time[taskidx][stag] - time[taskidx][stag-1])
            # instead of just checking the next stage's heuristic value, let's check the next k stages
            # to take advantage of the still-constant-time k-lookahead technique
            k = 5
            #for i in range(k):
            #    heurTable[
            if curheur >= nextheur or idx == left: #if back at left, we automatically add one stage
                # add this to the depth schedule
                depth_sched[taskidx] = stag
                time_used += time[taskidx][stag] - time[taskidx][stag-1] 
                #(next line assumes that stag-1 exists which is true when the first (mandatory stage) has been added)
                #print('setting depth_sched[',taskidx,'] to',stag)
                if idx == left:
                    # need to note down the nextheur value for comparison during this sweep
                    # but if the nextheur makes no sense since there aren't additional stages for this task, just move left over
                    if stag + 1 >= stages[taskidx]:
                        # just shift over left instead
                        left += 1
                        idx = left
                        if idx >= num_tasks:
                            break
                        taskidx = highest_prio_tasks[left]
                        continue
                    #nextheur = heuristic(prec[nexttaskidx][nextstag+1], prio[nexttaskidx], time[nexttaskidx][nextstag+1])
                    nextheur = heuristic(prec[taskidx][stag+1] - prec[taskidx][stag], prio[taskidx], time[taskidx][stag+1] - time[taskidx][stag+1])
                    """
                    nextidx = idx
                    nexttaskidx = highest_prio_tasks[nextidx]
                    nextstag = stag
                    done = False
                    while nextstag + 1 >= stages[nexttaskidx]:
                        nextidx += 1
                        if nextidx >= num_tasks:
                            done = True
                            break
                        nexttaskidx = highest_prio_tasks[idx]
                        nextstag = depth_sched[nexttaskidx] + 1
                    if done:
                        break
                    """
                idx += 1
                if idx >= num_tasks:
                    # go back to the beginning for a new sweep
                    idx = left
                taskidx = highest_prio_tasks[idx]
            else:
                # go back to the beginning for a new sweep
                idx = left
                taskidx = highest_prio_tasks[idx]
        # Return the depth schedule (EDF is used for the server to dispatch tasks)
        self.depth_sched = depth_sched
        return depth_sched

def heuristic(precision, priority, time):
    """ Returns a heuristic for how the 'goodness' of a potential stage. """
    return precision * priority / time
