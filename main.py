# main.py
from PyQt5 import QtWidgets
import sys
from Presentation.Login import LoginView

def main():
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    login = LoginView()
    login.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()