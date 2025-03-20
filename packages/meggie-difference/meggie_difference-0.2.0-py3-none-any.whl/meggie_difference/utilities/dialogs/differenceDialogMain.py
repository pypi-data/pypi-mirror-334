"""Contains a class for logic of the difference dialog."""

import logging

from PyQt5 import QtWidgets

from meggie_difference.utilities.dialogs.differenceDialogUi import Ui_differenceDialog
from meggie.utilities.widgets.batchingWidgetMain import BatchingWidget
from meggie.utilities.messaging import exc_messagebox


class DifferenceDialog(QtWidgets.QDialog):
    """Contains logic for the difference dialog."""

    def __init__(self, parent, experiment, conditions, name, handler):
        QtWidgets.QDialog.__init__(self, parent)
        self.ui = Ui_differenceDialog()
        self.ui.setupUi(self)

        self.experiment = experiment
        self.parent = parent
        self.handler = handler

        self.name = name
        self.differences = []

        for condition in conditions:
            self.ui.comboBoxCondition1.addItem(condition)
            self.ui.comboBoxCondition2.addItem(condition)

        self.batching_widget = BatchingWidget(
            experiment_getter=self._experiment_getter,
            parent=self,
            container=self.ui.groupBoxBatching,
            geometry=self.ui.batchingWidgetPlaceholder.geometry(),
        )
        self.ui.gridLayoutBatching.addWidget(self.batching_widget, 0, 0, 1, 1)

    def _experiment_getter(self):
        return self.experiment

    def on_pushButtonAdd_clicked(self, checked=None):
        if checked is None:
            return

        condition1 = self.ui.comboBoxCondition1.currentText()
        condition2 = self.ui.comboBoxCondition2.currentText()

        self.differences.append((condition1, condition2))

        item_name = f"{condition1} - {condition2}"
        self.ui.listWidgetDifferences.addItem(item_name)

    def on_pushButtonClear_clicked(self, checked=None):
        if checked is None:
            return

        self.ui.listWidgetDifferences.clear()
        self.differences = []

    def accept(self):
        subject = self.experiment.active_subject

        params = {"differences": self.differences, "name": self.name}

        try:
            self.handler(subject, params)
        except Exception as exc:
            exc_messagebox(self.parent, exc)
            return

        self.parent.initialize_ui()
        self.close()

    def acceptBatch(self):

        selected_subject_names = self.batching_widget.selected_subjects

        for name, subject in self.experiment.subjects.items():
            if name in selected_subject_names:
                try:
                    params = {"differences": self.differences, "name": self.name}

                    self.handler(subject, params)
                    subject.release_memory()
                except Exception as exc:
                    self.batching_widget.failed_subjects.append((subject, str(exc)))
                    logging.getLogger("ui_logger").exception("")
        self.batching_widget.cleanup()

        self.parent.initialize_ui()
        self.close()
