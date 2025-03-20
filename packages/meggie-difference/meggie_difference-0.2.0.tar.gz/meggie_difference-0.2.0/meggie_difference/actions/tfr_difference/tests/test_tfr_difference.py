from meggie.utilities.testing import BaseTestAction
from meggie_difference.actions.tfr_difference import TFRDifference
from meggie_difference.utilities.dialogs.differenceDialogMain import (
    DifferenceDialog,
)


class TestTFRDifference(BaseTestAction):

    def test_tfr_difference(self):

        data = {"outputs": {"tfr": ["TFR"]}}

        self.run_action(
            action_name="tfr_difference",
            handler=TFRDifference,
            data=data,
            patch_paths=["meggie_difference.actions.tfr_difference"],
        )
        dialog = self.find_dialog(DifferenceDialog)
        dialog.differences = [("Epochs", "Epochs2")]
        dialog.accept()
