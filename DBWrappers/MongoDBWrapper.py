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

from copy import deepcopy
from datetime import datetime
import pymongo, time
from DBWrappers.DBWrapper import DBWrapper
from DBWrappers.Exceptions import MachineDoesNotExist, CheckClassDoesNotExist, DoesNotExist, TeamDoesNotExist, CheckDoesNotExist, Exists, ScoringServerRunning, ArchivedSessionExists

class MongoDBWrapper(DBWrapper):

    def __init__(self, host, port, db_name):
        connection = pymongo.Connection(host, port, safe=True)
        self.host = host
        self.port = port
        self.db_name = db_name
        self.db = connection[db_name]

    def __deepcopy__(self, memo):
        return MongoDBWrapper(self.host, self.port, self.db_name)

    def _modify_document(self, collection, query, exclude_fields=[], **data):
        excluded_fields = {}
        for field in exclude_fields:
            excluded_fields[field] = 0
        if exclude_fields == []:
            orig_data = list(self.db[collection].find(query))
        else:
            orig_data = list(self.db[collection].find(query, excluded_fields))
        if len(orig_data) == 0:
            raise DoesNotExist()
        new_data = deepcopy(orig_data[0])
        for key in data:
            if key in new_data and not key in ('_id', 'id'):
                new_data[key] = data[key]
            else:
                raise KeyError("{} is not a valid property for a team.".format(key))
        self.db[collection].update(orig_data[0], new_data)

    def _query_db(self, collection, query, exclude_fields=[]):
        '''
        Excludes the fields that are being queried for in the actual query.
        '''
        excluded_fields = {'_id': 0}
        for field in exclude_fields:
            excluded_fields[field] = 0
        for key in query:
            excluded_fields[key] = 0
        return self.db[collection].find(query, excluded_fields)

    def init_db(self):
        self.db.teams.ensure_index([('id', pymongo.ASCENDING)])
        self.db.team_configs.ensure_index([('team_id', pymongo.ASCENDING), ('machine_id', pymongo.ASCENDING)])
        self.db.team_scores.ensure_index([('team_id', pymongo.ASCENDING), ('timestamp', pymongo.ASCENDING)])
        self.db.completed_checks.ensure_index([('id', pymongo.ASCENDING), ('team_id', pymongo.ASCENDING), ('timestamp', pymongo.ASCENDING)])
        self.db.active_checks.ensure_index([('id', pymongo.ASCENDING)])
        self.db.check_scripts.ensure_index([('id', pymongo.ASCENDING)])
        self.db.check_classes.ensure_index([('id', pymongo.ASCENDING)])
        self.db.machines.ensure_index([('id', pymongo.ASCENDING)])
        self.db.users.ensure_index([('id', pymongo.ASCENDING)])
        self.db.archived_sessions.ensure_index([('id', pymongo.ASCENDING), ('session.start_time', pymongo.DESCENDING), ('session.end_time', pymongo.DESCENDING)])

    def close(self):
        self.db.connection.close()

    def _datetime_to_timestamp(self, datetime_obj):
        return time.mktime(datetime_obj.timetuple())

    def get_all_teams(self):
        return list(self._query_db('teams', {}))

    def get_specific_team(self, team_id):
        return list(self._query_db('teams', {'id': team_id}))

    def create_team(self, team_name, team_id):
        if not len(self.get_specific_team(team_id)) == 0:
            raise Exists("A team with id {} already exists.".format(team_id))
        data = {
            "name": team_name,
            "id": team_id
        }
        score_data = {
            'team_id': team_id,
            'score': 0,
            'timestamp': datetime.now()
        }
        self.db.teams.insert(data)
        self.db.team_scores.insert(score_data)

    def modify_team(self, team_id, **data):
        self._modify_document('teams', {'id': team_id}, **data)

    def delete_team(self, team_id):
        if len(self.get_specific_team(team_id)) == 0:
            raise DoesNotExist
        self.db.teams.remove({'id': team_id})

    def get_scores_for_all_teams(self):
        return list(self._query_db('team_scores', {}))

    def get_score_for_team(self, team_id):
        if len(self.get_specific_team(team_id)) == 0:
            raise DoesNotExist
        result = list(self._query_db('team_scores', {'team_id':team_id}))
        if len(result) == 0:
            self.calculate_scores_for_team(team_id)
            result = list(self._query_db('team_scores', {'team_id':team_id}))
        return result

    def calculate_scores_for_team(self, team_id):
        if len(self.get_specific_team(team_id)) == 0:
            raise DoesNotExist
        old_score = list(self.db.team_scores.find({'team_id': team_id}))
        if len(old_score) == 0:
            self.db.team_scores.insert({
                'team_id': team_id,
                'score': 0,
                'timestamp': datetime.now()
            })
            old_score = list(self.db.team_scores.find({'team_id': team_id}))
        old_score = old_score[0]
        new_score = deepcopy(old_score)
        new_score['score'] = 0
        completed_checks = self.get_all_completed_checks_for_team(team_id)
        for check in completed_checks:
            new_score['score'] += check['score']
        new_score['timestamp'] = datetime.now()
        self.db.team_scores.update(old_score, new_score)
        return new_score

    def get_all_machines(self):
        return list(self._query_db('machines', {}))

    def get_specific_machine(self, machine_id):
        return list(self._query_db('machines', {'id': machine_id}))

    def create_machine(self, machine_id, general_ip):
        if not len(self.get_specific_machine(machine_id)) == 0:
            raise Exists("A machine with id {} already exists.".format(machine_id))
        data = {
            "id": machine_id,
            "general_ip": general_ip
        }
        self.db.machines.insert(data)

    def modify_machine(self, machine_id, **data):
        self._modify_document('machines', {'id': machine_id}, **data)

    def delete_machine(self, machine_id):
        if len(self.get_specific_machine(machine_id)) == 0:
            raise DoesNotExist
        self.db.machines.remove({'id': machine_id})

    def get_all_team_configs_for_all_machines(self):
        return list(self._query_db('team_configs', {}))

    def get_team_config_for_all_machines(self, team_id):
        if len(self.get_specific_team(team_id)) == 0:
            raise TeamDoesNotExist(team_id)
        team_config = list(self._query_db('team_configs', {'team_id': team_id}))
        return team_config

    def get_team_config_for_machine(self, team_id, machine_id):
        if len(self.get_specific_team(team_id)) == 0:
            raise TeamDoesNotExist(team_id)
        if len(self.get_specific_machine(machine_id)) == 0:
            raise MachineDoesNotExist(machine_id)
        return list(self._query_db('team_configs',{'team_id': team_id, 'machine_id': machine_id}))

    def create_team_config_for_machine(self, team_id, machine_id, **machine_data):
        if len(self.get_specific_team(team_id)) == 0:
            raise TeamDoesNotExist(team_id)
        if len(self.get_specific_machine(machine_id)) == 0:
            raise MachineDoesNotExist(machine_id)
        if not len(self.get_team_config_for_machine(team_id, machine_id)) == 0:
            raise Exists("A config for team {}'s '{}' machine already exists.".format(team_id, machine_id))
        data = {
            'team_id': team_id,
            'machine_id': machine_id
        }
        data.update(machine_data)
        self.db.team_configs.insert(data)

    def modify_team_config_for_machine(self, team_id, machine_id, **data):
        if len(self.get_specific_team(team_id)) == 0:
            raise TeamDoesNotExist(team_id)
        if len(self.get_specific_machine(machine_id)) == 0:
            raise MachineDoesNotExist(machine_id)
        return self._modify_document('team_configs', {'team_id': team_id, 'machine_id': machine_id}, **data)

    def delete_team_config_for_machine(self, team_id, machine_id):
        if len(self.get_team_config_for_machine(team_id, machine_id)) == 0:
            raise DoesNotExist
        self.db.team_configs.remove('team_configs', {'team_id': team_id, 'machine_id': machine_id})

    def get_all_users(self):
        return list(self._query_db('users', {}, exclude_fields=['password']))

    def get_all_users_with_role(self, role):
        return list(self._query_db('users', {'role': role}, exclude_fields=['password']))

    def get_specific_user(self, username, password_hash=None):
        if password_hash is None:
            return list(self._query_db('users', {'id': username}, exclude_fields=['password']))
        else:
            return list(self._query_db('users', {'id': username, 'password': password_hash}))

    def create_user(self, username, password_hash, email, role, **extra_info):
        if role not in ('administrator', 'organizer', 'attacker', 'team'):
            raise TypeError('Role must be one of "administrator", "organizer", "attacker", or "team".')
        if role == 'team' and not 'team' in extra_info and not isinstance(extra_info['team'], basestring):
            raise TypeError("team must be either a string or a unicode string")
        if not len(self.get_specific_user(username)) == 0:
            raise Exists("A user with username {} already exists.".format(username))
        data = {
            'id': username,
            'password': password_hash,
            'email': email,
            'role': role
        }
        data.update(extra_info)
        self.db.users.insert(data)

    def modify_user(self, username, **data):
        self._modify_document('users', {'id': username}, **data)

    def delete_user(self, username):
        if len(self.get_specific_user(username)) == 0:
            raise DoesNotExist
        self.db.users.remove({'id': username})

    def get_all_check_classes(self):
        return list(self._query_db('check_classes', {}))

    def get_specific_check_class(self, class_name):
        return list(self._query_db('check_classes', {'id': class_name}))

    def create_check_class(self, class_name, check_type, module_name):
        if check_type not in ('service', 'inject', 'manual', 'attacker'):
            raise KeyError, "check_type must be one of service, inject, manual, attacker, not {}".format(check_type)
        if not len(self.get_specific_check_class(class_name)) == 0:
            raise Exists("A check class with id {} already exists.".format(class_name))
        data = {
            'id': class_name,
            'check_type': check_type,
            'module_id': module_name
        }
        self.db.check_classes.insert(data)

    def modify_check_class(self, class_name, **data):
        self._modify_document('check_classes', {'id': class_name}, **data)

    def delete_check_class(self, class_name):
        if len(self.get_specific_check_class(class_name)) == 0:
            raise DoesNotExist
        self.db.check_classes.remove({'id': class_name})

    def get_all_check_scripts(self):
        return list(self._query_db('check_scripts', {}))

    def get_specific_check_script(self, module_name):
        return list(self._query_db('check_scripts', {'id': module_name}))

    def create_check_script(self, module_name, path):
        if not len(self.get_specific_check_script(module_name)) == 0:
            raise Exists("A check script with id {} already exists.".format(module_name))
        data = {
            'id': module_name,
            'path': path
        }
        self.db.check_scripts.insert(data)

    def modify_check_script(self, module_name, **data):
        self._modify_document('check_scripts', {'id': module_name}, **data)

    def delete_check_script(self, module_name):
        if len(self.get_specific_check_script(module_name)) == 0:
            raise DoesNotExist
        self.db.check_scripts.remove({'id': module_name})

    def get_all_checks(self):
        return list(self._query_db('active_checks', {}))

    def get_specific_check(self, check_id, check_type):
        return list(self._query_db('active_checks', {'id': check_id, 'type': check_type}))

    def delete_specific_check(self, check_id, check_type):
        if len(self.get_specific_check(check_id, check_type)) == 0:
            raise DoesNotExist
        self.db.active_checks.remove({'id': check_id, 'type': check_type})

    def get_all_service_checks(self):
        return list(self._query_db('active_checks', {'type': 'service'}))

    def get_specific_service_check(self, check_id):
        return list(self._query_db('active_checks', {'id': check_id, 'type': 'service'}))

    def create_service_check(self, check_id, description, machine, check_class):
        if len(self.get_specific_machine(machine)) == 0:
            raise MachineDoesNotExist(machine)
        if not len(self.get_specific_service_check(check_id)) == 0:
            raise Exists("A check with id {} already exists.".format(check_id))
        _class = self.get_specific_check_class(check_class)
        if len(_class) == 0 or not _class[0]['check_type'] == 'service':
            raise CheckClassDoesNotExist(check_class, 'service')
        data = {
            "id": check_id,
            "description": description,
            "machine": machine,
            "type": 'service',
            "class_name": check_class
        }
        self.db.active_checks.insert(data)

    def modify_service_check(self, check_id, **data):
        self._modify_document('active_checks', {'id': check_id, 'type': 'service'}, **data)

    # todo Write a check for complete_service_check
    def complete_service_check(self, check_id, team_id, timestamp, score):
        if len(self.get_specific_team(team_id)) == 0:
            raise TeamDoesNotExist(team_id)
        service_check = self.get_specific_service_check(check_id)
        if len(service_check) == 0:
            raise CheckDoesNotExist(check_id, 'service')
        data = {
            "id": check_id,
            "description": service_check[0]['description'],
            "type": 'service',
            "timestamp": timestamp,
            "team_id": team_id,
            "score": score
        }
        self.db.completed_checks.insert(data)

    def delete_service_check(self, check_id):
        if len(self.get_specific_service_check(check_id)) == 0:
            raise DoesNotExist
        self.db.active_checks.remove({'id': check_id})

    def get_all_attacker_checks(self):
        return list(self._query_db('active_checks', {'type': 'attacker'}))

    def get_all_attacker_checks_for_team(self, team_id):
        return list(self._query_db('active_checks', {'team_id': team_id, 'type': 'attacker'}))

    def get_specific_attacker_check(self, check_id, team_id):
        return list(self._query_db('active_checks', {'id': check_id, 'team_id': team_id, 'type': 'attacker'}))

    def create_attacker_check(self, check_id, description, machine, team_id, check_class):
        if len(self.get_specific_machine(machine)) == 0:
            raise MachineDoesNotExist(machine)
        if len(self.get_specific_team(team_id)) == 0:
            raise TeamDoesNotExist(team_id)
        if not len(self.get_specific_attacker_check(check_id, team_id)) == 0:
            raise Exists("A check with id {} already exists.".format(check_id))
        _class = self.get_specific_check_class(check_class)
        if len(_class) == 0 or not _class[0]['check_type'] == 'attacker':
            raise CheckClassDoesNotExist(check_class, 'attacker')
        data = {
            "id": check_id,
            "description": description,
            "machine": machine,
            "type": 'attacker',
            "team_id": team_id,
            "class_name": check_class
        }
        self.db.active_checks.insert(data)

    def modify_attacker_check(self, check_id, team_id, **data):
        self._modify_document('active_checks', {'id': check_id, 'team_id': team_id, 'type': 'attacker'}, **data)

    # todo Write a check for complete_attacker_check
    def complete_attacker_check(self, check_id, team_id, timestamp, score):
        if len(self.get_specific_team(team_id)) == 0:
            raise TeamDoesNotExist(team_id)
        attacker_check = self.get_specific_attacker_check(check_id, team_id)
        if len(attacker_check) == 0:
            raise CheckDoesNotExist(check_id, 'attacker')
        data = {
            "id": check_id,
            "description": attacker_check[0]['description'],
            "comments": attacker_check[0]['comments'],
            "type": 'attacker',
            "timestamp": timestamp,
            "team_id": team_id,
            "score": score
        }
        self.db.completed_checks.insert(data)

    def delete_attacker_check(self, check_id, team_id):
        if len(self.get_specific_attacker_check(check_id, team_id)) == 0:
            raise DoesNotExist
        self.db.active_checks.remove({'id': check_id, 'team_id': team_id})

    def get_all_inject_checks(self):
        return list(self._query_db('active_checks', {'type': 'inject'}))

    def get_specific_inject_check(self, check_id):
        return list(self._query_db('active_checks', {'id': check_id, 'type': 'inject'}))

    def create_inject_check(self, check_id, description, machine, check_class, inject_number, time_to_check):
        if len(self.get_specific_machine(machine)) == 0:
            raise MachineDoesNotExist(machine)
        if not len(self.get_specific_inject_check(check_id)) == 0:
            raise Exists("A check with id {} already exists.".format(check_id))
        _class = self.get_specific_check_class(check_class)
        if len(_class) == 0 or not _class[0]['check_type'] == 'inject':
            raise CheckClassDoesNotExist(check_class, 'inject')
        data = {
            "id": check_id,
            "description": description,
            "machine": machine,
            "type": 'inject',
            "class_name": check_class,
            "inject_number": inject_number,
            "time_to_check":time_to_check
        }
        self.db.active_checks.insert(data)

    def modify_inject_check(self, check_id, **data):
        self._modify_document('active_checks', {'id': check_id, 'type': 'inject'}, **data)

    # todo Write a check for complete_inject_check
    def complete_inject_check(self, check_id, team_id, timestamp, score):
        if len(self.get_specific_team(team_id)) == 0:
            raise TeamDoesNotExist(team_id)
        inject_check = self.get_specific_inject_check(check_id)
        if len(inject_check) == 0:
            raise CheckDoesNotExist(check_id, 'inject')
        data = {
            "id": check_id,
            "description": inject_check[0]['description'],
            "type": 'inject',
            "inject_number": inject_check[0]['inject_number'],
            "time_to_check": inject_check[0]['time_to_check'],
            "timestamp": timestamp,
            "team_id": team_id,
            "score": score
        }
        self.db.completed_checks.insert(data)

    def delete_inject_check(self, check_id):
        if len(self.get_specific_inject_check(check_id)) == 0:
            raise DoesNotExist
        self.db.active_checks.remove({'id': check_id})

    def get_all_manual_checks(self):
        return list(self._query_db('completed_checks', {'type': 'manual'}))

    def get_specific_manual_check(self, check_id, team_id):
        return list(self._query_db('completed_checks', {'id': check_id, 'team_id': team_id, 'type': 'manual'}))

    def create_manual_check(self, check_id, description, comments, inject_number, team_id, points_awarded):
        if not len(self.get_specific_manual_check(check_id, team_id)) == 0:
            raise Exists("A check with id {} already exists.".format(check_id))
        data = {
            "id": check_id,
            "description": description,
            "comments": comments,
            "type": 'manual',
            "inject_number": inject_number,
            "team_id": team_id,
            "score": points_awarded
        }
        self.db.completed_checks.insert(data)

    def modify_manual_check(self, check_id, team_id, **data):
        self._modify_document('completed_checks', {'id': check_id, 'team_id': team_id, 'type': 'manual'}, **data)

    def delete_manual_check(self, check_id, team_id):
        if len(self.get_specific_manual_check(check_id, team_id)) == 0:
            raise DoesNotExist
        self.db.completed_checks.remove({'id': check_id, 'team_id': team_id})

    def get_all_completed_checks(self):
        return list(self._query_db('completed_checks', {}))

    def get_all_completed_service_checks(self):
        return list(self._query_db('completed_checks', {'type': 'service'}))

    def get_all_completed_attacker_checks(self):
        return list(self._query_db('completed_checks', {'type': 'attacker'}))

    def get_all_completed_inject_checks(self):
        return list(self._query_db('completed_checks', {'type': 'inject'}))

    def get_all_completed_manual_checks(self):
        return list(self._query_db('completed_checks', {'type': 'manual'}))

    def get_all_completed_checks_for_team(self, team_id):
        return list(self._query_db('completed_checks', {'team_id': team_id}))

    def get_all_completed_service_checks_for_team(self, team_id):
        if len(self.get_specific_team(team_id)) == 0:
            raise TeamDoesNotExist
        return list(self._query_db('completed_checks', {'team_id': team_id, 'type': 'service'}))

    def get_all_completed_attacker_checks_for_team(self, team_id):
        if len(self.get_specific_team(team_id)) == 0:
            raise TeamDoesNotExist
        return list(self._query_db('completed_checks', {'team_id': team_id, 'type': 'attacker'}))

    def get_all_completed_inject_checks_for_team(self, team_id):
        if len(self.get_specific_team(team_id)) == 0:
            raise TeamDoesNotExist
        return list(self._query_db('completed_checks', {'team_id': team_id, 'type': 'inject'}))

    def get_all_completed_manual_checks_for_team(self, team_id):
        if len(self.get_specific_team(team_id)) == 0:
            raise TeamDoesNotExist
        return list(self._query_db('completed_checks', {'team_id': team_id, 'type': 'manual'}))

    def get_all_completed_checks_for_team_since(self, team_id, timestamp):
        if len(self.get_specific_team(team_id)) == 0:
            raise TeamDoesNotExist
        return list(self._query_db('completed_checks', {'team_id': team_id, '$gt': {'timestamp': timestamp}}))

    def get_specific_completed_service_check_for_team(self, check_id, team_id):
        if len(self.get_specific_team(team_id)) == 0:
            raise TeamDoesNotExist
        return list(self._query_db('completed_checks', {'team_id': team_id, 'type': 'service', 'id': check_id}))

    def get_specific_completed_attacker_check_for_team(self, check_id, team_id):
        if len(self.get_specific_team(team_id)) == 0:
            raise TeamDoesNotExist
        return list(self._query_db('completed_checks', {'team_id': team_id, 'type': 'attacker', 'id': check_id}))

    def get_specific_completed_inject_check_for_team(self, check_id, team_id):
        if len(self.get_specific_team(team_id)) == 0:
            raise TeamDoesNotExist
        return list(self._query_db('completed_checks', {'team_id': team_id, 'type': 'inject', 'id': check_id}))

    def get_specific_completed_manual_check_for_team(self, check_id, team_id):
        if len(self.get_specific_team(team_id)) == 0:
            raise TeamDoesNotExist
        return list(self._query_db('completed_checks', {'team_id': team_id, 'type': 'manual', 'id': check_id}))

    def get_specific_completed_service_check_for_team_at_time(self, check_id, team_id, timestamp):
        if len(self.get_specific_team(team_id)) == 0:
            raise TeamDoesNotExist
        return list(self._query_db('completed_checks', {'team_id': team_id, 'type': 'service', 'id': check_id, 'timestamp': timestamp}))

    def get_specific_completed_attacker_check_for_team_at_time(self, check_id, team_id, timestamp):
        if len(self.get_specific_team(team_id)) == 0:
            raise TeamDoesNotExist
        return list(self._query_db('completed_checks', {'team_id': team_id, 'type': 'attacker', 'id': check_id, 'timestamp': timestamp}))

    # todo Write unit tests for scoring session functions
    def get_current_scoring_session(self):
        return list(self._query_db('session', {}))

    def start_current_scoring_session(self):
        old_session = list(self.db.session.find({}))
        session = {}
        if not len(old_session) == 0:
            session = old_session[0]
        if not 'state' in session or session['state'] == 'stopped':
            session['state'] = 'started'
        else:
            return
        if 'start_time' not in session:
            session['start_time'] = datetime.now()
        session['end_time'] = datetime(1,1,1)
        if '_id' in session:
            self.db.session.update(old_session[0], session)
        else:
            self.db.session.insert(session)

    def stop_current_scoring_session(self):
        old_session = list(self.db.session.find({}))
        if len(old_session) == 0:
            return
        session = deepcopy(old_session[0])
        session['end_time'] = datetime.now()
        session['state'] = 'stopped'
        self.db.session.update(old_session[0], session)

    def clear_current_scoring_session(self):
        session = list(self.db.session.find({}))
        if len(session) == 0:
            return
        self.db.session.remove(session)
        completed_checks = list(self.db.completed_checks.find({}))
        self.db.completed_checks.remove(completed_checks)

    # todo Write unit tests for archive scoring session functions
    def archive_current_scoring_session(self, archive_id):
        if not len(self.get_specific_archived_scoring_session(archive_id)) == 0:
            raise ArchivedSessionExists(archive_id)
        session_archive = {
            'id': archive_id,
            'session': self.get_current_scoring_session(),
            'teams': self.get_all_teams(),
            'team_configs': self.get_all_team_configs_for_all_machines(),
            'team_scores': self.get_scores_for_all_teams(),
            'completed_checks': self.get_all_completed_checks(),
            'active_checks': self.get_all_checks(),
            'check_scripts': self.get_all_check_scripts(),
            'check_classes': self.get_all_check_classes(),
            'machines': self.get_all_machines(),
            'users': self.get_all_users()
        }
        if not len(session_archive['session']) == 0 or not session_archive['session']['state'] == 'stopped':
            raise ScoringServerRunning
        self.db.archived_sessions.insert(session_archive)

    def get_all_archived_scoring_sessions(self):
        return list(self._query_db('archived_sessions', {}))

    def get_specific_archived_scoring_session(self, archive_id):
        return list(self._query_db('archived_sessions', {'id': archive_id}))