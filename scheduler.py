import time

class Scheduler:
    def __init__(self):
        self.tasks = []

    def run_tasks(self):
        while True:
            for task in self.tasks:
                do_work(task)

    def add_task(self, task):
        self.tasks.append(task)


def do_work(task):
    print(task)
    time.sleep(5)
