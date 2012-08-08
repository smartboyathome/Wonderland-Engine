from multiprocessing import Process
from DBWrappers.MongoDBWrapper import MongoDBWrapper

class CheckerProcess(Process):
    def __init__(self, team_id, checks, db_host, db_port, db_name):
        self.team_id = team_id
        self.checks = checks
        self.db_host, self.db_port, self.db_name = db_host, db_port, db_name
    def run(self, queue):
        db = MongoDBWrapper(self.db_host, self.db_port, self.db_name)
        team = db.get_specific_team(self.team_id)

        for command in queue:
            if command == 'quit':
                db.close()
                return