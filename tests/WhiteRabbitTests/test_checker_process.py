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
from tests.WhiteRabbitTests import CheckerProcessTestCase

class TestCheckerProcess(CheckerProcessTestCase):
    def test_checker_start(self):
        self.setup_process_with_no_checks()
        self.process.start()
        assert self.process.is_alive()

    def test_checker_stop(self):
        self.setup_process_with_no_checks()
        self.process.start()
        self.process.shutdown_event.set()
        self.process.join(5)
        assert not self.process.is_alive()

    def test_checker_service_score(self):
        self.setup_process_with_service_check()
        self.process.run_checks()
        stuff = self.db_wrapper.get_all_completed_checks_for_team(self.team)
        score = self.db_wrapper.get_score_for_team(self.team)
        assert score[0]['score'] == 20

    def test_checker_inject_score(self):
        self.setup_process_with_inject_check()
        self.process.run_checks()
        score = self.db_wrapper.get_score_for_team(self.team)
        print score[0]['score']
        assert score[0]['score'] == 0
        time.sleep(3)
        self.process.run_checks()
        score = self.db_wrapper.get_score_for_team(self.team)
        assert score[0]['score'] == 20

    def test_checker_attacker_score(self):
        self.setup_process_with_attacker_check()
        self.process.run_checks()
        score = self.db_wrapper.get_score_for_team(self.team)
        assert score[0]['score'] == 10

    def test_checker_all_types(self):
        self.setup_process_with_all_check_types()
        self.process.run_checks()
        score = self.db_wrapper.get_score_for_team(self.team)
        # score = 15 (orig) + 5 (SampleServiceCheck) + -5 (SampleAttackerCheck)
        assert score[0]['score'] == 15
        time.sleep(4)
        self.process.run_checks()
        score = self.db_wrapper.get_score_for_team(self.team)
        # score = 15 (orig) + 5 (SampleServiceCheck) + -5 (SampleAttackerCheck) + 5 (SampleInjectCheck)
        print score[0]['score']
        assert score[0]['score'] == 20