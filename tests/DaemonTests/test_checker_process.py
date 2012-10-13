import time
from tests.DaemonTests import CheckerProcessTestCase

class TestCheckerProcess(CheckerProcessTestCase):
    def test_checker_start(self):
        self.process.start()
        assert self.process.is_alive()

    def test_checker_stop(self):
        self.process.start()
        self.process.shutdown_event.set()
        self.process.join(5)
        assert not self.process.is_alive()

    def test_checker_scores(self):
        self.process.run_checks()
        stuff = self.db_wrapper.get_all_completed_checks_for_team(self.team)
        scores = self.db_wrapper.get_scores_for_all_teams()
        score = [obj for obj in scores if obj['team_id'] == self.team][0]['score']
        assert score == 20