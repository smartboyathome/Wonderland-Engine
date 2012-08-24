from tests import DaemonTestCase

class TestDaemon(DaemonTestCase):
    def test_team_count(self):
        assert self.master_process.is_alive()
        assert len(self.master.checkers) == 3

