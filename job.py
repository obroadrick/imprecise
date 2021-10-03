
class Task:
    """A Class that defines how a job runs"""
    stages = []
    def __init__(self, deadline):
        self.deadline = deadline

    def add_stage(self, stage):
        self.stages.append(stage)
