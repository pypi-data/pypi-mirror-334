"""Contains a class for logic of the permutation test dialog."""

from PyQt5 import QtWidgets


from meggie.utilities.channels import get_channels_by_type

from meggie.utilities.messaging import messagebox

from meggie_statistics.utilities.dialogs.permutationTestDialogUi import (
    Ui_permutationTestDialog,
)
from meggie.utilities.dialogs.groupSelectionDialogMain import GroupSelectionDialog


class PermutationTestDialog(QtWidgets.QDialog):
    """Contains logic for the permutation test dialog."""

    def __init__(
        self,
        experiment,
        parent,
        handler,
        meggie_item,
        limit_frequency=False,
        limit_time=False,
        limit_channel=True,
    ):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_permutationTestDialog()
        self.ui.setupUi(self)

        self.handler = handler
        self.experiment = experiment

        ch_types = get_channels_by_type(meggie_item.info).keys()
        self.channel_group_options = []

        # add eeg if relevant
        if experiment.channel_groups.get("eeg") and "eeg" in ch_types:
            for ch_group_name, _ in experiment.channel_groups["eeg"].items():
                self.channel_group_options.append(("eeg", ch_group_name))

        # add grad if relevant
        if experiment.channel_groups.get("meg") and "grad" in ch_types:
            for ch_group_name, _ in experiment.channel_groups["meg"].items():
                self.channel_group_options.append(("grad", ch_group_name))

        # add mag if relevant
        if experiment.channel_groups.get("meg") and "mag" in ch_types:
            for ch_group_name, _ in experiment.channel_groups["meg"].items():
                self.channel_group_options.append(("mag", ch_group_name))

        self.limit_frequency = limit_frequency
        self.limit_time = limit_time
        self.limit_channel = limit_channel

        if not limit_time:
            self.ui.groupBoxTime.hide()
        else:
            self.ui.doubleSpinBoxTimeTmin.setValue(meggie_item.times[0])
            self.ui.doubleSpinBoxTimeTmax.setValue(meggie_item.times[-1])

        if not limit_frequency:
            self.ui.groupBoxFrequency.hide()
        else:
            self.ui.doubleSpinBoxFrequencyFmin.setValue(meggie_item.freqs[0])
            self.ui.doubleSpinBoxFrequencyFmax.setValue(meggie_item.freqs[-1])

        if not limit_channel:
            self.ui.groupBoxChannel.hide()
        else:
            for ch_type in ch_types:
                self.ui.comboBoxChannelType.addItem(ch_type)
            for ch_name in meggie_item.info["ch_names"]:
                self.ui.comboBoxChannelName.addItem(ch_name)
            for ch_type, ch_group_name in self.channel_group_options:
                self.ui.comboBoxChannelGroup.addItem(f"{ch_type} - {ch_group_name}")

        self.meggie_item = meggie_item

        self.groups = {}

    def on_pushButtonGroups_clicked(self, checked=None):
        if checked is None:
            return

        def handler(groups):
            if not groups:
                return

            self.groups = groups
            self.ui.listWidgetGroups.clear()
            for key, names in sorted(groups.items(), key=lambda x: x[0]):
                for name in sorted(names):
                    item_name = str(key) + ": " + str(name)
                    self.ui.listWidgetGroups.addItem(item_name)

        dialog = GroupSelectionDialog(self.experiment, self, handler)
        dialog.show()

    def accept(self):
        if not self.groups:
            messagebox(self, "You should select some groups first")
            return

        if self.ui.radioButtonWithinSubjects.isChecked():
            design = "within-subjects"
        else:
            design = "between-subjects"

        if design == "between-subjects" and len(self.groups) <= 1:
            messagebox(
                self, "At least two groups are needed for between-subjects design"
            )
            return

        if design == "within-subjects":
            conditions = self.meggie_item.content.keys()
            if len(conditions) <= 1:
                messagebox(
                    self,
                    "At least two conditions are needed for within-subjects design",
                )
                return

        time_limits = None
        frequency_limits = None
        location_limits = None

        if self.limit_time and self.ui.radioButtonTimeEnabled.isChecked():
            tmin = self.ui.doubleSpinBoxTimeTmin.value()
            tmax = self.ui.doubleSpinBoxTimeTmax.value()
            time_limits = tmin, tmax

        if self.limit_frequency and self.ui.radioButtonFrequencyEnabled.isChecked():
            fmin = self.ui.doubleSpinBoxFrequencyFmin.value()
            fmax = self.ui.doubleSpinBoxFrequencyFmax.value()
            frequency_limits = fmin, fmax

        if self.limit_channel and self.ui.radioButtonChannelType.isChecked():
            location_limits = ("ch_type", self.ui.comboBoxChannelType.currentText())
        if self.limit_channel and self.ui.radioButtonChannelName.isChecked():
            location_limits = ("ch_name", self.ui.comboBoxChannelName.currentText())
        if self.limit_channel and self.ui.radioButtonChannelGroup.isChecked():
            idx = self.ui.comboBoxChannelGroup.currentIndex()
            ch_group_choice = self.channel_group_options[idx]
            location_limits = ("ch_group", ch_group_choice)

        threshold = self.ui.doubleSpinBoxClusterThreshold.value()
        significance = self.ui.doubleSpinBoxClusterSignificance.value()
        n_permutations = self.ui.spinBoxNPermutations.value()

        params = {}
        params["groups"] = self.groups
        params["time_limits"] = time_limits
        params["frequency_limits"] = frequency_limits
        params["location_limits"] = location_limits
        params["threshold"] = threshold
        params["significance"] = significance
        params["n_permutations"] = n_permutations
        params["design"] = design

        self.handler(params)
        self.close()
