"""
Implementing the algorithm presented in 
"Scheduling Real-time Deep Learning Services as Imprecise Computations"
by Yao et al.

2021 - Oliver Broadrick - odbroadrick@gmail.com
"""
# Quick function for printing the alg's tables in a decently readable manner
def printSP(S, P):
    print("\n")
    for i in range(len(S)):
        print(str(i)+": "+str(S[i])+"  ")
    for i in range(len(P)):
        print(str(i)+": "+str(P[i])+"  ")
    print("\n")

import numpy as np
import math

#POS_INF = 10**10
#NEG_INF = -POS_INF
POS_INF = 'INF' #for printing porpoises

# delta is the basic increment of reward
delta = 1

# N is the number of tasks
N = 3

# L[i] is the number of stages for task i
L = [5,3,4]

# T[i][l] is the runtime for the first l stages of task i (cumulative)
T = [[2,3,5,7,9], [3,4,7], [1,9,9,12]]

# R[i][l] is the reward for completing the first l stages of task i before the deadline
R = [[12,15,16,17,17], [2,6,6], [3,3,4,6]]

# D[i] is the deadline for task i 
# (we assume we begin running at time 0, so D[i] is the maximum permissable runtime before task i must have been run)
# Note that these are weakly increasing as per requirement of the algorithm
D = [18, 19, 23]

# Rmax is the maximum possible reward for a single task
Rmax = max(max(R[i]) for i in range(len(R)))

# S[i][r] is the depth to which task i should be computed to optimally achieve exactly reward r*delta
S = [[None for r in range(N*math.floor(Rmax/delta))] for i in range(N)]

# P[i][r] is the time required to carry out the schedule implied by S[i][r]
P = [[POS_INF for r in range(N*math.floor(Rmax/delta))] for i in range(N)]

# Algorithm to schedule for these parameters begins!
# Start with task 1 on its own
i = 0
for r in range(0, N*math.floor(Rmax/delta)): # for each level of reward
    # We need to find the depth which achieves reward r in minimum time
    # winning_l is that depth
    winning_l = None
    # winning_t is the corresponding worst-case runtime
    winning_t = POS_INF
    for l in range(L[i]):
        # If this depth achieves reward r
        if R[i][l] == r:
            # If this is the first such task, it is the current winner
            if winning_l is None:
                winning_l = l
                winning_t = T[i][l]
            # If the time to achieve this depth does so in less time than the current winner
            elif T[i][l] < T[i][l]:
                winning_l = l
                winning_t = T[i][l]
    # Update this cell in S and P as long as the winning time abides by the task's deadline
    if winning_l is not None and winning_t <= D[i]:
        S[i][r] = winning_l
        P[i][r] = winning_t

# Sanity check
#printSP(S,P)

# Now for subsequent tasks we apply the same operations
for i in range(1, N):
    for r in range(0, N*math.floor(Rmax/delta)): # for each level of reward
        # We need to find the depth which achieves reward r in minimum time
        # winning_l is that depth
        winning_l = None
        # winning_t is the corresponding worst-case runtime
        winning_t = POS_INF
        # For each possible optimal depth, l
        for l in range(L[i]):
            # If this depth achieves reward r on its own
            if R[i][l] == r:
                # If this is the first sufficient depth, it is the current winner
                if winning_l is None:
                    winning_l = l
                    winning_t = T[i][l]
                # If the time to achieve this depth does so in less time than the current winner
                elif T[i][l] < winning_t:
                    winning_l = l
                    winning_t = T[i][l]
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
                        winning_t = T[i][l] + P[i-1][r_]
                    # If the time to achieve this depth does so in less time than the current winner
                    elif T[i][l] + P[i-1][r_] < winning_t:
                        winning_l = l
                        winning_t = T[i][l] + P[i-1][r_]
     
        # Update this cell in S and P as long as the winning time is less than the deadline for this task
        if winning_l is not None and winning_t <= D[i]:
            S[i][r] = winning_l
            P[i][r] = winning_t

# Sanity check
printSP(S,P)

# Now that the tables are completed, we find the optimal path using the tables
# First we need to answer the following question about the last (latest deadline) task:
# which depth/layer achieves the highest reward with runtime sufficient to meet the deadline?

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
    print("No schedule for you... give nicer inputs"+"  ")
else:
    # Now we construct the optimal schedule
    l_cur = l_max
    # r_ is the remaining reward
    r_ = r_max - R[N-1][l_max]
    depth_sched = [l_cur]
    reward_sched = [R[N-1][l_max]]
    time_sched = [T[N-1][l_max]]
    for i in range(N-2, -1, -1):
        l_cur = S[i][r_]
        r_ = r_ - R[i][l_cur]
        depth_sched.insert(0, l_cur)
        reward_sched.insert(0, R[i][l_cur])
        time_sched.insert(0, T[i][l_cur])

# Print out the solution schedule that was found
print("Schedule that achieves reward", r_max, "  ")
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










