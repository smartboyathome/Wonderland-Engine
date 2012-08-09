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

class BaseDBException(BaseException):
    pass

class DoesNotExist(BaseDBException):
    pass

class TeamDoesNotExist(BaseDBException):
    def __init__(self, team_id, *args, **kwargs):
        super(TeamDoesNotExist, self).__init__(*args, **kwargs)
        self.team_id = team_id
    def __str__(self):
        return "A team with ID {} does not exist.".format(self.team_id)

class TeamExists(BaseDBException):
    def __init__(self, team_id, *args, **kwargs):
        super(TeamExists, self).__init__(*args, **kwargs)
        self.team_id = team_id
    def __str__(self):
        return "A team with ID {} already exists.".format(self.team_id)

class MachineDoesNotExist(BaseDBException):
    def __init__(self, machine_id, *args, **kwargs):
        super(MachineDoesNotExist, self).__init__(*args, **kwargs)
        self.machine_id = machine_id
    def __str__(self):
        return "A machine with ID {} does not exist.".format(self.machine_id)

class MachineExists(BaseDBException):
    def __init__(self, machine_id, *args, **kwargs):
        super(MachineExists, self).__init__(*args, **kwargs)
        self.machine_id = machine_id
    def __str__(self):
        return "A machine with ID {} already exists.".format(self.machine_id)

class CheckClassDoesNotExist(BaseDBException):
    def __init__(self, check_class, check_type, *args, **kwargs):
        super(CheckClassDoesNotExist, self).__init__(*args, **kwargs)
        self.check_class = check_class
        self.check_type = check_type
    def __str__(self):
        return "A check class with id '{}' and type '{}' does not exist.".format(self.check_class, self.check_type)

class CheckClassExists(BaseDBException):
    def __init__(self, check_class, check_type, *args, **kwargs):
        super(CheckClassExists, self).__init__(*args, **kwargs)
        self.check_class = check_class
        self.check_type = check_type
    def __str__(self):
        return "A check class with id '{}' and type '{}' already exists.".format(self.check_class, self.check_type)

class CheckDoesNotExist(BaseDBException):
    def __init__(self, check_id, check_type, *args, **kwargs):
        super(CheckDoesNotExist, self).__init__(*args, **kwargs)
        self.check_id = check_id
        self.check_type = check_type
    def __str__(self):
        return "A check of type '{}' with id '{}' does not exist.".format(self.check_type, self.check_id)

class CheckExists(BaseDBException):
    def __init__(self, check_id, check_type, *args, **kwargs):
        super(CheckExists, self).__init__(*args, **kwargs)
        self.check_id = check_id
        self.check_type = check_type
    def __str__(self):
        return "A check of type '{}' with id '{}' already exists.".format(self.check_type, self.check_id)

class ArchivedSessionExists(BaseDBException):
    def __init__(self, archive_id):
        self.archive_id = archive_id
    def __str__(self):
        return "An archived session with id '{}' already exists.".format(self.archive_id)

class Exists(BaseDBException):
    def __init__(self, msg, *args, **kwargs):
        super(Exists, self).__init__(*args, **kwargs)
        self.msg = msg
    def __str__(self):
        return self.msg

class ScoringServerRunning(BaseDBException):
    def __str__(self):
        return "Cannot perform this action when the server is running."