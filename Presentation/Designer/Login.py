from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LoginView(object):
    def setupUi(self, Form):
        Form.setObjectName("LoginForm")
        Form.resize(800, 600)
        Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Form.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(30, 30, 550, 500))
        self.widget.setStyleSheet("""
            QPushButton#pushButton {
                background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(11, 131, 120, 219), stop:1 rgba(85, 98, 112, 226));
                color: rgba(255, 255, 255, 210);
                border-radius: 5px;
            }
            QPushButton#pushButton:hover {
                background-color: qlineargradient(spread:pad, x1:0, y1:0.505682, x2:1, y2:0.477, stop:0 rgba(150, 123, 111, 219), stop:1 rgba(85, 81, 84, 226));
            }
            QPushButton#pushButton:pressed {
                padding-left: 5px;
                padding-top: 5px;
                background-color: rgba(150, 123, 111, 255);
            }
            QPushButton#pushButton_2, #pushButton_3, #pushButton_4, #pushButton_5 {
                background-color: rgba(0, 0, 0, 0);
                color: rgba(85, 98, 112, 255);
            }
            QPushButton#pushButton_2:hover, #pushButton_3:hover, #pushButton_4:hover, #pushButton_5:hover {
                color: rgba(131, 96, 53, 255);
            }
            QPushButton#pushButton_2:pressed, #pushButton_3:pressed, #pushButton_4:pressed, #pushButton_5:pressed {
                padding-left: 5px;
                padding-top: 5px;
                color: rgba(91, 88, 53, 255);
            }
        """)
        self.widget.setObjectName("widget")

        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(40, 30, 280, 430))
        self.label.setStyleSheet("border-image: url(:/images/background.jpg); border-top-left-radius: 50px;")
        self.label.setText("")
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(40, 30, 280, 430))
        self.label_2.setStyleSheet("background-color: rgba(0, 0, 0, 80); border-top-left-radius: 50px;")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(270, 30, 240, 430))
        self.label_3.setStyleSheet("background-color: rgba(255, 255, 255, 255); border-bottom-right-radius: 50px;")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setGeometry(QtCore.QRect(340, 80, 100, 40))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgba(0, 0, 0, 200);")
        self.label_4.setText("Log In")
        self.label_4.setObjectName("label_4")

        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setGeometry(QtCore.QRect(295, 150, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0);
            border: none;
            border-bottom: 2px solid rgba(46, 82, 101, 200);
            color: rgba(0, 0, 0, 240);
            padding-bottom: 7px;
        """)
        self.lineEdit.setPlaceholderText("User Name")
        self.lineEdit.setObjectName("lineEdit")

        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setGeometry(QtCore.QRect(295, 215, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0);
            border: none;
            border-bottom: 2px solid rgba(46, 82, 101, 200);
            color: rgba(0, 0, 0, 240);
            padding-bottom: 7px;
        """)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setPlaceholderText("Password")
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(295, 295, 190, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.pushButton.setFont(font)
        self.pushButton.setText("L o g  I n")
        self.pushButton.setObjectName("pushButton")

        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setGeometry(QtCore.QRect(301, 345, 181, 16))
        self.label_5.setStyleSheet("color: rgba(0, 0, 0, 210);")
        self.label_5.setText("Forgot your User Name or password?")
        self.label_5.setObjectName("label_5")

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.widget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(318, 383, 141, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        for btn_id in ["pushButton_2", "pushButton_3", "pushButton_4", "pushButton_5"]:
            btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
            btn.setMaximumSize(QtCore.QSize(30, 30))
            font = QtGui.QFont()
            font.setFamily("Social Media Circled")
            font.setPointSize(15)
            btn.setFont(font)
            btn.setText({"pushButton_2": "E", "pushButton_3": "D", "pushButton_4": "M", "pushButton_5": "C"}[btn_id])
            btn.setObjectName(btn_id)
            self.horizontalLayout.addWidget(btn)

        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setGeometry(QtCore.QRect(40, 80, 230, 130))
        self.label_6.setStyleSheet("background-color: rgba(0, 0, 0, 75);")
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")

        self.label_7 = QtWidgets.QLabel(self.widget)
        self.label_7.setGeometry(QtCore.QRect(50, 80, 180, 40))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: rgba(255, 255, 255, 200);")
        self.label_7.setText("Parking")
        self.label_7.setObjectName("label_7")

        self.label_8 = QtWidgets.QLabel(self.widget)
        self.label_8.setGeometry(QtCore.QRect(50, 145, 220, 50))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: rgba(255, 255, 255, 170);")
        self.label_8.setText("DEMO")
        self.label_8.setObjectName("label_8")

        for widget in [self.label, self.label_3, self.pushButton]:
            effect = QtWidgets.QGraphicsDropShadowEffect(blurRadius=25, xOffset=0 if widget != self.pushButton else 3, yOffset=0 if widget != self.pushButton else 3)
            widget.setGraphicsEffect(effect)

        QtCore.QMetaObject.connectSlotsByName(Form)