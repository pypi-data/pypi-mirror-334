from meggie.utilities.testing import BaseTestAction
from meggie.utilities.testing import create_test_experiment


class BaseStatisticsTestAction(BaseTestAction):

    def setup_experiment(self):
        self.experiment = create_test_experiment(
            self.dirpath, "test_experiment", n_subjects=10
        )
        self.experiment.activate_subject("sample_01-raw")
