from PyQt5.QtWidgets import QWidget, QMessageBox
from DataAccess.dbcontext import DBContext
from DataAccess.Repository.manager import ManagerRepository
from Presentation.CameraManagement import CameraManagementView
from Presentation.Designer.Login import Ui_LoginView

class LoginView(QWidget, Ui_LoginView):
    def __init__(self):
        super().__init__()
        self.db_context = DBContext()
        self.manager_repo = ManagerRepository(self.db_context)
        self.setupUi(self)
        self.connect_signals()

    def connect_signals(self):
        """Kết nối các tín hiệu sự kiện"""
        self.pushButton.clicked.connect(lambda: self.handle_login(self))

    def open_camera_management(self, form, username):
        try:
            self.camera_management = CameraManagementView(manager_username=username)
            self.camera_management.show()
            form.close()
        except Exception as e:
            QMessageBox.critical(None, "Lỗi", f"Không thể mở Camera Management: {str(e)}")

    def handle_login(self, form):
        username = self.lineEdit.text().strip()
        password = self.lineEdit_2.text().strip()
        try:
            if not username or not password:
                raise ValueError("Tên đăng nhập và mật khẩu không được để trống!")
            manager = self.manager_repo.authenticate(username, password)
            if manager:
                QMessageBox.information(None, "Thông báo", "Đăng nhập thành công!")
                self.open_camera_management(form, username)
            else:
                QMessageBox.warning(None, "Lỗi", "Tài khoản hoặc mật khẩu sai!")
        except ValueError as e:
            QMessageBox.warning(None, "Lỗi", str(e))
        except Exception as e:
            QMessageBox.critical(None, "Lỗi", f"Lỗi hệ thống: {str(e)}")

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    login = LoginView()
    login.show()
    sys.exit(app.exec_())