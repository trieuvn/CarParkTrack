from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QHeaderView

class Ui_CameraManagementView(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("CameraManagement")
        MainWindow.resize(1000, 700)
        MainWindow.setStyleSheet("""
            QWidget {
                background-color: rgba(255, 255, 255, 255);
                font-family: Arial;
            }
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(11, 131, 120, 219), stop:1 rgba(85, 98, 112, 226));
                color: rgba(255, 255, 255, 210);
                border-radius: 5px;
                padding: 8px;
                font-size: 12pt;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(150, 123, 111, 219), stop:1 rgba(85, 81, 84, 226));
            }
            QPushButton:pressed {
                background-color: rgba(150, 123, 111, 255);
            }
            QLineEdit {
                background-color: rgba(0, 0, 0, 0);
                border: none;
                border-bottom: 2px solid rgba(46, 82, 101, 200);
                color: rgba(0, 0, 0, 240);
                padding-bottom: 7px;
                font-size: 10pt;
            }
            QTableWidget {
                border: 1px solid rgba(46, 82, 101, 200);
                gridline-color: rgba(0, 0, 0, 50);
            }
            QHeaderView::section {
                background-color: rgba(11, 131, 120, 219);
                color: white;
                padding: 5px;
                border: none;
            }
        """)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)

        self.label_title = QtWidgets.QLabel("Camera Management")
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.label_title.setFont(font)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.main_layout.addWidget(self.label_title)

        self.form_widget = QtWidgets.QWidget()
        self.form_layout = QtWidgets.QFormLayout(self.form_widget)
        self.form_layout.setLabelAlignment(QtCore.Qt.AlignRight)
        self.form_layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)

        self.name_edit = QtWidgets.QLineEdit()
        self.val_link_edit = QtWidgets.QLineEdit()
        self.main_map_edit = QtWidgets.QLineEdit()
        self.picker_button = QtWidgets.QPushButton("Pick Points")
        self.picker_button.setEnabled(True)

        self.form_layout.addRow("Name:", self.name_edit)
        self.form_layout.addRow("Validation Link:", self.val_link_edit)
        self.form_layout.addRow("Main Map:", self.main_map_edit)
        self.form_layout.addRow("Points:", self.picker_button)

        self.main_layout.addWidget(self.form_widget)

        self.button_widget = QtWidgets.QWidget()
        self.button_layout = QtWidgets.QHBoxLayout(self.button_widget)
        self.button_layout.setSpacing(10)

        self.add_button = QtWidgets.QPushButton("Add Camera")
        self.edit_button = QtWidgets.QPushButton("Edit Camera")
        self.delete_button = QtWidgets.QPushButton("Delete Camera")
        self.clear_button = QtWidgets.QPushButton("Clear Form")
        self.operate_button = QtWidgets.QPushButton("Operate")
        self.mapping_button = QtWidgets.QPushButton("Mapping")
        self.delete_pts_button = QtWidgets.QPushButton("Delete PTS")
        self.clear_pts_points_button = QtWidgets.QPushButton("Clear PTS Points")  # New button
        self.pts_id_edit = QtWidgets.QLineEdit()
        self.pts_id_edit.setPlaceholderText("Enter PTS ID to delete")

        for btn in [self.add_button, self.edit_button, self.delete_button, self.clear_button,
                    self.operate_button, self.mapping_button, self.delete_pts_button,
                    self.clear_pts_points_button]:
            btn.setEnabled(True)
            btn.setVisible(True)
            self.button_layout.addWidget(btn)
        self.button_layout.addWidget(self.pts_id_edit)
        self.main_layout.addWidget(self.button_widget)

        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels([
            "ID", "Name", "ValLink", "CheckInLoc", "d1x", "d1y", "d2x", "d2y", "d3x", "d3y", "d4x"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setVisible(True)

        self.main_layout.addWidget(self.table)