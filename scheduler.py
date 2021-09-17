import time

class Scheduler:
    def __init__(self):
        self.tasks = []

    def run_tasks(self):
        while True:
            for task in self.tasks:
                do_work(task)

    def add_task(self, task):
        print(self.tasks)
        self.tasks.append(task)
        print(self.tasks)


def do_work(task):
    time.sleep(2)
