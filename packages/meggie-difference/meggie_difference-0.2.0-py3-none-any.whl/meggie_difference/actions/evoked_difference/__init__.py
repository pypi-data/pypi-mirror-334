from meggie.datatypes.evoked.evoked import Evoked
from meggie.utilities.names import next_available_name
from meggie.utilities.threading import threaded
from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action

from meggie_difference.utilities.dialogs.differenceDialogMain import DifferenceDialog


class EvokedDifference(Action):
    """Creates a difference object."""

    def run(self, params={}):

        try:
            selected_name = self.data["outputs"]["evoked"][0]
        except IndexError:
            return

        meggie_evoked = self.experiment.active_subject.evoked.get(selected_name)
        if not meggie_evoked:
            return

        conditions = list(meggie_evoked.content.keys())

        name = next_available_name(
            self.experiment.active_subject.evoked.keys(), "diff_" + selected_name
        )

        difference_dialog = DifferenceDialog(
            self.window, self.experiment, conditions, name, self.handler
        )
        difference_dialog.show()

    @subject_action
    def handler(self, subject, params):
        """ """

        @threaded
        def difference_fun(subject, evoked, params):
            evokeds = {}
            evoked_params = {"conditions": []}
            for difference in params["differences"]:

                diff_name = f"{difference[0]} - {difference[1]}"

                mne_evoked1 = evoked.content.get(difference[0])
                mne_evoked2 = evoked.content.get(difference[1])

                mne_evoked = mne_evoked1.copy()
                mne_evoked._data = mne_evoked1.data - mne_evoked2.data

                mne_evoked.comment = diff_name
                mne_evoked.filename = None

                evoked_params["conditions"].append(diff_name)
                evokeds[diff_name] = mne_evoked

            evoked_directory = subject.evoked_directory
            evoked = Evoked(
                params["name"], evoked_directory, evoked_params, content=evokeds
            )
            evoked.save_content()
            subject.add(evoked, "evoked")

        selected_name = self.data["outputs"]["evoked"][0]

        evoked = subject.evoked.get(selected_name)
        if not evoked:
            raise Exception("No evoked found with name " + str(selected_name))

        difference_fun(subject, evoked, params, do_meanwhile=self.window.update_ui)
        self.experiment.save_experiment_settings()
