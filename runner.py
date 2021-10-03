import threading
from gpu import GPU


class Runner:
    """Class and methods for how we actually run tasks and send to GPU"""
    def __init__(self):
        self.gpu = GPU()

    def run_tasks(self, scheduler):
        """forever run the tasks, call the scheduler API"""
        while True:
            while scheduler.get_task_list_length() > 0:
                curr_task = scheduler.get_next_task()
                # Send task to GPU for execution
                self.gpu.run_task(curr_task)

    def start_runner(self, scheduler):
        """Create a new thread and run all the tasks"""
        tid = threading.Thread(target=self.run_tasks, args=(scheduler,))
        tid.start()
