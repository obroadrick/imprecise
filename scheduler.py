from apscheduler.schedulers.background import BackgroundScheduler
class Scheduler:
    def __init__(self):
        self.task_q = [] # Que of tasks input by the server
        self.run_arr = [] # tasks to be run by the server
        self.task_reward_table = [] # Table of task/rewards
    def schedule_table(self):
        """Schedule the table based on the dynamic programming algo"""
        """Will also need to add tasks the the run_arr"""
        if len(self.task_q) > 0:
            self.run_arr.append(self.task_q.pop(-1))

        #TODO
    def start_scheduler(self, time_seconds):
        """Server calls this to start the scheduler"""
        sched = BackgroundScheduler(daemon=True)
        sched.add_job(self.schedule_table,'interval', seconds = time_seconds)
        sched.start()

    def add_task(self, task):
        """Sever will call this to add a task to the task_q which will later be scheduled"""
        self.task_q.append(task)

    def get_next_task(self):
        """Runner will call this to get the next task"""
        return self.run_arr.pop(-1)

    def get_task_list_length(self):
        """Runner will call this to make sure the list is not empty"""
        return len(self.run_arr)
