import time
from ScoringDaemon.check_types import ServiceCheck

class SampleServiceCheck(ServiceCheck):
    def __init__(self, machine):
        self._machine = machine

    @property
    def machine(self):
        return self._machine

    @property
    def timeout(self):
        return 60

    @property
    def score(self):
        return 5

    def run_check(self):
        time.sleep(45)
        return True