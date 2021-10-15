import csv
import numpy
# import time
from numba import cuda

# @cuda.reduce
# def sum_reduce(a, b):
#     return a + b

# start_time = time.time()
# while(True):
#     got = sum_reduce(A)   # cuda sum reduction
# print("GPU", time.time() - start_time)
# print(got)


@cuda.reduce
def sum_reduce(a, b):
    return a + b

num = 0

class GPU:
    """Methods to describe how we will tasks will be ran by the GPU"""
    def run_task(self, task):
        ans = 0
        global num
        for i in range(task.level):
            # print("GPU running task at level", i)
            workload_arr = self.workload_to_arr("tasks/" + str(task.name) + "/stage" + str(i))
            ans += self.do_work(workload_arr)
        ans = ans / task.level
        num = num + 1
        # reward_sum = task.reward
        print(num)
        # print("Final answer to task: ", ans)

    def workload_to_arr(self, stagedir):
        return numpy.genfromtxt(stagedir, delimiter=',', dtype = numpy.float64)


    def do_work(self, workload):
        work_sum = 0
        work_sum = work_sum + sum_reduce(workload)
        return work_sum / len(workload)
