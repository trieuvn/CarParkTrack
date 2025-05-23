from PyQt5.QtWidgets import QMainWindow, QMessageBox
from DataAccess.dbcontext import DBContext
from DataAccess.Repository.manager import ManagerRepository
from Presentation.CameraManagement import CameraManagementView
from Presentation.Designer.Login import Ui_LoginView

class LoginView(QMainWindow, Ui_LoginView):
    def __init__(self):
        super().__init__()
        try:
            self.db_context = DBContext()
            self.manager_repo = ManagerRepository(self.db_context)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể kết nối đến cơ sở dữ liệu: {str(e)}")
            return
        self.setupUi(self)
        self.connect_signals()

    def connect_signals(self):
        """Kết nối các tín hiệu sự kiện"""
        self.pushButton.clicked.connect(self.handle_login)

    def open_camera_management(self, username):
        try:
            self.camera_management = CameraManagementView(manager_username=username)
            self.camera_management.show()
            self.close()  # Đóng cửa sổ login
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể mở Camera Management: {str(e)}")

    def handle_login(self):
        username = self.lineEdit.text().strip()
        password = self.lineEdit_2.text().strip()
        try:
            if not username or not password:
                raise ValueError("Tên đăng nhập và mật khẩu không được để trống!")
            manager = self.manager_repo.authenticate(username, password)
            if manager:
                QMessageBox.information(self, "Thông báo", "Đăng nhập thành công!")
                self.open_camera_management(username)
            else:
                QMessageBox.warning(self, "Lỗi", "Tài khoản hoặc mật khẩu sai!")
        except ValueError as e:
            QMessageBox.warning(self, "Lỗi", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi hệ thống: {str(e)}")

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    login = LoginView()
    login.showMaximized()
    sys.exit(app.exec_())