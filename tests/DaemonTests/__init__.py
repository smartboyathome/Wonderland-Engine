import unittest
from configobj import ConfigObj
import redis
from DBWrappers.MongoDBWrapper import MongoDBWrapper
from ScoringDaemon.checker_process import CheckerProcess
from ScoringDaemon.checks.SampleChecks import SampleServiceCheck, SampleInjectCheck, SampleAttackerCheck
from ScoringDaemon.master import Master, ActiveCheck
from tests import DBTestCaseMixin, config_path

class MasterTestCase(unittest.TestCase, DBTestCaseMixin):
    def setUp(self):
        config = ConfigObj(config_path)['CORE']
        db_host = config['DATABASE']['HOST']
        db_port = config['DATABASE']['PORT']
        db_name = config['DATABASE']['DB_NAME']
        self.init_db_data(db_host, db_port, db_name)
        self.redis = redis.Redis(config['REDIS']['HOST'], int(config['REDIS']['PORT']), password=config['REDIS']['PASSWORD'])
        self.daemon_channel = config['REDIS']['DAEMON_CHANNEL']
        self.master = Master(config_path)
        self.db_wrapper = MongoDBWrapper(db_host, int(db_port), db_name)

    def tearDown(self):
        try:
            self.master.run_command('shutdown')
        except SystemExit:
            pass
        self.drop_db_data()

class CheckerProcessTestCase(unittest.TestCase, DBTestCaseMixin):
    def setUp(self):
        config = ConfigObj(config_path)['CORE']
        self.db_host = config['DATABASE']['HOST']
        self.db_port = config['DATABASE']['PORT']
        self.db_name = config['DATABASE']['DB_NAME']
        self.check_delay =  config['DAEMON']['CHECK_DELAY']
        self.init_db_data(self.db_host, self.db_port, self.db_name)
        self.db_wrapper = MongoDBWrapper(self.db_host, int(self.db_port), self.db_name)
        self.team = '6'

    def setup_process_with_no_checks(self):
        self.checkers = []
        self.process = CheckerProcess(self.team, self.checkers, self.db_host, int(self.db_port), self.db_name, self.check_delay)

    def setup_process_with_service_check(self):
        service_check = [obj for obj in self.data['active_checks'] if obj['class_name'] == 'SampleServiceCheck'][0]
        self.checkers = [
            ActiveCheck(service_check['id'], SampleServiceCheck)
        ]
        self.process = CheckerProcess(self.team, self.checkers, self.db_host, int(self.db_port), self.db_name, self.check_delay)

    def setup_process_with_inject_check(self):
        inject_check = [obj for obj in self.data['active_checks'] if obj['class_name'] == 'SampleInjectCheck'][0]
        self.checkers =[
            ActiveCheck(inject_check['id'], SampleInjectCheck)
        ]
        self.process = CheckerProcess(self.team, self.checkers, self.db_host, int(self.db_port), self.db_name, self.check_delay)

    def setup_process_with_attacker_check(self):
        attacker_check = [obj for obj in self.data['active_checks'] if obj['class_name'] == 'SampleAttackerCheck' and obj['team_id'] == self.team][0]
        self.checkers =[
            ActiveCheck(attacker_check['id'], SampleAttackerCheck)
        ]
        self.process = CheckerProcess(self.team, self.checkers, self.db_host, int(self.db_port), self.db_name, self.check_delay)

    def tearDown(self):
        if self.process.is_alive():
            self.process.shutdown_event.set()
            self.process.join(5)
            self.process.terminate()
        self.drop_db_data()