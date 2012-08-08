from threading import Thread
from ScoringDaemon.checker_process import CheckerProcess

class TeamController(Thread):
    def __init__(self, team):
        super(Thread, self).__init__()
        self.team_process = CheckerProcess([])