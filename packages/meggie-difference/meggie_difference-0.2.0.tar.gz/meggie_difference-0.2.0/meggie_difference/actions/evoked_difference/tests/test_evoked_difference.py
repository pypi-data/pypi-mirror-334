import mne

from meggie.utilities.testing import create_evoked_conditions_experiment
from meggie.utilities.events import find_events
from meggie.utilities.events import find_stim_channel
from meggie.utilities.testing import BaseTestAction
from meggie.datatypes.epochs.epochs import Epochs
from meggie.datatypes.evoked.evoked import Evoked

from meggie_difference.actions.evoked_difference import EvokedDifference
from meggie_difference.utilities.dialogs.differenceDialogMain import (
    DifferenceDialog,
)


def create_difference_experiment(experiment_folder, experiment_name, n_subjects=2):
    """Generate experiment with data for testing."""

    experiment = create_evoked_conditions_experiment(
        experiment_folder, experiment_name, n_subjects=n_subjects
    )

    # create trivial content
    for subject in experiment.subjects.values():
        raw = subject.get_raw()

        # create epochs
        stim_channel = find_stim_channel(raw)
        events = find_events(raw, stim_channel)

        epochs_directory = subject.epochs_directory

        params = {
            "tmin": -0.1,
            "tmax": 0.2,
            "bstart": -0.1,
            "bend": 0.2,
        }
        category = {"1": 1}
        mne_epochs_1 = mne.Epochs(
            raw,
            events,
            category,
            tmin=params["tmin"],
            tmax=params["tmax"],
            baseline=(params["bstart"], params["bend"]),
        )
        epochs_1 = Epochs("Epochs", epochs_directory, params, content=mne_epochs_1)
        epochs_1.save_content()
        subject.add(epochs_1, "epochs")

        params = {
            "tmin": -0.1,
            "tmax": 0.2,
            "bstart": -0.1,
            "bend": 0.2,
        }
        category = {"2": 2}

        mne_epochs_2 = mne.Epochs(
            raw,
            events,
            category,
            tmin=params["tmin"],
            tmax=params["tmax"],
            baseline=(params["bstart"], params["bend"]),
        )
        epochs_directory = subject.epochs_directory
        epochs_2 = Epochs("Epochs", epochs_directory, params, content=mne_epochs_2)
        epochs_2.save_content()
        subject.add(epochs_2, "epochs")

        # create evoked with two conditions
        params = {"conditions": ["epochs_1", "epochs_2"]}
        content = {
            "epochs_1": mne_epochs_1.average(),
            "epochs_2": mne_epochs_2.average(),
        }
        evoked_directory = subject.evoked_directory
        evoked = Evoked("Evoked", evoked_directory, params, content=content)
        evoked.save_content()
        subject.add(evoked, "evoked")

    return experiment


class TestEvokedDifference(BaseTestAction):

    def setup_experiment(self):
        self.experiment = create_difference_experiment(self.dirpath, "test_experiment")
        self.experiment.activate_subject("sample_01-raw")

    def test_evoked_difference(self):

        data = {"outputs": {"evoked": ["Evoked"]}}

        self.run_action(
            action_name="evoked_difference",
            handler=EvokedDifference,
            data=data,
            patch_paths=["meggie_difference.actions.evoked_difference"],
        )
        dialog = self.find_dialog(DifferenceDialog)
        dialog.differences = [("epochs_1", "epochs_2")]
        dialog.accept()
