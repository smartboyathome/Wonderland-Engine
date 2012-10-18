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

import time
from tests.DaemonTests import MasterTestCase

class TestMaster(MasterTestCase):
    pass
    '''def test_team_count(self):
        assert len(self.master.checkers) == 3

    def test_start_team_processes(self):
        self.master.run_command('start')
        for team_id in self.master.checkers:
            assert self.master.checkers[team_id].process.is_alive()

    def test_stop_team_processes(self):
        self.master.run_command('start')
        self.master.run_command('stop')
        for team_id in self.master.checkers:
            self.master.checkers[team_id].process.join(5)
            assert not self.master.checkers[team_id].process.is_alive()

    def test_default_team_processes_stopped(self):
        for team_id in self.master.checkers:
            assert not self.master.checkers[team_id].process.is_alive()

    def test_shutdown_signal_emitted(self):
        with self.assertRaises(SystemExit):
            self.master.run_command('shutdown')

    def test_check_scores(self):
        self.master.run_command('start')
        time.sleep(5)
        scores = self.db_wrapper.get_scores_for_all_teams()
        \'''for team in scores:
            assert scores[team] == 5'''