from meggie.datatypes.spectrum.spectrum import Spectrum
from meggie.utilities.names import next_available_name
from meggie.utilities.threading import threaded
from meggie.mainwindow.dynamic import Action
from meggie.mainwindow.dynamic import subject_action

from meggie_difference.utilities.dialogs.differenceDialogMain import DifferenceDialog


class SpectrumDifference(Action):
    """Creates a difference object."""

    def run(self, params={}):

        try:
            selected_name = self.data["outputs"]["spectrum"][0]
        except IndexError:
            return

        meggie_spectrum = self.experiment.active_subject.spectrum.get(selected_name)
        if not meggie_spectrum:
            return

        conditions = list(meggie_spectrum.content.keys())

        name = next_available_name(
            self.experiment.active_subject.spectrum.keys(), "diff_" + selected_name
        )

        difference_dialog = DifferenceDialog(
            self.window, self.experiment, conditions, name, self.handler
        )
        difference_dialog.show()

    @subject_action
    def handler(self, subject, params):
        """ """

        @threaded
        def difference_fun(subject, spectrum, params):
            spectrum_data = {}

            spectrum_params = spectrum.params.copy()
            del spectrum_params["intervals"]
            spectrum_params["scalar"] = False
            spectrum_params["conditions"] = []
            for difference in params["differences"]:

                diff_name = f"{difference[0]} - {difference[1]}"

                data_1 = spectrum.content.get(difference[0])
                data_2 = spectrum.content.get(difference[1])

                data = data_1 - data_2
                spectrum_params["conditions"].append(diff_name)
                spectrum_data[diff_name] = data

            spectrum_directory = subject.spectrum_directory
            spectrum = Spectrum(
                params["name"],
                spectrum_directory,
                spectrum_params,
                spectrum_data,
                spectrum.freqs,
                spectrum.info,
            )
            spectrum.save_content()
            subject.add(spectrum, "spectrum")

        selected_name = self.data["outputs"]["spectrum"][0]
        spectrum = subject.spectrum.get(selected_name)
        if not spectrum:
            raise Exception("No spectrum found with name " + str(selected_name))

        difference_fun(subject, spectrum, params, do_meanwhile=self.window.update_ui)
        self.experiment.save_experiment_settings()
