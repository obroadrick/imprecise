import os
from scheduler import Scheduler
from task import Task
from stage import Stage
from flask import Flask
from runner import Runner

app = Flask(__name__)

scheduler = Scheduler()
runner = Runner()

def create_new_task(job, deadline):
    stage_files_list = os.listdir("tasks/" + "task" + job)
    stage_files_list.sort()
    stage_list = []
    for stage_file in stage_files_list:
        stage = Stage(stage_file, 0, 0, 0)
        stage_list.append(stage)

    task = Task(stage_list, 0, deadline, "task"+job)
    return task

@app.route("/<job>,<deadline>")
def home(job, deadline):
    """ Function for test purposes. """
    task = create_new_task(job, deadline)
    scheduler.add_task(task)
    return "Adding job" + str(job) + "deadline" + str(deadline)


if __name__ == "__main__":
    scheduler.start_scheduler(1)
    runner.start_runner(scheduler)
    app.run()
