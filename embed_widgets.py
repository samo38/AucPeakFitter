from PySide6 import QtWidgets
import gui_import
import gui_species_list
import gui_species_control


class ImportWidget(QtWidgets.QFrame, gui_import.Ui_Frame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)


class SpeciesList(QtWidgets.QFrame, gui_species_list.Ui_Frame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)


class SpeciesControl(QtWidgets.QFrame, gui_species_control.Ui_Frame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setupUi(self)




