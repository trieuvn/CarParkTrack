# Designer/PointPicker.py
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QScrollArea
from PyQt5.QtCore import Qt

class Ui_PointPickerView(object):
    def setupUi(self, PointPickerDialog):
        PointPickerDialog.setWindowTitle(f"Point Picker - Manager: {PointPickerDialog.manager_username}")
        PointPickerDialog.setGeometry(100, 100, 900, 700)

        self.layout = QVBoxLayout(PointPickerDialog)

        self.toolbar = QHBoxLayout()
        self.val_link_label = QLabel("MainMap: Not loaded")
        self.select_image_button = QPushButton("Select Image")
        self.create_button = QPushButton("Create Slot")
        self.slot_combo = QComboBox()
        self.edit_slot_button = QPushButton("Edit Slot")
        self.delete_slot_button = QPushButton("Delete Slot")
        self.save_button = QPushButton("Save")
        self.add_checkin_button = QPushButton("Add CheckIn")
        self.checkin_combo = QComboBox()
        self.edit_checkin_button = QPushButton("Edit CheckIn")
        self.remove_checkin_button = QPushButton("Remove CheckIn")

        self.toolbar.addWidget(self.val_link_label)
        self.toolbar.addWidget(self.select_image_button)
        self.toolbar.addWidget(self.create_button)
        self.toolbar.addWidget(QLabel("Slot:"))
        self.toolbar.addWidget(self.slot_combo)
        self.toolbar.addWidget(self.edit_slot_button)
        self.toolbar.addWidget(self.delete_slot_button)
        self.toolbar.addWidget(self.add_checkin_button)
        self.toolbar.addWidget(QLabel("CheckIn:"))
        self.toolbar.addWidget(self.checkin_combo)
        self.toolbar.addWidget(self.edit_checkin_button)
        self.toolbar.addWidget(self.remove_checkin_button)
        self.toolbar.addWidget(self.save_button)
        self.toolbar.addStretch()
        self.layout.addLayout(self.toolbar)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(False)
        self.layout.addWidget(self.scroll_area)

        QtCore.QMetaObject.connectSlotsByName(PointPickerDialog)