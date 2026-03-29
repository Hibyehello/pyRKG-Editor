from rkg_py import rkg
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Signal
import os

from RKGEditor import RkgEditorWidget
from MiiEditor import MiiEditorWidget


class MainWidget(QtWidgets.QMainWindow):
    file_chosen = Signal()

    def __init__(self):
        super().__init__()

        self.rkg_header = rkg.rkg_header()

        self.rkg_editor = RkgEditorWidget(self.rkg_header)
        self.mii_editor = MiiEditorWidget(self.rkg_header)

        self.central_widget = QtWidgets.QWidget()

        self.tab_widget = QtWidgets.QTabWidget()
        self.tab_widget.addTab(self.rkg_editor, "Metadata")
        self.tab_widget.addTab(self.mii_editor, "Mii")

        self.file_button = QtWidgets.QPushButton("Open Ghost File")

        self.layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.layout.addWidget(self.file_button)

        self.setCentralWidget(self.central_widget)

        self.file_button.clicked.connect(self.getRkgFile)
        self.file_chosen.connect(self.createTabUI)

    @QtCore.Slot()
    def getRkgFile(self):
        self.file_path = QtWidgets.QFileDialog.getOpenFileName(self, self.tr("Open Ghost File"), os.getcwd(), self.tr("Mario Kart Wii Ghost File (*.rkg)"))[0]
        if self.file_path == '':
            return
        with open(self.file_path, "rb") as file:
            self.rkg_header.parse_file(file)
        if self.rkg_header.ID == 'RKGD':
            self.file_chosen.emit()
        else:
            QtWidgets.QMessageBox.critical(self,
                                           self.tr("Error!"),
                                           self.tr("That is not a valid RKG File!"))

    @QtCore.Slot()
    def getOutputRKG(self):
        self.out_file = QtWidgets.QFileDialog.getSaveFileName(self, self.tr("Save RKG"), os.getcwd(), self.tr("Mario Kart Wii Ghost File (*.rkg)"))[0]

    @QtCore.Slot()
    def saveGhost(self):
        if not hasattr(self, "out_file"):
            self.getOutputRKG()

        # If the user doesn't actually select a file
        if self.out_file == "":
            return

        with open(self.out_file, "wb") as out:
            out.write(self.rkg_header.pack_bytes())

    def createTabUI(self):
        self.layout.removeWidget(self.file_button)
        self.file_button.deleteLater()
        self.rkg_editor.ShowUI()
        self.mii_editor.ShowUI()
        print_btn = QtWidgets.QPushButton("Print Current RKG Data")
        print_btn.clicked.connect(lambda: print(self.rkg_header))

        save_btn = QtWidgets.QPushButton("Save to RKG")
        save_btn.clicked.connect(self.saveGhost)

        self.layout.addWidget(self.tab_widget)
        self.layout.addWidget(print_btn)
        self.layout.addWidget(save_btn)

        QtWidgets.QApplication.processEvents()
        self.adjustSize()
