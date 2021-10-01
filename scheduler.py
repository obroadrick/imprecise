from apscheduler.schedulers.background import BackgroundScheduler
class Scheduler:
    def __init__(self):
        self.task_q = [] # Que of tasks input by the server
        self.run_arr = [] # tasks to be run by the server
        self.task_reward_table = [] # Table of task/rewards
    def schedule_table(self):
        """Schedule the table based on the dynamic programming algo"""
        print(self.task_q)
        #TODO
    def start_scheduler(self, time_seconds):
        sched = BackgroundScheduler(daemon=True)
        sched.add_job(self.schedule_table,'interval', seconds = time_seconds)
        sched.start()

    def add_task(self, task):
        self.task_q.append(task)

    def get_next_task(self):
        self.run_arr.pop(len(self.run_arr))
