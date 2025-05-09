from PyQt5 import QtCore, QtGui, QtWidgets

#url được lưu vào đâu thì copy địa chỉ đó vô border-image
class Ui_LoginView(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")

        MainWindow.setStyleSheet("""
        QMainWindow {
            
            border-image: url("C:/Users/Phuc/Downloads/lineEdit/static/100000.jpg") 12 12 12 12 stretch stretch;
            background-color: #f0f0f0;
        }
        #widget {
            background-color: #ffffff;
            border-radius: 10px;
        }
        QLabel {
            color: #767e89;
            font-size: 11pt;
        }
        QLabel#label {
            color: #000000;
            font-size: 20pt;
            font-weight: bold;
        }
        QLineEdit {
            padding: 8px 10px;
            font-size: 14pt;
            color: #333;
            background: transparent;
        }
        QLineEdit:focus {
            border-bottom: 2px solid #28a2a2;
        }
        QPushButton {
            background-color: #0d6efd;
            border: none;
            color: white;
            border-radius: 8px;
            padding: 12px;
            font-size: 14pt;
            margin-top: 20px;
        }
        QPushButton:hover {
            background-color: #0b5ed7;
        }
        """)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")

        self.gridLayout_2.addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding), 0, 1)
        self.gridLayout_2.addItem(QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum), 1, 0)

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setMinimumSize(QtCore.QSize(400, 300))
        self.widget.setObjectName("widget")

        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setObjectName("gridLayout")

        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setContentsMargins(40, 40, 40, 40)
        self.verticalLayout_4.setSpacing(20)

        self.label = QtWidgets.QLabel("Welcome", self.widget)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)

        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(15)

        self.label_2 = QtWidgets.QLabel("Username", self.widget)
        self.verticalLayout_3.addWidget(self.label_2)

        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.verticalLayout_3.addWidget(self.lineEdit)

        self.label_3 = QtWidgets.QLabel("Password", self.widget)
        self.verticalLayout_3.addWidget(self.label_3)

        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.verticalLayout_3.addWidget(self.lineEdit_2)

        self.verticalLayout_4.addLayout(self.verticalLayout_3)

        self.pushButton = QtWidgets.QPushButton("Login", self.widget)
        self.verticalLayout_4.addWidget(self.pushButton)

        self.gridLayout.addLayout(self.verticalLayout_4, 0, 0, 1, 1)

        self.gridLayout_2.addWidget(self.widget, 1, 1)
        self.gridLayout_2.addItem(QtWidgets.QSpacerItem(100, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum), 1, 2)
        self.gridLayout_2.addItem(QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding), 2, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Login App"))
        


    
