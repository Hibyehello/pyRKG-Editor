from py_rkg import rkg
from PySide6 import QtCore, QtWidgets, QtGui


class MiiEditorWidget(QtWidgets.QWidget):
    def __init__(self, rkg_header):
        super().__init__()

        self.mii_data = rkg_header.mii

        self.layout = QtWidgets.QVBoxLayout(self)

    @QtCore.Slot()
    def ShowUI(self):
        self.mii_image_data = QtGui.QImage()
        self.mii_image_data.loadFromData(self.mii_data.fetch_mii_image())

        self.mii_image = QtGui.QPixmap.fromImage(self.mii_image_data)

        self.image_lbl = QtWidgets.QLabel(self)
        self.image_lbl.setPixmap(self.mii_image)

        self.name_lbl = QtWidgets.QLabel(self, text=self.mii_data.name.strip('\x00'))
        self.name_lbl.setStyleSheet("font-size: 24pt;")

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.name_lbl, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.layout.addWidget(self.image_lbl, alignment=QtCore.Qt.AlignmentFlag.AlignHCenter)
