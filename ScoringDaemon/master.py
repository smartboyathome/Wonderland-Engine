from multiprocessing import Queue
from configobj import ConfigObj
import os, redis, inspect
from validate import Validator
from DBWrappers.MongoDBWrapper import MongoDBWrapper
from ScoringDaemon.check_types import Check
from ScoringDaemon.checker_process import CheckerProcess
from ScoringServer.utils import load_plugins

class Master(object):
    def __init__(self, _config_file=os.path.join(os.getcwd(), 'settings.cfg')):
        configspec = ConfigObj(os.path.join(os.getcwd(), 'configspec.cfg'), list_values=False)
        self.config = ConfigObj(_config_file, configspec=configspec)['CORE']
        self.checkers = {}
        self.redis = redis.Redis(self.config['REDIS']['HOST'], self.config['REDIS']['PORT'], password=self.config['REDIS']['PASSWORD'])
        self.pubsub = self.redis.pubsub()
        self.channel = self.config['REDIS']['DB_CHANNEL']
        self.check_scripts = []
        self.check_classes = []
        self.active_checks = []
        self.reload_check_classes()

    def run(self):
        self.pubsub.subscribe(self.channel)
        for message in self.pubsub.listen():
            print "server recieving message:", message['data']
            command = message['data'].split(' ')
            if command[0] == 'changed' and len(command) == 2:
                self.changed(command[1])

    def changed(self, arg):
        if arg == 'checks':
            self.reload_check_classes()
            for team_id in self.checkers:
                pass
        if arg in self.checkers:
            pass

    def reload_check_classes(self):
        del self.check_classes[:]
        del self.check_scripts[:]
        check_modules = load_plugins(os.path.join(os.path.dirname(__file__), 'checks'))
        for check_name in check_modules:
            check = check_modules[check_name]
            classes = inspect.getmembers(check, inspect.isclass)
            for _class in classes:
                if issubclass(_class, Check):
                    if check_name not in self.check_scripts:
                        self.check_scripts.append(check_name)
                    self.check_classes.append(_class)
        db = MongoDBWrapper(self.config['DATABASE']['HOST'], self.config['DATABASE']['PORT'], self.config['DATABASE']['DB_NAME'])


    def reload_active_checks(self):
        pass

class CheckerManager(object):
    def __init__(self, team_id, checks, db_host, db_port, db_name):
        self.command_queue = Queue()
        self.process = CheckerProcess(team_id, checks, db_host, db_port, db_name)
        self.process.start()
    def changed(self):
        self.command_queue.put('quit')
        self.process = CheckerProcess()
        self.process.start()