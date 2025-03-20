from meggie.utilities.testing import BaseTestAction

from meggie_difference.actions.spectrum_difference import SpectrumDifference
from meggie_difference.utilities.dialogs.differenceDialogMain import (
    DifferenceDialog,
)


class TestSpectrumDifference(BaseTestAction):

    def test_spectrum_difference(self):

        data = {"outputs": {"spectrum": ["Spectrum"]}}

        self.run_action(
            action_name="spectrum_difference",
            handler=SpectrumDifference,
            data=data,
            patch_paths=["meggie_difference.actions.spectrum_difference"],
        )
        dialog = self.find_dialog(DifferenceDialog)
        dialog.differences = [("1", "2")]
        dialog.accept()
