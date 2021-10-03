import csv
class GPU:
    """Methods to describe how we will tasks will be ran by the GPU"""
    def run_task(self, task):
        ans = 0
        for i in range(task.level):
            print("GPU running task at level", i)
            workload_arr = self.workload_to_arr("tasks/" + str(task.name) + "/stage" + str(i))
            ans += self.do_work(workload_arr)
        ans = ans / task.level
        print("Final answer to task: ", ans)

    def workload_to_arr(self, stagedir):
        print(stagedir)
        return list(csv.reader(open(stagedir)))

    def do_work(self, workload):
        work_sum = 0
        for i in range(len(workload)):
            for j in range(len(workload[i])):
                work_sum = work_sum + int(workload[i][j])
        return work_sum / (len(workload) * len(workload[0]))
