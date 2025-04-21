from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QDialog, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QComboBox, QSlider, QScrollArea
from PyQt5.QtCore import Qt

class Ui_PointPickerView(object):
    def setupUi(self, PointPickerDialog):
        PointPickerDialog.setWindowTitle(f"Point Picker - Camera ID: {PointPickerDialog.camera_id}")
        PointPickerDialog.setGeometry(100, 100, 900, 700)

        self.layout = QVBoxLayout(PointPickerDialog)

        self.toolbar = QHBoxLayout()
        self.val_link_label = QLabel("ValLink: Not loaded")
        self.select_image_button = QPushButton("Select Image")
        self.select_video_button = QPushButton("Select Video")
        self.edit_check_in_button = QPushButton("Edit Check In")
        self.slot_combo = QComboBox()
        self.edit_slot_button = QPushButton("Edit Slot")
        self.delete_button = QPushButton("Delete Mode")
        self.save_button = QPushButton("Save")

        self.toolbar.addWidget(self.val_link_label)
        self.toolbar.addWidget(self.select_image_button)
        self.toolbar.addWidget(self.select_video_button)
        self.toolbar.addWidget(self.edit_check_in_button)
        self.toolbar.addWidget(QLabel("Slot:"))
        self.toolbar.addWidget(self.slot_combo)
        self.toolbar.addWidget(self.edit_slot_button)
        self.toolbar.addWidget(self.delete_button)
        self.toolbar.addWidget(self.save_button)
        self.toolbar.addStretch()
        self.layout.addLayout(self.toolbar)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(False)
        self.layout.addWidget(self.scroll_area)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(0)
        self.layout.addWidget(self.slider)

        QtCore.QMetaObject.connectSlotsByName(PointPickerDialog)