import time
from tests import DaemonTestCase

class TestMaster(DaemonTestCase):
    def test_team_count(self):
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
        '''for team in scores:
            assert scores[team] == 5'''