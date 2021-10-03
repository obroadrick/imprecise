class Task:
    """Class and methods for how a task is handled"""
    def __init__(self, stages, priority, deadline, name):
        self.stages = stages
        self.priority = priority
        self.deadline = deadline
        self.name = name
        self.level = 2

    def set_optimal_level(self, level):
        """Method for setting optimal level made by the scheduler"""
        self.level = level
