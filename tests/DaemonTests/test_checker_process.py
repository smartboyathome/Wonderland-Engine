import time
from tests.DaemonTests import CheckerProcessTestCase

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