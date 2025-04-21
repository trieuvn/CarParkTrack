from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget, QStackedWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    "------------------------------------------------------------------------------------"

    def toggle_groupbox(self):
        if self.pushButton_6.isChecked() and self.car_btn.isChecked():
            self.groupBox.setVisible(True)
            self.play_video()
        else:
            self.groupBox.setVisible(False)
            self.mediaPlayer.stop()

    def play_video(self):
        video_path = r"test/Mechanics/car1.mp4"
        self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(video_path)))
        self.mediaPlayer.play()

    "------------------------------------------------------------------------------------"

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 502)
        MainWindow.setStyleSheet("/* Style for first menu widget  */\n"
                                 "#main_menu_widget {\n"
                                 "    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 rgba(188, 231, 215, 255), stop:1 rgba(122, 215, 255, 255));\n"
                                 "    border-top: 1px solid #434343;\n"
                                 "}\n"
                                 "\n"
                                 "#main_menu_widget QPushButton {\n"
                                 "    border: none;\n"
                                 "    padding-left: 15px;\n"
                                 "    padding-right: 15px;\n"
                                 "}\n"
                                 "\n"
                                 "#main_menu_widget QPushButton:hover {\n"
                                 "    color: #0946F7\n"
                                 "}\n"
                                 "\n"
                                 "#main_menu_widget QPushButton:checked {\n"
                                 "    padding-top: 5px;\n"
                                 "    border-bottom: 5px solid rgb(67, 67, 67)\n"
                                 "}\n"
                                 "\n"
                                 "/* Style for second menu widget  */\n"
                                 "#second_menu_widget  {\n"
                                 "    background-color: rgb(67, 67, 67);\n"
                                 "}\n"
                                 "\n"
                                 "#second_menu_widget QPushButton  {\n"
                                 "    border: none;\n"
                                 "   color: #fff;\n"
                                 "}\n"
                                 "\n"
                                 "#second_menu_widget QPushButton:hover  {\n"
                                 "    color: #EDBB99;\n"
                                 "}\n"
                                 "\n"
                                 "#second_menu_widget QPushButton:checked  {\n"
                                 "    color: rgb(255, 186, 74);\n"
                                 "}\n"
                                 "\n"
                                 "/* Style for search widget  */\n"
                                 "#search_widget QLineEdit {\n"
                                 "    border-radius: 2px;\n"
                                 "    padding-left: 5px;\n"
                                 "}\n"
                                 "\n"
                                 "#search_widget QPushButton {\n"
                                 "    border-radius: 2px;\n"
                                 "    background-color: #fff;\n"
                                 "    border: 1px solid #f0f0f0;\n"
                                 "}\n"
                                 "\n"
                                 "#search_widget QPushButton:pressed {\n"
                                 "    padding-left:5px;\n"
                                 "}\n"
                                 "\n"
                                 "/* Style for main widget  */\n"
                                 "#main_widget {\n"
                                 "    border-left: 5px solid #434343;\n"
                                 "    border-right: 5px solid #434343;\n"
                                 "    border-bottom: 5px solid #434343;\n"
                                 "}\n"
                                 "\n"
                                 "")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.main_widget = QtWidgets.QWidget(self.centralwidget)
        self.main_widget.setStyleSheet("")
        self.main_widget.setObjectName("main_widget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.main_widget)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setSpacing(0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.stackedWidget = QtWidgets.QStackedWidget(self.main_widget)
        self.stackedWidget.setAcceptDrops(False)
        self.stackedWidget.setStyleSheet("")
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_8 = QtWidgets.QWidget()
        self.page_8.setObjectName("page_8")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.page_8)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.groupBox = QtWidgets.QGroupBox(self.page_8)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_11.addWidget(self.groupBox, 0, 1, 1, 1)
        self.stackedWidget.addWidget(self.page_8)
        self.gridLayout_4.addWidget(self.stackedWidget, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.main_widget, 1, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.main_menu_widget = QtWidgets.QWidget(self.centralwidget)
        self.main_menu_widget.setMinimumSize(QtCore.QSize(0, 30))
        self.main_menu_widget.setMaximumSize(QtCore.QSize(16777215, 40))
        self.main_menu_widget.setStyleSheet("")
        self.main_menu_widget.setObjectName("main_menu_widget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.main_menu_widget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 15, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.home_btn = QtWidgets.QPushButton(self.main_menu_widget)
        self.home_btn.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.home_btn.setFont(font)
        self.home_btn.setStyleSheet("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/icon/home-4-48.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.home_btn.setIcon(icon)
        self.home_btn.setIconSize(QtCore.QSize(12, 12))
        self.home_btn.setCheckable(True)
        self.home_btn.setChecked(True)
        self.home_btn.setAutoExclusive(True)
        self.home_btn.setObjectName("home_btn")
        self.horizontalLayout_2.addWidget(self.home_btn)
        self.car_btn = QtWidgets.QPushButton(self.main_menu_widget)
        self.car_btn.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.car_btn.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/icon/car-4-64.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.car_btn.setIcon(icon1)
        self.car_btn.setIconSize(QtCore.QSize(12, 12))
        self.car_btn.setCheckable(True)
        self.car_btn.setAutoExclusive(True)
        self.car_btn.setObjectName("car_btn")
        self.horizontalLayout_2.addWidget(self.car_btn)
        self.social_btn = QtWidgets.QPushButton(self.main_menu_widget)
        self.social_btn.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.social_btn.setFont(font)
        self.social_btn.setStyleSheet("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/icon/group-64.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.social_btn.setIcon(icon2)
        self.social_btn.setIconSize(QtCore.QSize(12, 12))
        self.social_btn.setCheckable(True)
        self.social_btn.setAutoExclusive(True)
        self.social_btn.setObjectName("social_btn")
        self.horizontalLayout_2.addWidget(self.social_btn)
        self.search_btn = QtWidgets.QPushButton(self.main_menu_widget)
        self.search_btn.setMinimumSize(QtCore.QSize(0, 30))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.search_btn.setFont(font)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icon/icon/search-3-48.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.search_btn.setIcon(icon3)
        self.search_btn.setIconSize(QtCore.QSize(12, 12))
        self.search_btn.setCheckable(True)
        self.search_btn.setAutoExclusive(True)
        self.search_btn.setObjectName("search_btn")
        self.horizontalLayout_2.addWidget(self.search_btn)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.user_logo = QtWidgets.QLabel(self.main_menu_widget)
        self.user_logo.setMinimumSize(QtCore.QSize(20, 20))
        self.user_logo.setMaximumSize(QtCore.QSize(20, 20))
        self.user_logo.setText("")
        self.user_logo.setPixmap(QtGui.QPixmap(":/icon/icon/user-48.ico"))
        self.user_logo.setScaledContents(True)
        self.user_logo.setObjectName("user_logo")
        self.horizontalLayout_2.addWidget(self.user_logo)
        self.verticalLayout.addWidget(self.main_menu_widget)
        self.second_menu_widget = QtWidgets.QWidget(self.centralwidget)
        self.second_menu_widget.setMinimumSize(QtCore.QSize(0, 30))
        self.second_menu_widget.setMaximumSize(QtCore.QSize(16777215, 30))
        self.second_menu_widget.setStyleSheet("")
        self.second_menu_widget.setObjectName("second_menu_widget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.second_menu_widget)
        self.horizontalLayout_3.setContentsMargins(15, 0, 15, 0)
        self.horizontalLayout_3.setSpacing(25)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.home_widget = QtWidgets.QWidget(self.second_menu_widget)
        self.home_widget.setObjectName("home_widget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.home_widget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton_5 = QtWidgets.QPushButton(self.home_widget)
        self.pushButton_5.setCheckable(True)
        self.pushButton_5.setChecked(True)
        self.pushButton_5.setAutoExclusive(True)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_4.addWidget(self.pushButton_5)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem1)
        self.horizontalLayout_3.addWidget(self.home_widget)
        self.car_widget = QtWidgets.QWidget(self.second_menu_widget)
        self.car_widget.setObjectName("car_widget")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.car_widget)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(25)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.car_widget)
        self.pushButton_6.setCheckable(True)
        self.pushButton_6.setChecked(True)
        self.pushButton_6.setAutoExclusive(True)
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_5.addWidget(self.pushButton_6)
        self.pushButton_7 = QtWidgets.QPushButton(self.car_widget)
        self.pushButton_7.setCheckable(True)
        self.pushButton_7.setAutoExclusive(True)
        self.pushButton_7.setObjectName("pushButton_7")
        self.horizontalLayout_5.addWidget(self.pushButton_7)
        self.pushButton_8 = QtWidgets.QPushButton(self.car_widget)
        self.pushButton_8.setCheckable(True)
        self.pushButton_8.setAutoExclusive(True)
        self.pushButton_8.setObjectName("pushButton_8")
        self.horizontalLayout_5.addWidget(self.pushButton_8)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem2)
        self.horizontalLayout_3.addWidget(self.car_widget)
        self.socail_widget = QtWidgets.QWidget(self.second_menu_widget)
        self.socail_widget.setObjectName("socail_widget")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.socail_widget)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setSpacing(25)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.pushButton_10 = QtWidgets.QPushButton(self.socail_widget)
        self.pushButton_10.setCheckable(True)
        self.pushButton_10.setChecked(True)
        self.pushButton_10.setAutoExclusive(True)
        self.pushButton_10.setObjectName("pushButton_10")
        self.horizontalLayout_6.addWidget(self.pushButton_10)
        self.pushButton_11 = QtWidgets.QPushButton(self.socail_widget)
        self.pushButton_11.setCheckable(True)
        self.pushButton_11.setAutoExclusive(True)
        self.pushButton_11.setObjectName("pushButton_11")
        self.horizontalLayout_6.addWidget(self.pushButton_11)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem3)
        self.horizontalLayout_3.addWidget(self.socail_widget)
        self.search_widget = QtWidgets.QWidget(self.second_menu_widget)
        self.search_widget.setObjectName("search_widget")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.search_widget)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setSpacing(5)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem4)
        self.lineEdit = QtWidgets.QLineEdit(self.search_widget)
        self.lineEdit.setMinimumSize(QtCore.QSize(150, 0))
        self.lineEdit.setMaximumSize(QtCore.QSize(150, 16777215))
        self.lineEdit.setStyleSheet("")
        self.lineEdit.setClearButtonEnabled(True)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_8.addWidget(self.lineEdit)
        self.pushButton_13 = QtWidgets.QPushButton(self.search_widget)
        self.pushButton_13.setMinimumSize(QtCore.QSize(25, 18))
        self.pushButton_13.setMaximumSize(QtCore.QSize(25, 18))
        self.pushButton_13.setStyleSheet("")
        self.pushButton_13.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/blueIcons/search.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_13.setIcon(icon4)
        self.pushButton_13.setIconSize(QtCore.QSize(12, 12))
        self.pushButton_13.setObjectName("pushButton_13")
        self.horizontalLayout_8.addWidget(self.pushButton_13)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem5)
        self.horizontalLayout_3.addWidget(self.search_widget)
        self.verticalLayout.addWidget(self.second_menu_widget)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        self.car_btn.toggled['bool'].connect(self.car_widget.setVisible)  # type: ignore
        self.car_btn.toggled['bool'].connect(self.home_widget.setHidden)  # type: ignore
        self.car_btn.toggled['bool'].connect(self.socail_widget.setHidden)  # type: ignore
        self.home_btn.toggled['bool'].connect(self.socail_widget.setHidden)  # type: ignore
        self.home_btn.toggled['bool'].connect(self.home_widget.setVisible)  # type: ignore
        self.home_btn.toggled['bool'].connect(self.car_widget.setHidden)  # type: ignore
        self.search_btn.toggled['bool'].connect(self.search_widget.setVisible)  # type: ignore
        self.search_btn.toggled['bool'].connect(self.socail_widget.setHidden)  # type: ignore
        self.search_btn.toggled['bool'].connect(self.car_widget.setHidden)  # type: ignore
        self.search_btn.toggled['bool'].connect(self.home_widget.setHidden)  # type: ignore
        self.home_btn.toggled['bool'].connect(self.search_widget.setHidden)  # type: ignore
        self.car_btn.toggled['bool'].connect(self.search_widget.setHidden)  # type: ignore
        self.social_btn.toggled['bool'].connect(self.socail_widget.setVisible)  # type: ignore
        self.social_btn.toggled['bool'].connect(self.home_widget.setHidden)  # type: ignore
        self.social_btn.toggled['bool'].connect(self.car_widget.setHidden)  # type: ignore
        self.social_btn.toggled['bool'].connect(self.search_widget.setHidden)  # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.home_btn.setText(_translate("MainWindow", "Home"))
        self.car_btn.setText(_translate("MainWindow", "Camera"))
        self.social_btn.setText(_translate("MainWindow", "Social Media"))
        self.search_btn.setText(_translate("MainWindow", "Search"))
        self.pushButton_5.setText(_translate("MainWindow", "Dashboard"))
        self.pushButton_6.setText(_translate("MainWindow", "Camera 1"))
        self.pushButton_7.setText(_translate("MainWindow", "Camera 2"))
        self.pushButton_8.setText(_translate("MainWindow", "Camera 3"))
        self.pushButton_10.setText(_translate("MainWindow", "Website"))
        self.pushButton_11.setText(_translate("MainWindow", "Facebook"))
        "------------------------------------------------------------------------------------"
        'Create a video widget'
        self.videoWidget = QVideoWidget(self.groupBox)
        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.setVideoOutput(self.videoWidget)
        layout = QVBoxLayout()
        layout.addWidget(self.videoWidget)
        self.groupBox.setLayout(layout)
        'Create a button to play video'
        self.pushButton_6.clicked.connect(self.toggle_groupbox)
        self.pushButton_7.clicked.connect(self.toggle_groupbox)
        self.pushButton_8.clicked.connect(self.toggle_groupbox)
        self.car_btn.clicked.connect(self.toggle_groupbox)
        self.pushButton_10.clicked.connect(self.toggle_groupbox)
        self.pushButton_11.clicked.connect(self.toggle_groupbox)
        self.social_btn.clicked.connect(self.toggle_groupbox)
        self.search_btn.clicked.connect(self.toggle_groupbox)
        self.home_btn.clicked.connect(self.toggle_groupbox)
        self.pushButton_5.clicked.connect(self.toggle_groupbox)
        "------------------------------------------------------------------------------------"


#import res

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())