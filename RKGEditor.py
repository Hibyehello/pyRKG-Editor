from rkg_py import rkg
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Signal
import os


class RkgEditorWidget(QtWidgets.QWidget):
    file_chosen = Signal()

    def __init__(self, rkg_header):
        super().__init__()

        self.rkg_header = rkg_header

        self.layout = QtWidgets.QVBoxLayout()

    @QtCore.Slot()
    def ShowUI(self):
        timer_layout = QtWidgets.QHBoxLayout()
        timer_lbl = QtWidgets.QLabel("Finish Timer:")
        self.finish_time = [QtWidgets.QSpinBox(), QtWidgets.QSpinBox(), QtWidgets.QSpinBox()]
        for box in self.finish_time:
            box.setMaximum(999)

        self.finish_time[0].setValue(self.rkg_header.timer.minutes)
        self.finish_time[0].valueChanged.connect(lambda v: setattr(self.rkg_header.timer, "minutes", v))
        self.finish_time[1].setValue(self.rkg_header.timer.seconds)
        self.finish_time[1].valueChanged.connect(lambda v: setattr(self.rkg_header.timer, "seconds", v))
        self.finish_time[2].setValue(self.rkg_header.timer.ms_secs)
        self.finish_time[2].valueChanged.connect(lambda v: setattr(self.rkg_header.timer, "ms_secs", v))

        timer_layout.addWidget(timer_lbl)
        for box in self.finish_time:
            timer_layout.addWidget(box)

        self.layout.addLayout(timer_layout)

        track_layout = QtWidgets.QHBoxLayout()
        track_lbl = QtWidgets.QLabel("Track:")
        self.track_box = QtWidgets.QComboBox()

        for track in rkg.Track:
            self.track_box.addItem(track.name, track)

        self.track_box.setCurrentText(self.rkg_header.track_id.name)
        self.track_box.currentIndexChanged.connect(lambda v: setattr(self.rkg_header, "track_id", self.track_box.currentData()))

        track_layout.addWidget(track_lbl)
        track_layout.addWidget(self.track_box)
        self.layout.addLayout(track_layout)

        vehicle_layout = QtWidgets.QHBoxLayout()
        vehicle_lbl = QtWidgets.QLabel("Vehicle:")
        self.vehicle_box = QtWidgets.QComboBox()

        for vehicle in rkg.Vehicle:
            self.vehicle_box.addItem(vehicle.name, vehicle)

        self.vehicle_box.setCurrentText(self.rkg_header.vehicle_id.name)
        self.vehicle_box.currentIndexChanged.connect(lambda v: setattr(self.rkg_header, "vehicle_id", self.vehicle_box.currentData()))

        vehicle_layout.addWidget(vehicle_lbl)
        vehicle_layout.addWidget(self.vehicle_box)
        self.layout.addLayout(vehicle_layout)

        character_layout = QtWidgets.QHBoxLayout()
        character_lbl = QtWidgets.QLabel("Character:")
        self.character_box = QtWidgets.QComboBox()

        for character in rkg.Character:
            self.character_box.addItem(character.name, character)

        self.character_box.setCurrentText(self.rkg_header.character_id.name)
        self.character_box.currentIndexChanged.connect(lambda v: setattr(self.rkg_header, "character_id", self.character_box.currentData()))

        character_layout.addWidget(character_lbl)
        character_layout.addWidget(self.character_box)
        self.layout.addLayout(character_layout)

        date_layout = QtWidgets.QHBoxLayout()
        date_lbl = [QtWidgets.QLabel("Day:"), QtWidgets.QLabel("Month:"), QtWidgets.QLabel("Year:")]
        self.date_boxes = [QtWidgets.QSpinBox(), QtWidgets.QSpinBox(), QtWidgets.QSpinBox()]
        self.date_boxes[0].setValue(self.rkg_header.day)
        self.date_boxes[0].valueChanged.connect(lambda v: setattr(self.rkg_header, "day", v))
        self.date_boxes[1].setValue(self.rkg_header.month)
        self.date_boxes[1].valueChanged.connect(lambda v: setattr(self.rkg_header, "month", v))
        self.date_boxes[2].setMaximum(99)
        self.date_boxes[2].setValue(self.rkg_header.year)
        self.date_boxes[2].valueChanged.connect(lambda v: setattr(self.rkg_header, "year", v))

        for i in range(len(date_lbl)):
            date_layout.addWidget(date_lbl[i])
            date_layout.addWidget(self.date_boxes[i])

        self.layout.addLayout(date_layout)

        controller_layout = QtWidgets.QHBoxLayout()
        controller_lbl = QtWidgets.QLabel("Controller:")
        self.controller_box = QtWidgets.QComboBox()

        for controller in rkg.Controller_Type:
            self.controller_box.addItem(controller.name, controller)

        self.controller_box.setCurrentText(self.rkg_header.controller.name)
        self.controller_box.currentIndexChanged.connect(lambda v: setattr(self.rkg_header, "controller", self.controller_box.currentData()))

        controller_layout.addWidget(controller_lbl)
        controller_layout.addWidget(self.controller_box)
        self.layout.addLayout(controller_layout)

        ghost_layout = QtWidgets.QHBoxLayout()
        ghost_lbl = QtWidgets.QLabel("Ghost Type:")
        self.ghost_box = QtWidgets.QComboBox()

        for ghost in rkg.Ghost:
            self.ghost_box.addItem(ghost.name, ghost)

        self.ghost_box.setCurrentText(self.rkg_header.ghost_type.name)
        self.ghost_box.currentIndexChanged.connect(lambda v: setattr(self.rkg_header, "ghost_type", self.ghost_box.currentData()))

        ghost_layout.addWidget(ghost_lbl)
        ghost_layout.addWidget(self.ghost_box)
        self.layout.addLayout(ghost_layout)

        drift_layout = QtWidgets.QHBoxLayout()
        drift_lbl = QtWidgets.QLabel("Drift Type:")
        self.drift_box = QtWidgets.QComboBox()

        for drift in rkg.Drift:
            self.drift_box.addItem(drift.name, drift)

        self.drift_box.setCurrentText(self.rkg_header.drift_type.name)
        self.drift_box.currentIndexChanged.connect(lambda v: setattr(self.rkg_header, "drift_type", self.drift_box.currentData()))

        drift_layout.addWidget(drift_lbl)
        drift_layout.addWidget(self.drift_box)
        self.layout.addLayout(drift_layout)

        data_length_layout = QtWidgets.QHBoxLayout()
        data_length_lbl = QtWidgets.QLabel("Data Length:")
        self.data_length_box = QtWidgets.QLineEdit()
        self.data_length_box.setReadOnly(True)
        self.data_length_box.setText(str(self.rkg_header.data_length))

        data_length_layout.addWidget(data_length_lbl)
        data_length_layout.addWidget(self.data_length_box)
        self.layout.addLayout(data_length_layout)

        self.splits = [0] * self.rkg_header.lap_count

        for i in range(self.rkg_header.lap_count):
            splits_layout = QtWidgets.QHBoxLayout()
            splits_lbl = QtWidgets.QLabel(f"Lap {i+1} Time:")
            self.splits[i] = [QtWidgets.QSpinBox(), QtWidgets.QSpinBox(), QtWidgets.QSpinBox()]
            for box in self.splits[i]:
                box.setMaximum(999)

            self.splits[i][0].setValue(self.rkg_header.splits[i].minutes)
            self.splits[i][1].setValue(self.rkg_header.splits[i].seconds)
            self.splits[i][2].setValue(self.rkg_header.splits[i].ms_secs)

            self.splits[i][0].valueChanged.connect(lambda v, i=i: setattr(self.rkg_header.splits[i], "minutes", v))
            self.splits[i][1].valueChanged.connect(lambda v, i=i: setattr(self.rkg_header.splits[i], "seconds", v))
            self.splits[i][2].valueChanged.connect(lambda v, i=i: setattr(self.rkg_header.splits[i], "ms_secs", v))

            splits_layout.addWidget(splits_lbl)
            for box in self.splits[i]:
                splits_layout.addWidget(box)

            self.layout.addLayout(splits_layout)

            self.setLayout(self.layout)


