import csv
class gpu:
    """Methods to describe how we will tasks will be ran by the GPU"""
    def run_task(self, task):
        ans = 0
        for i in range(task.level):
            print("GPU running task at level", i)
            workload_arr = self.workload_to_arr(task.stages[i].workload)
            ans += self.do_work(workload_arr)
        ans = ans / task.level
        print("Final answer to task: ", ans)

    def workload_to_arr(self, stage):
        return list(csv.reader(open(stage)))

    def do_work(self, workload):
        work_sum = 0
        for i in workload:
            for j in workload[i]:
                work_sum = work_sum + workload[i][j]
        return sum / (len(workload) * len(workload[0]))
