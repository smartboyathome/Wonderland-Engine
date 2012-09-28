import unittest
from configobj import ConfigObj
import redis
from DBWrappers.MongoDBWrapper import MongoDBWrapper
from ScoringDaemon.checker_process import CheckerProcess
from ScoringDaemon.checks.SampleChecks import SampleServiceCheck, SampleInjectCheck
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
        db_host = config['DATABASE']['HOST']
        db_port = config['DATABASE']['PORT']
        db_name = config['DATABASE']['DB_NAME']
        self.init_db_data(db_host, db_port, db_name)
        self.db_wrapper = MongoDBWrapper(db_host, int(db_port), db_name)
        service_check_data = [obj for obj in self.data['active_checks'] if obj['class_name'] == 'SampleServiceCheck']
        service_check_id = service_check_data[0]['id']
        inject_check_id = [obj for obj in self.data['active_checks'] if obj['class_name'] == 'SampleInjectCheck'][0]['id']
        self.checkers = [
            ActiveCheck(service_check_id, SampleServiceCheck),
            ActiveCheck(inject_check_id, SampleInjectCheck)
        ]
        self.team = '6'
        self.process = CheckerProcess(self.team, self.checkers, db_host, int(db_port), db_name, config['DAEMON']['CHECK_DELAY'])

    def tearDown(self):
        if self.process.is_alive():
            self.process.shutdown_event.set()
            self.process.join(5)
            self.process.terminate()
        self.drop_db_data()