from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QHeaderView

class Ui_CameraManagementView(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("CameraManagement")
        MainWindow.showMaximized()
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
            QGroupBox {
                background-color: rgb(255, 255, 127);
                font-family: Arial;
                font-size: 11pt;
                font-weight: bold;
            }
            QLabel {
                background-color: #4c506d;
                color: white;
            }
        """)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)

        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setObjectName("verticalLayout_6")

        # Tiêu đề
        self.label_title = QtWidgets.QLabel("Camera Management")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(20)
        font.setBold(True)
        self.label_title.setFont(font)
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.main_layout.addWidget(self.label_title)

        # GroupBox cho thông tin camera
        self.groupBox = QtWidgets.QGroupBox("Camera Info")
        self.groupBox.setObjectName("groupBox")
        font2 = QtGui.QFont()
        font2.setFamily("Arial")
        font2.setPointSize(11)
        font2.setBold(True)
        self.groupBox.setFont(font2)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")

        # Widget trái (nhập liệu và nút Add/Edit/Delete)
        self.widget_3 = QtWidgets.QWidget(self.groupBox)
        self.widget_3.setObjectName("widget_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget_3)
        self.verticalLayout_4.setObjectName("verticalLayout_4")

        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")

        # Form nhập liệu
        self.form_layout = QtWidgets.QFormLayout()
        self.form_layout.setObjectName("verticalLayout")
        self.form_layout.setLabelAlignment(QtCore.Qt.AlignRight)
        self.form_layout.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)

        font3 = QtGui.QFont()
        font3.setFamily("Arial")
        font3.setPointSize(9)
        font3.setBold(False)

        self.label_name = QtWidgets.QLabel("Name:")
        self.label_name.setObjectName("label_name")
        self.label_name.setFont(font3)
        self.name_edit = QtWidgets.QLineEdit()
        self.name_edit.setObjectName("name_edit")
        self.form_layout.addRow(self.label_name, self.name_edit)

        self.label_val_link = QtWidgets.QLabel("Validation Link:")
        self.label_val_link.setObjectName("label_val_link")
        self.label_val_link.setFont(font3)
        self.val_link_edit = QtWidgets.QLineEdit()
        self.val_link_edit.setObjectName("val_link_edit")
        self.form_layout.addRow(self.label_val_link, self.val_link_edit)

        self.label_main_map = QtWidgets.QLabel("Main Map:")
        self.label_main_map.setObjectName("label_main_map")
        self.label_main_map.setFont(font3)
        self.main_map_edit = QtWidgets.QLineEdit()
        self.main_map_edit.setObjectName("main_map_edit")
        self.form_layout.addRow(self.label_main_map, self.main_map_edit)

        self.verticalLayout_3.addLayout(self.form_layout)

        # Nút Add, Edit, Delete
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")

        self.add_button = QtWidgets.QPushButton("Add Camera")
        self.add_button.setObjectName("add_button")
        self.add_button.setEnabled(True)
        self.add_button.setIcon(QtGui.QIcon(":/blueIcons/camera.svg"))
        self.horizontalLayout_4.addWidget(self.add_button)

        self.edit_button = QtWidgets.QPushButton("Edit Camera")
        self.edit_button.setObjectName("edit_button")
        self.edit_button.setEnabled(True)
        self.edit_button.setIcon(QtGui.QIcon(":/blueIcons/edit-2.svg"))
        self.horizontalLayout_4.addWidget(self.edit_button)

        self.delete_button = QtWidgets.QPushButton("Delete Camera")
        self.delete_button.setObjectName("delete_button")
        self.delete_button.setEnabled(True)
        self.delete_button.setIcon(QtGui.QIcon(":/blueIcons/camera-off.svg"))
        self.horizontalLayout_4.addWidget(self.delete_button)

        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        # Nút Pick Points
        self.picker_button = QtWidgets.QPushButton("Pick Points")
        self.picker_button.setObjectName("picker_button")
        self.picker_button.setEnabled(True)
        self.picker_button.setIcon(QtGui.QIcon(":/blueIcons/mouse-pointer.svg"))
        self.verticalLayout_3.addWidget(self.picker_button)

        self.verticalLayout_4.addLayout(self.verticalLayout_3)
        self.horizontalLayout_6.addWidget(self.widget_3)

        # Widget phải (PTS ID, Clear PTS Points, Delete PTS, Mapping)
        self.widget = QtWidgets.QWidget(self.groupBox)
        self.widget.setObjectName("widget")
        self.widget.setStyleSheet("QWidget { background-color: rgb(255, 255, 127); }")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.pts_id_edit = QtWidgets.QLineEdit()
        self.pts_id_edit.setObjectName("pts_id_edit")
        self.pts_id_edit.setPlaceholderText("Enter PTS ID to delete")
        self.verticalLayout_2.addWidget(self.pts_id_edit)

        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")

        self.clear_pts_points_button = QtWidgets.QPushButton("Clear PTS Points")
        self.clear_pts_points_button.setObjectName("clear_pts_points_button")
        self.clear_pts_points_button.setEnabled(True)
        self.clear_pts_points_button.setStyleSheet("""
            QPushButton {
                background-color: #4c506d;
            }
            QPushButton:hover {
                background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(150, 123, 111, 219), stop:1 rgba(85, 81, 84, 226));
            }
            QPushButton:pressed {
                background-color: rgba(150, 123, 111, 255);
            }
        """)
        self.horizontalLayout_5.addWidget(self.clear_pts_points_button)

        self.delete_pts_button = QtWidgets.QPushButton("Delete PTS")
        self.delete_pts_button.setObjectName("delete_pts_button")
        self.delete_pts_button.setEnabled(True)
        self.delete_pts_button.setStyleSheet("""
            QPushButton {
                background-color: #4c506d;
            }
            QPushButton:hover {
                background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(150, 123, 111, 219), stop:1 rgba(85, 81, 84, 226));
            }
            QPushButton:pressed {
                background-color: rgba(150, 123, 111, 255);
            }
        """)
        self.horizontalLayout_5.addWidget(self.delete_pts_button)

        self.verticalLayout_2.addLayout(self.horizontalLayout_5)

        self.mapping_button = QtWidgets.QPushButton("Mapping")
        self.mapping_button.setObjectName("mapping_button")
        self.mapping_button.setEnabled(True)
        self.mapping_button.setIcon(QtGui.QIcon(":/blueIcons/map-pin.svg"))
        self.mapping_button.setStyleSheet("""
            QPushButton {
                background-color: rgb(154, 50, 205);
            }
            QPushButton:hover {
                background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(150, 123, 111, 219), stop:1 rgba(85, 81, 84, 226));
            }
            QPushButton:pressed {
                background-color: rgba(150, 123, 111, 255);
            }
        """)
        self.verticalLayout_2.addWidget(self.mapping_button)

        self.horizontalLayout_6.addWidget(self.widget)
        self.main_layout.addWidget(self.groupBox)

        # Widget chứa Operate, Table và Clear Form
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.widget_2)
        self.verticalLayout_5.setObjectName("verticalLayout_5")

        self.operate_button = QtWidgets.QPushButton("Operate")
        self.operate_button.setObjectName("operate_button")
        self.operate_button.setEnabled(True)
        self.operate_button.setIcon(QtGui.QIcon("C:/Users/ADMIN/Pictures/operate.png"))
        self.operate_button.setIconSize(QtCore.QSize(39, 18))
        self.verticalLayout_5.addWidget(self.operate_button)

        self.table = QtWidgets.QTableWidget()
        self.table.setObjectName("table")
        self.table.setColumnCount(11)
        self.table.setHorizontalHeaderLabels([
            "ID", "Name", "ValLink", "CheckInLoc", "d1x", "d1y", "d2x", "d2y", "d3x", "d3y", "d4x"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.table.setShowGrid(True)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_5.addWidget(self.table)

        self.clear_button = QtWidgets.QPushButton("Clear Form")
        self.clear_button.setObjectName("clear_button")
        self.clear_button.setEnabled(True)
        self.clear_button.setIcon(QtGui.QIcon(":/blueIcons/trash-2.svg"))
        self.verticalLayout_5.addWidget(self.clear_button)

        self.main_layout.addWidget(self.widget_2)

        # Menu bar và Status bar
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1022, 21))
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)