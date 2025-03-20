"""Contains implementation for spectrum permutation tests"""

from meggie.utilities.messaging import exc_messagebox

from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action

from meggie_statistics.actions.spectrum_permutation_test.controller.spectrum import (
    run_permutation_test,
)
from meggie_statistics.utilities.dialogs.permutationTestDialogMain import (
    PermutationTestDialog,
)


class PermutationTest(Action):
    """Runs permutation tests for spectrum items"""

    def run(self, params={}):
        try:
            selected_name = self.data["outputs"]["spectrum"][0]
        except IndexError:
            return

        meggie_item = self.experiment.active_subject.spectrum[selected_name]

        def handle_close(params):
            params["name"] = selected_name
            try:
                self.handler(self.experiment.active_subject, params)
            except Exception as exc:
                exc_messagebox(self.window, exc)

        dialog = PermutationTestDialog(
            self.experiment,
            self.window,
            handle_close,
            meggie_item,
            limit_frequency=True,
        )
        dialog.show()

    @subject_action
    def handler(self, subject, params):
        """ """
        run_permutation_test(
            self.experiment,
            self.window,
            params["name"],
            params["groups"],
            params["time_limits"],
            params["frequency_limits"],
            params["location_limits"],
            params["threshold"],
            params["significance"],
            params["n_permutations"],
            params["design"],
        )
