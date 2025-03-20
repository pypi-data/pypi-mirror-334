from meggie.datatypes.tfr.tfr import TFR
from meggie.utilities.names import next_available_name
from meggie.utilities.threading import threaded
from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action

from meggie_difference.utilities.dialogs.differenceDialogMain import DifferenceDialog


class TFRDifference(Action):
    """Creates a difference object."""

    def run(self, params={}):

        try:
            selected_name = self.data["outputs"]["tfr"][0]
        except IndexError:
            return

        meggie_tfr = self.experiment.active_subject.tfr.get(selected_name)
        if not meggie_tfr:
            return

        conditions = list(meggie_tfr.content.keys())

        name = next_available_name(
            self.experiment.active_subject.tfr.keys(), "diff_" + selected_name
        )

        difference_dialog = DifferenceDialog(
            self.window, self.experiment, conditions, name, self.handler
        )
        difference_dialog.show()

    @subject_action
    def handler(self, subject, params):
        """ """

        @threaded
        def difference_fun(subject, tfr, params):

            tfr_data = {}
            tfr_params = tfr.params.copy()
            tfr_params["scalar"] = False
            tfr_params["conditions"] = []
            for difference in params["differences"]:

                diff_name = f"{difference[0]} - {difference[1]}"

                mne_tfr1 = tfr.content.get(difference[0])
                mne_tfr2 = tfr.content.get(difference[1])

                mne_tfr = mne_tfr1.copy()
                mne_tfr._data = mne_tfr1.data - mne_tfr2.data

                mne_tfr.comment = diff_name
                mne_tfr.filename = None

                tfr_params["conditions"].append(diff_name)
                tfr_data[diff_name] = mne_tfr

            tfr_directory = subject.tfr_directory
            tfr = TFR(params["name"], tfr_directory, tfr_params, tfr_data)
            tfr.save_content()
            subject.add(tfr, "tfr")

        selected_name = self.data["outputs"]["tfr"][0]
        tfr = subject.tfr.get(selected_name)
        if not tfr:
            raise Exception("No tfr found with name " + str(selected_name))

        difference_fun(subject, tfr, params, do_meanwhile=self.window.update_ui)
        self.experiment.save_experiment_settings()
