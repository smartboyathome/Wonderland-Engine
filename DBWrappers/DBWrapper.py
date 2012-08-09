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

import abc

@abc.ABCMeta
class DBWrapper(object):

    @abc.abstractmethod
    def close(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_all_teams(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_specific_team(self, team_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def create_team(self, team_name, team_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def modify_team(self, team_id, **data):
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_team(self, team_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_team_config_for_all_machines(self, team_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_team_config_for_machine(self, team_id, machine_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def create_team_config_for_machine(self, team_id, machine_id, username, password, port):
        raise NotImplementedError()

    @abc.abstractmethod
    def modify_team_config_for_machine(self, team_id, machine_id, **data):
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_team_config_for_machine(self, team_id, machine_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_all_machines(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_specific_machine(self, machine_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def create_machine(self, machine_id, general_ip):
        raise NotImplementedError()

    @abc.abstractmethod
    def modify_machine(self, machine_id, **data):
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_machine(self, machine_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_all_users(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_specific_user(self, username, password_hash=None):
        raise NotImplementedError()

    @abc.abstractmethod
    def create_user(self, username, password_hash, email, role, **extra_info):
        raise NotImplementedError()

    @abc.abstractmethod
    def modify_user(self, username, **data):
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_user(self, username):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_current_scoring_session(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def start_current_scoring_session(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def stop_current_scoring_session(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def clear_current_scoring_session(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_all_archived_scoring_sessions(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_specific_archived_scoring_session(self, archive_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def archive_current_scoring_session(self, archive_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def clear_current_scoring_session(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_attacker_check(self, check_id, team_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_all_check_classes(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_specific_check_class(self, class_name):
        raise NotImplementedError()

    @abc.abstractmethod
    def create_check_class(self, class_name, check_type, module_name):
        raise NotImplementedError()

    @abc.abstractmethod
    def modify_check_class(self, class_name, **data):
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_check_class(self, class_name):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_all_check_scripts(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_specific_check_script(self, module_name):
        raise NotImplementedError()

    @abc.abstractmethod
    def create_check_script(self, module_name, path):
        raise NotImplementedError()

    @abc.abstractmethod
    def modify_check_script(self, module_name, **data):
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_check_script(self, module_name):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_all_checks(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_all_service_checks(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_specific_service_check(self, check_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def create_service_check(self, check_id, description, machine, check_class):
        raise NotImplementedError()

    @abc.abstractmethod
    def modify_service_check(self, check_id, **data):
        raise NotImplementedError()

    @abc.abstractmethod
    def complete_service_check(self, check_id, team_id, timestamp, score):
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_service_check(self, check_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_all_inject_checks(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_specific_inject_check(self, check_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def create_inject_check(self, check_id, description, machine, check_class, inject_number, time_to_check):
        raise NotImplementedError()

    @abc.abstractmethod
    def modify_inject_check(self, check_id, **data):
        raise NotImplementedError()

    @abc.abstractmethod
    def complete_inject_check(self, check_id, team_id, timestamp, score):
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_inject_check(self, check_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_all_manual_checks(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_specific_manual_check(self, check_id, team_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def create_manual_check(self, check_id, description, comments, inject_number, team_id, points_awarded):
        raise NotImplementedError()

    @abc.abstractmethod
    def modify_manual_check(self, check_id, team_id, **data):
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_manual_check(self, check_id, team_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_all_attacker_checks(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_specific_attacker_check(self, check_id, team_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def create_attacker_check(self, check_id, description, comments, machine, team_id, check_class):
        raise NotImplementedError()

    @abc.abstractmethod
    def modify_attacker_check(self, check_id, team_id, **data):
        raise NotImplementedError()

    @abc.abstractmethod
    def complete_attacker_check(self, check_id, team_id, timestamp, score):
        raise NotImplementedError()

    @abc.abstractmethod
    def delete_attacker_check(self, check_id, team_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_all_completed_checks(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_all_completed_service_checks(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_all_completed_inject_checks(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_all_completed_manual_checks(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_all_completed_attacker_checks(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_all_completed_checks_for_team(self, team_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_all_completed_service_checks_for_team(self, team_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_all_completed_inject_checks_for_team(self, team_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_all_completed_manual_checks_for_team(self, team_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_all_completed_attacker_checks_for_team(self, team_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_specific_completed_service_check_for_team(self, check_id, team_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_specific_completed_inject_check_for_team(self, check_id, team_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_specific_completed_manual_check_for_team(self, check_id, team_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_specific_completed_attacker_check_for_team(self, check_id, team_id):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_specific_completed_service_check_for_team_at_time(self, check_id, team_id, timestamp):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_specific_completed_attacker_check_for_team_at_time(self, check_id, team_id, timestamp):
        raise NotImplementedError()