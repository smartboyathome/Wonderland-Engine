'''
    Copyright (c) 2012 Alexander Abbott

    This file is part of the Cheshire Cyber Defense Scoring Engine (henceforth
    referred to as Cheshire).

    Cheshire is free software: you can redistribute it and/or modify it under
    the terms of the GNU Affero General Public License as published by the
    Free Software Foundation, either version 3 of the License, or (at your
    option) any later version.

    Cheshire is distributed in the hope that it will be useful, but WITHOUT ANY
    WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
    FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for
    more details.

    You should have received a copy of the GNU Affero General Public License
    along with Cheshire.  If not, see <http://www.gnu.org/licenses/>.
'''
from configobj import ConfigObj
import os, redis, inspect
from parcon import alphanum_word, Regex, ZeroOrMore, flatten, Optional
from Doorknob.MongoDBWrapper import MongoDBWrapper
from WhiteRabbit.check_types import Check
from WhiteRabbit.checker_process import CheckerProcess
from WonderlandUtils import load_plugins, get_root_dir, get_first_file_that_exists, FileNotFound

default_config_dirs = [
    os.path.join(get_root_dir(), "etc", "wonderland-engine")
]

class Master(object):
    def __init__(self, _config_dir=None, _config_filename='settings.cfg', _configspec_filename='configspec.cfg'):
        if _config_dir is not None:
            default_config_dirs.insert(0, _config_dir)

        configspec_path = get_first_file_that_exists(default_config_dirs, _configspec_filename)
        config_path = get_first_file_that_exists(default_config_dirs, _config_filename)
        if configspec_path is None:
            raise FileNotFound('configspec', default_config_dirs, _configspec_filename)
        if config_path is None:
            raise FileNotFound('config', default_config_dirs, _config_filename)
        configspec = ConfigObj(configspec_path, list_values=False)
        self.config = ConfigObj(config_path, configspec=configspec)['CORE']

        self.db = MongoDBWrapper(self.config['DATABASE']['HOST'], int(self.config['DATABASE']['PORT']),
            self.config['DATABASE']['DB_NAME'])
        self.checkers = {}
        self.redis = redis.Redis(self.config['REDIS']['HOST'], int(self.config['REDIS']['PORT']),
            password=self.config['REDIS']['PASSWORD'])
        self.pubsub = self.redis.pubsub()
        self.channel = self.config['REDIS']['DAEMON_CHANNEL']
        self._command_parser = (alphanum_word + Optional(Regex('[\w\d_]+') + ZeroOrMore(Regex('[\w\d_.,:]+'))))[flatten]
        self.commands = {
            'changed': self.changed,
            'start': self.start,
            'stop': self.stop,
            'shutdown': self.shutdown
        }

        self.check_scripts = {}
        self.check_classes = {}
        self.active_checks = []
        self.reload_check_classes()
        self.reload_active_checks()
        self.reload_checkers()

    def run(self):
        self.pubsub.subscribe(self.channel)
        for message in self.pubsub.listen():
            self.run_command(message['data'])

    def run_command(self, message):
        try:
            print "server recieving message '{}' of type '{}'".format(message, type(message).__name__)
            if not issubclass(type(message), basestring):
                message = str(message)
            command_list = self._command_parser.parse_string(message)
            command = command_list.pop(0).lower()
            if command in self.commands:
                print "Running command '{}' with arguments '{}'".format(command, ', '.join(command_list))
                self.commands[command](*command_list)
        except BaseException, e:
            # This is to make sure that we clean up all shutdown processes before we error out.
            self.stop()
            raise

    def changed(self, subcommand, *args):
        if subcommand == 'all':
            self.reload_check_classes()
            self.reload_active_checks()
            self.reload_checkers()
        elif subcommand == 'team':
            try:
                self.reload_check_classes()
                self.reload_specific_checker(args[0])
            except IndexError:
                pass


    def start(self):
        for team_id in self.checkers:
            self.checkers[team_id].start()

    def stop(self):
        for team_id in self.checkers:
            self.checkers[team_id].shutdown()

    def shutdown(self):
        raise SystemExit

    def reload_check_classes(self):
        self.check_classes.clear()
        self.check_scripts.clear()
        check_modules = load_plugins(os.path.join(os.path.dirname(__file__), 'checks'))
        for check_name in check_modules:
            check = check_modules[check_name]
            classes = inspect.getmembers(check, lambda _class: inspect.isclass(_class) and issubclass(_class, Check))
            for check_class_name, check_class in classes:
                if check_name not in self.check_scripts:
                    self.check_scripts[check_name] = check
                    if len(self.db.get_specific_check_script(check_name)) == 0:
                        self.db.create_check_script(check_name, check.__file__)
                self.check_classes[check_class_name] = check_class
                if len(self.db.get_specific_check_class(check_class_name)) == 0:
                    self.db.create_check_class(check_class.__name__, check_class.check_type, check_name)

    def reload_active_checks(self):
        del self.active_checks[:]
        active_checks = self.db.get_all_checks()
        for check in active_checks:
            if check['class_name'] not in self.check_classes:
                self.db.delete_specific_check(check['id'], check['type'])
            else:
                self.active_checks.append(ActiveCheck(check['id'], self.check_classes[check['class_name']]))

    def reload_checkers(self):
        self.checkers.clear()
        teams = self.db.get_all_teams()
        for team in teams:
            self.reload_specific_checker(team['id'])

    def reload_specific_checker(self, team_id):
        if team_id in self.checkers:
            self.checkers[team_id].shutdown()
        team_checks = []
        for check in self.db.get_all_attacker_checks_for_team(team_id):
            if check['class_name'] in self.check_classes:
                team_checks.append({
                    'id': check['id'],
                    'class': self.check_classes[check['class_name']]
                })
        self.checkers[team_id] = CheckerManager(team_id, self.active_checks + team_checks,
                                                self.config['DATABASE']['HOST'], int(self.config['DATABASE']['PORT']),
                                                self.config['DATABASE']['DB_NAME'], self.config['DAEMON']['CHECK_DELAY'])

class CheckerManager(object):
    def __init__(self, team_id, checks, db_host, db_port, db_name, check_delay):
        self.team_id = team_id
        self.db_host, self.db_port, self.db_name = db_host, db_port, db_name
        self.check_delay = check_delay
        self.process = CheckerProcess(team_id, checks, db_host, db_port, db_name, check_delay)
    def restart(self, checks):
        self.shutdown()
        self.process = CheckerProcess(self.team_id, checks, self.db_host, self.db_port, self.db_name, self.check_delay)
        self.process.start()
    def shutdown(self):
        self.process.shutdown_event.set()
    def start(self):
        self.process.start()

class ActiveCheck(object):
    def __init__(self, _id, _class):
        self.check_class = _class
        self.check_id = _id