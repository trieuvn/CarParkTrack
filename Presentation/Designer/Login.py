from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LoginView(object):
    def setupUi(self, Form):
        Form.setObjectName("LoginForm")
        Form.resize(900, 650)  # Tăng kích thước cửa sổ cho bố cục rộng rãi
        Form.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        Form.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.widget = QtWidgets.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(50, 50, 600, 550))
        self.widget.setStyleSheet("""
            QPushButton#pushButton {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(52, 152, 219, 230), stop:1 rgba(41, 128, 185, 230));
                color: rgba(255, 255, 255, 240);
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton#pushButton:hover {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(41, 128, 185, 230), stop:1 rgba(52, 152, 219, 230));
            }
            QPushButton#pushButton:pressed {
                background-color: rgba(41, 128, 185, 255);
                padding-left: 3px;
                padding-top: 3px;
            }
            QPushButton#pushButton_2, #pushButton_3, #pushButton_4, #pushButton_5 {
                background-color: rgba(0, 0, 0, 0);
                color: rgba(44, 62, 80, 255);
                border: 1px solid rgba(44, 62, 80, 100);
                border-radius: 15px;
            }
            QPushButton#pushButton_2:hover, #pushButton_3:hover, #pushButton_4:hover, #pushButton_5:hover {
                color: rgba(52, 152, 219, 255);
                border-color: rgba(52, 152, 219, 200);
            }
            QPushButton#pushButton_2:pressed, #pushButton_3:pressed, #pushButton_4:pressed, #pushButton_5:pressed {
                color: rgba(41, 128, 185, 255);
                background-color: rgba(52, 152, 219, 20);
            }
        """)
        self.widget.setObjectName("widget")

        # Label nền với hình ảnh
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(50, 30, 300, 480))
        self.label.setStyleSheet("border-image: url(:/images/background.jpg); border-top-left-radius: 60px; border-bottom-left-radius: 60px;")
        self.label.setText("")
        self.label.setObjectName("label")

        # Lớp phủ mờ
        self.label_2 = QtWidgets.QLabel(self.widget)
        self.label_2.setGeometry(QtCore.QRect(50, 30, 300, 480))
        self.label_2.setStyleSheet("background-color: rgba(0, 0, 0, 100); border-top-left-radius: 60px; border-bottom-left-radius: 60px;")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")

        # Phần nền trắng bên phải
        self.label_3 = QtWidgets.QLabel(self.widget)
        self.label_3.setGeometry(QtCore.QRect(300, 30, 250, 480))
        self.label_3.setStyleSheet("background-color: rgba(245, 245, 245, 255); border-top-right-radius: 60px; border-bottom-right-radius: 60px;")
        self.label_3.setText("")
        self.label_3.setObjectName("label_3")

        # Tiêu đề "Log In"
        self.label_4 = QtWidgets.QLabel(self.widget)
        self.label_4.setGeometry(QtCore.QRect(350, 80, 150, 50))
        font = QtGui.QFont("Segoe UI", 24)
        font.setBold(True)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgba(44, 62, 80, 220);")
        self.label_4.setText("Log In")
        self.label_4.setObjectName("label_4")

        # Hộp nhập User Name
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setGeometry(QtCore.QRect(320, 160, 200, 45))
        font = QtGui.QFont("Segoe UI", 11)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0);
            border: none;
            border-bottom: 2px solid rgba(52, 152, 219, 200);
            color: rgba(44, 62, 80, 240);
            padding-bottom: 8px;
        """)
        self.lineEdit.setPlaceholderText("User Name")
        self.lineEdit.setObjectName("lineEdit")

        # Hộp nhập Password
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setGeometry(QtCore.QRect(320, 230, 200, 45))
        font = QtGui.QFont("Segoe UI", 11)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0);
            border: none;
            border-bottom: 2px solid rgba(52, 152, 219, 200);
            color: rgba(44, 62, 80, 240);
            padding-bottom: 8px;
        """)
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setPlaceholderText("Password")
        self.lineEdit_2.setObjectName("lineEdit_2")

        # Nút Log In
        self.pushButton = QtWidgets.QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(320, 310, 200, 50))
        font = QtGui.QFont("Segoe UI", 12)
        font.setBold(True)
        self.pushButton.setFont(font)
        self.pushButton.setText("Log In")
        self.pushButton.setObjectName("pushButton")

        # Nhãn "Forgot your User Name or password?"
        self.label_5 = QtWidgets.QLabel(self.widget)
        self.label_5.setGeometry(QtCore.QRect(320, 370, 200, 20))
        font = QtGui.QFont("Segoe UI", 9)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgba(44, 62, 80, 180);")
        self.label_5.setText("Forgot your User Name or Password?")
        self.label_5.setObjectName("label_5")

        # Layout chứa các nút mạng xã hội
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.widget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(340, 410, 160, 40))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # Các nút mạng xã hội
        social_icons = {
            "pushButton_2": "🅵",  # Facebook
            "pushButton_3": "🆃",  # Twitter
            "pushButton_4": "🅸",  # Instagram
            "pushButton_5": "🅶"   # Google
        }
        for btn_id in ["pushButton_2", "pushButton_3", "pushButton_4", "pushButton_5"]:
            btn = QtWidgets.QPushButton(self.horizontalLayoutWidget)
            btn.setMaximumSize(QtCore.QSize(35, 35))
            font = QtGui.QFont("Segoe UI Emoji", 16)
            btn.setFont(font)
            btn.setText(social_icons[btn_id])
            btn.setObjectName(btn_id)
            self.horizontalLayout.addWidget(btn)

        # Nhãn nền mờ cho phần "Parking"
        self.label_6 = QtWidgets.QLabel(self.widget)
        self.label_6.setGeometry(QtCore.QRect(50, 90, 250, 150))
        self.label_6.setStyleSheet("background-color: rgba(0, 0, 0, 120); border-radius: 20px;")
        self.label_6.setText("")
        self.label_6.setObjectName("label_6")

        # Nhãn "Parking"
        self.label_7 = QtWidgets.QLabel(self.widget)
        self.label_7.setGeometry(QtCore.QRect(60, 100, 200, 50))
        font = QtGui.QFont("Segoe UI", 26)
        font.setBold(True)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: rgba(255, 255, 255, 220);")
        self.label_7.setText("Parking")
        self.label_7.setObjectName("label_7")

        # Nhãn "DEMO"
        self.label_8 = QtWidgets.QLabel(self.widget)
        self.label_8.setGeometry(QtCore.QRect(60, 160, 200, 40))
        font = QtGui.QFont("Segoe UI", 12)
        font.setBold(True)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: rgba(255, 255, 255, 180);")
        self.label_8.setText("DEMO")
        self.label_8.setObjectName("label_8")

        # Hiệu ứng bóng đổ
        for widget in [self.label, self.label_3, self.pushButton]:
            effect = QtWidgets.QGraphicsDropShadowEffect(blurRadius=30, xOffset=0 if widget != self.pushButton else 2, yOffset=0 if widget != self.pushButton else 2)
            widget.setGraphicsEffect(effect)

        QtCore.QMetaObject.connectSlotsByName(Form)