"""
**Implements the Yao algorithm with modifications to the "reward" function.**

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

class Dynamic():
    """
    The algorithm class maintains two tables S and P where:
        S[i][r] is the depth to which task i should be computed to achieve at least 
                reward r*delta but less than reward (r+1)*delta in
                the minimum possible time.
        P[i][r] is the time (mentioned above) required to run the schedule implied by S[i][r].
                The schedule implied by S[i][r] is the schedule obtained by running the tasks to 
                the depths assigned by the solution S[i][r].
    """
    
    # The S and P tables as described above.
    S = None
    P = None

    # Delta, the basic quantization increment used for the dynamic programming algorithm
    delta = .001

    # The maintained list of optimal depths. 
    # That is, depth_sched[i] is the number of stages to be run for task i in the selected schedule.
    # i.e. this is where the solution for the current optimal schedule gets stored
    depth_sched = []

    def __init__(self):
        """
        The algorithm class will populate the S and P solution tables once 
        tasks are passed (ie. sched is called).
        """
        # Give some default values to other members
        self.S = None
        self.P = None
        self.delta = .1

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

        # delta is the basic increment of reward
        # NOTE this is a good place to play and have fun!
        delta = self.delta

        # Compute the expected rewards for all stages of all tasks
        # R[i][l] is the reward for completing the first l stages of task i before the deadline
        R = []
        for i in range(num_tasks):
            R.append([None]*len(prec[i]))
            for l in range(len(prec[i])):
                reward = self.reward(prec[i][l], prio[i])
                R[i][l] = self.quantize(reward, delta)

        # TODO add a sanity check here that R[i][l] is weakly increasing WRT l for all i

        if verbose:
            # Sanity check:
            print("R:")
            for i, r_list in enumerate(R):
                line = ""
                for j, r in enumerate(r_list):
                    line += " "+str(r)
                print(line)

        # Find the solutions to all problems in tables S and P
        if not self.compute_tables_from_scratch(num_tasks, stages, time, R, dead, delta):
            print('Error in compute_tables_from_scratch')
            exit()

        # COME BACK HERE

        """ too much
        if verbose:
            # Sanity check:
            self.printSP()
        """

        # Find optimal depths from the completed tables
        depth_sched, reward_sched, time_sched = self.find_optimal_depths_from_tables(R, time, verbose)

        # If verbose, print out the solution schedule that was found... messily for now... 
        if verbose:
            if depth_sched == None:
                print("No viable schedule for these inputs")
                return None
            print("Depth schedule that achieves reward", sum(reward_sched), "  ")
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
        self.depth_sched = depth_sched
        return depth_sched

    def compute_tables_from_scratch(self, num_tasks, stages, time, R, dead, delta):
        """
        Computes the solutions to S and P (tables as described by Yao et al)

        num_tasks   number of tasks
        stages      stages[i] is number of stages for task i
        time        time[i][l] is the expected runtime for the first l stages of task i (cumulative)
        R           R[i][l] is the expected reward for the first l stages of task i (cumulative)(quantized)
        dead        dead[i] is the deadline for task i
        delta       delta is the basic increment of reward used for quantization of the reward space

        returns S, P the completed tables
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
                raise ValueError("time[i] should have length stages[i] + 1")
        for task_idx, R_list in enumerate(R):
            if not len(R_list) == stages[task_idx]:
                raise ValueError("R[i] should have length stages[i]")
        if not len(dead) == num_tasks:
            raise ValueError("dead should have length num_tasks")

        # Establish shorthand variable names
        N = num_tasks

        # Rmax_quantized is the maximum possible reward for a single task (quantized)
        Rmax_quantized_single_task = int(math.floor(max(max(R[i]) for i in range(len(R)))))
        Rmax_quantized = Rmax_quantized_single_task * N

        # S[i][r] is the depth to which task i should be computed to optimally achieve at least reward r*delta but less than (r+1)*delta
        self.S = [[None for r in range(Rmax_quantized+1)] for i in range(N)]

        # P[i][r] is the time required to carry out the schedule implied by S[i][r]
        self.P = [[POS_INF for r in range(Rmax_quantized+1)] for i in range(N)]

        # Start by solving the first row of the table (first task)
        i = 0
        for r in range(Rmax_quantized+1): # for each level of reward
            # We need to find the depth which achieves reward r in minimum time
            # winning_l is that depth, and winning_t is the corresponding expected runtime
            winning_l = None
            winning_t = POS_INF
            for l in range(len(time[i])):
                # If this depth achieves reward r
                if R[i][l] == r:
                    # If this is the first such task, it is the current winner
                    if winning_l is None:
                        winning_l = l
                        winning_t = time[i][l]
                    # If the time to achieve this depth does so in less time than the current winner
                    elif time[i][l] < winning_t:
                        winning_l = l
                        winning_t = time[i][l]
            # Update this cell in S and P as long as the winning time abides by the task's deadline
            if winning_l is not None and winning_t <= dead[i]:
                self.S[i][r] = winning_l
                self.P[i][r] = winning_t

        """
        # Sanity check
        self.printSP()
        """

        # Now for subsequent tasks we apply the same operations (i.e. inductively build the solutions)
        for i in range(1, N):
            for r in range(Rmax_quantized+1): # for each level of reward
                # We need to find the depth which achieves reward r in minimum time
                # winning_l is that depth, and winning_t is the corresponding expected runtime
                winning_l = None
                winning_t = POS_INF
                # For each possible optimal depth, l
                for l in range(len(time[i])):
                    """ this won't work anymore, since we require the mandatory component of each task to be run first
                    # If this depth achieves reward r on its own
                    if R[i][l] == r:
                        # If this is the first sufficient depth, it is the current winner
                        #TODO remove this unneeded clause
                        if winning_l is None:
                            winning_l = l
                            winning_t = time[i][l]
                        # Otherwise, if the time to achieve this depth does so in less time than the current winner
                        elif time[i][l] < winning_t:
                            winning_l = l
                            winning_t = time[i][l]
                    # If this depth achieves reward r on its own
                    # If this depth achieves some part of this reward but an earlier task
                    # achieves the remainder of the reward, for a total of r still
                    if R[i][l] < r:
                    """
                    # r_ is the remaining portion of r
                    r_ = r - R[i][l] # HERE IS CHANGE
                    # If the preceding task can earn the remaining portion of r
                    if self.S[i-1][r_] is not None:
                        # If this is the first sufficient depth, is is the current winner
                        if winning_l is None:
                            winning_l = l
                            winning_t = time[i][l] + self.P[i-1][r_]
                        # If the time to achieve this depth does so in less time than the current winner
                        elif time[i][l] + self.P[i-1][r_] < winning_t:
                            winning_l = l
                            winning_t = time[i][l] + self.P[i-1][r_]
         
                # Update this cell in S and P as long as the winning time is less than the deadline for this task
                if winning_l is not None and winning_t <= dead[i]:
                    self.S[i][r] = winning_l
                    self.P[i][r] = winning_t

        """
        # Sanity check
        self.printSP()
        """

        # Return True on success
        return True

    def find_optimal_depths_from_tables(self, R, time, verbose=False):
        """
        Now that the tables are completed, we find the optimal path using the tables
        First we need to answer the following question about the last (latest deadline) task:
        which depth/layer achieves the highest reward with runtime sufficient to meet the deadline?

        R       rewards
        time    time table
        """
        # Assume S, P, and R are correct since they are generated internally.

        N = len(self.S)

        i = N - 1
        # l_max is the optimal layer as described above
        l_max = None
        # r_max is the corresponding quantized reward
        r_max = None
        # For each reward for this task
        for r in range(len(self.S[i])):
            if self.S[i][r] is not None:
                r_max = r
                l_max = self.S[i][r]

        # If there is not possible order for this task... this is an unschedulable set of inputs
        if l_max is None:
            #NOTE this is where we will make changes to handle an unschedulable input set
            return None, None, None

        # Now we construct the optimal schedule
        l_cur = l_max
        # r_ is the remaining reward
        r_ = r_max - R[N-1][l_max]
        depth_sched = [l_cur]
        reward_sched = [R[N-1][l_max]]
        time_sched = [time[N-1][l_max]]
        for i in range(N-2, -1, -1):
            l_cur = self.S[i][r_]
            r_ = r_ - R[i][l_cur]
            depth_sched.insert(0, l_cur)
            reward_sched.insert(0, R[i][l_cur])
            time_sched.insert(0, time[i][l_cur])
            if r_ == 0:
                #TODO remove this since it is outdated if the assumption is that all first layers are manditory
                # if 0 reward remains, the remaining tasks should all have depth 0
                for j in range(i):
                    # assign remaining tasks 0
                    depth_sched.insert(0, 0)
                    reward_sched.insert(0, 0)
                    time_sched.insert(0, 0)
                # then break, since we've built the whole schedule now
                break

        # depth_sched is a list of the depths to which each task should be run
        # reward_sched is a list of corresponding marginal rewards
        # time_sched is a list of corresponding marginal runtimes
        return depth_sched, reward_sched, time_sched

    def reward(self, prec, prio):
        # NOTE this is a good place to play and have fun!
        """
        Computes reward as a function of the precision and priority.
        For prec, prio in [0,1], computes prec * prio.
        """

        return prec * prio

    def quantize(self, reward, delta):
        """
        Gives the quantized reward for reward and delta.
        """
        return int(math.floor(reward / delta))

    def printSP(self):
        """ 
        A scrappy function for printing the S and P tables for debugging.

        S   S[i][r] is the solution to S(i,r) as defined by Yao et al
        P   P[i][r] is the solution to P(i,r) as defined by Yao et al
        """
        # Assume S and P are correct since they are generated internally.
        S = self.S
        P = self.P
        print("\nS:")
        for i in range(len(S)):
            if S[i] == POS_INF:
                s = 'INF'
            else:
                s = str(S[i])
            print(str(i)+": "+s+"  ")
        print("P:")
        for i in range(len(P)):
            if P[i] == POS_INF:
                s = 'INF'
            else:
                s = str(P[i])
            print(str(i)+": "+s+"  ")
        print("\n")
