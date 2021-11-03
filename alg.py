"""
API for scheduling using the algorithm presented in 
"Scheduling Real-time Deep Learning Services as Imprecise Computations"
by Yao et al.


NOTE
'sched' can be called by the server, passing a set of tasks and associated metadata.
'sched' will then return the correct depths to run the tasks at.
the server need not use any of the other functions here.
"""

import numpy as np
import math

POS_INF = 10**10 

class Algorithm():
    """
    The algorithm class maintains two tables S and P where:
        S[i][r] is the depth to which task i should be computed to achieve exactly reward r*delta in
                the minimum possible time.
        P[i][r] is the time (mentioned above) required to run the schedule implied by S[i][r].
                The schedule implied by S[i][r] is the schedule obtained by running the tasks to 
                the depths assigned by the solution S[i][r].
    """
    
    # The S and P tables as described above.
    S = None
    P = None

    # The maintained list of optimal depths. 
    # That is, depth_sched[i] is the number of stages to be run for task i in the selected schedule.
    depth_sched = []

    def __init__():
        """
        The algorithm class will populate the S and P solution tables once 
        tasks are passed (ie. sched is called).
        """
        S = None
        P = None

    def sched(num_tasks, stages, time, prec, prio, dead, verbose=False):
        """
        Schedules the passed tasks with associated metadata

        num_tasks   number of tasks
        stages      stages[i] is number of stages for task i
        time        time[i][l] is the expected runtime for the first l stages of task i (cumulative)
        prec        prec[i][l] is the expected precision achieved by running the first l stages of task i
        prio        prio[i] is the priority for task i
        dead        dead[i] is the deadline for task i

        """
        # TODO check inputs

        # Compute the expected rewards for all stages of all tasks
        # R[i][l] is the reward for completing the first l stages of task i before the deadline
        R = []
        for i in range(num_tasks):
            R.append([None]*stages[i])
            for l in range(stages[i]):
                R[i][l] = reward(prec[i][l], prio[i])

        # Find the solutions to all problems in tables S and P
        S, P = compute_tables_from_scratch(num_tasks, stages, time, R, dead)

        # Find optimal depths from the completed tables
        depth_sched, reward_sched, time_sched = find_optimal_depths_from_tables(S, P, R, time)

        # If verbose, print out the solution schedule that was found... messily for now... 
        if verbose:
            print("Schedule that achieves reward", sum(reward_sched), "  ")
            print(str(depth_sched)+"  ")
            print("with corresponding rewards for each task:"+"  ")
            print(str(reward_sched)+"  ")
            print("corresponding times for each task:"+"  ")
            print(str(time_sched)+"  ")
            print("or cumulatively:"+"  ")
            cum = []
            for time in time_sched:
                if len(cum) > 0:
                    cum.append(cum[-1] + time)
                else:
                    cum.append(time)
            print(str(cum)+"  ")

        # Return the depth schedule (the only item relevant to the server)
        return depth_sched

    def compute_tables_from_scratch(num_tasks, stages, time, R, dead):
        """
        Computes the solutions to S and P (tables as described by Yao et al)

        num_tasks   number of tasks
        stages      stages[i] is number of stages for task i
        time        time[i][l] is the expected runtime for the first l stages of task i (cumulative)
        R           R[i][l] is the expected reward for the first l stages of task i (cumulative)
        dead        dead[i] is the deadline for task i

        returns S, P the completed tables
        """
        # TODO check inputs
        # Establish shorthand for num_tasks
        N = num_tasks

        # Rmax is the maximum possible reward for a single task
        Rmax = max(max(R[i]) for i in range(len(R)))

        # delta is the basic increment of reward
        # NOTE this is a good place to play and have fun!
        delta = Rmax / 10

        # Compute useful constant
        Rmax_quantized = int(N*math.floor(Rmax/delta))

        # S[i][r] is the depth to which task i should be computed to optimally achieve exactly reward r*delta
        S = [[None for r in range(Rmax_quantized)] for i in range(N)]

        # P[i][r] is the time required to carry out the schedule implied by S[i][r]
        P = [[POS_INF for r in range(Rmax_quantized)] for i in range(N)]

        # Start by solving the first row of the table (first task)
        i = 0
        for r in range(0, Rmax_quantized): # for each level of reward
            # We need to find the depth which achieves reward r in minimum time
            # winning_l is that depth
            winning_l = None
            # winning_t is the corresponding worst-case runtime
            winning_t = POS_INF
            for l in range(stages[i]):
                # If this depth achieves reward r
                if R[i][l] == r:
                    # If this is the first such task, it is the current winner
                    if winning_l is None:
                        winning_l = l
                        winning_t = time[i][l]
                    # If the time to achieve this depth does so in less time than the current winner
                    elif time[i][l] < time[i][l]:
                        winning_l = l
                        winning_t = time[i][l]
            # Update this cell in S and P as long as the winning time abides by the task's deadline
            if winning_l is not None and winning_t <= dead[i]:
                S[i][r] = winning_l
                P[i][r] = winning_t

        # Sanity check
        #printSP(S,P)

        # Now for subsequent tasks we apply the same operations
        for i in range(1, N):
            for r in range(0, Rmax_quantized): # for each level of reward
                # We need to find the depth which achieves reward r in minimum time
                # winning_l is that depth
                winning_l = None
                # winning_t is the corresponding worst-case runtime
                winning_t = POS_INF
                # For each possible optimal depth, l
                for l in range(stages[i]):
                    # If this depth achieves reward r on its own
                    if R[i][l] == r:
                        # If this is the first sufficient depth, it is the current winner
                        if winning_l is None:
                            winning_l = l
                            winning_t = time[i][l]
                        # If the time to achieve this depth does so in less time than the current winner
                        elif time[i][l] < winning_t:
                            winning_l = l
                            winning_t = time[i][l]
                    # If this depth achieves some part of this reward but an earlier task
                    # achieves the remainder of the reward, for a total of r still
                    elif R[i][l] < r:
                        # r_ is the remaining portion of r
                        r_ = r - R[i][l]
                        # If the preceding task can earn the remaining portion of r
                        if S[i-1][r_] is not None:
                            # If this is the first sufficient depth, is is the current winner
                            if winning_l is None:
                                winning_l = l
                                winning_t = time[i][l] + P[i-1][r_]
                            # If the time to achieve this depth does so in less time than the current winner
                            elif time[i][l] + P[i-1][r_] < winning_t:
                                winning_l = l
                                winning_t = time[i][l] + P[i-1][r_]
             
                # Update this cell in S and P as long as the winning time is less than the deadline for this task
                if winning_l is not None and winning_t <= dead[i]:
                    S[i][r] = winning_l
                    P[i][r] = winning_t

        # Sanity check
        #printSP(S,P)

        # Return the completed tables
        return S, P

    def find_optimal_depths_from_tables(S, P, R, time):
        """
        Now that the tables are completed, we find the optimal path using the tables
        First we need to answer the following question about the last (latest deadline) task:
        which depth/layer achieves the highest reward with runtime sufficient to meet the deadline?

        S       S table
        P       P table
        R       rewards
        time    time table
        """
        # TODO check inputs
        N = len(S)

        i = N - 1
        # l_max is the optimal layer as described above
        l_max = None
        # r_max is the corresponding quantized reward
        r_max = None
        # For each reward for this task
        for r in range(len(S[i])):
            if S[i][r] is not None:
                r_max = r
                l_max = S[i][r]

        # If there is not possible order for this task... this is an unschedulable set of inputs
        if l_max is None:
            if verbose:
                # Indicate that no solution exists for these inputs
                print("No schedule for you... give nicer inputs"+"  ")
            return None #NOTE this is where we will make changes to handle an unschedulable input set
        else:
            # Now we construct the optimal schedule
            l_cur = l_max
            # r_ is the remaining reward
            r_ = r_max - R[N-1][l_max]
            depth_sched = [l_cur]
            reward_sched = [R[N-1][l_max]]
            time_sched = [time[N-1][l_max]]
            for i in range(N-2, -1, -1):
                l_cur = S[i][r_]
                r_ = r_ - R[i][l_cur]
                depth_sched.insert(0, l_cur)
                reward_sched.insert(0, R[i][l_cur])
                time_sched.insert(0, time[i][l_cur])

        assert sum(reward_sched) == r_max
        return depth_sched, reward_sched, time_sched

    def reward(prec, prio):
        # NOTE this is a good place to play and have fun!
        """
        Computes reward as a function of the precision and priority.
        For prec, prio in [0,1], computes prec * prio.
        """
        # TODO check inputs
        return prec * prio

    def printSP(S, P):
        """ 
        A scrappy function for printing the S and P tables for debugging.

        S   S[i][r] is the solution to S(i,r) as defined by Yao et al
        P   P[i][r] is the solution to P(i,r) as defined by Yao et al
        """
        # TODO check inputs
        print("\n")
        for i in range(len(S)):
            if S[i] == POS_INF:
                s = 'INF'
            else:
                s = str(S[i])
            print(str(i)+": "+s+"  ")
        for i in range(len(P)):
            if P[i] == POS_INF:
                s = 'INF'
            else:
                s = str(P[i])
            print(str(i)+": "+s+"  ")
     
        print("\n")
