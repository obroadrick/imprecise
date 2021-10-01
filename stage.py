class Stage:
    """A class that defines a stage, which is part of a job"""
    def __init__(self, workload, mandatory, expected, worst_case):
        self.workload = workload
        self.mandatory = mandatory
        self.expected = expected
        self.worst_case = worst_case
        self.reward = 0

    def set_reward(self, reward):
        """Should be called by the scheduler"""
        self.reward = reward
