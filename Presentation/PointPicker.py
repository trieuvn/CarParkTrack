import sys
import logging
import warnings
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox, QInputDialog
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtCore import Qt, QPoint
from DataAccess.dbcontext import DBContext
from DataAccess.Repository.manager import ManagerRepository
from DataAccess.Repository.slot import SlotRepository
from BusinessObject.models import Slot
from Presentation.Designer.PointPicker import Ui_PointPickerView

# Bỏ qua cảnh báo DeprecationWarning liên quan đến sipPyTypeDict()
warnings.filterwarnings("ignore", category=DeprecationWarning, message="sipPyTypeDict*")

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class ImageLabel(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.points = []
        self.slot_quads = {}  # {slot_id: [QPoint, QPoint, QPoint, QPoint]}
        self.mode = None  # 'create' hoặc 'edit'
        self.current_slot_id = None
        self.current_media_path = ""
        self.original_size = QtCore.QSize(0, 0)
        self.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        logging.debug("ImageLabel initialized")

    def mousePressEvent(self, event):
        logging.debug("mousePressEvent triggered")
        try:
            if event.button() == QtCore.Qt.LeftButton:
                pos = event.pos()
                logging.debug(f"Clicked point: {pos.x()}, {pos.y()}")

                if pos.x() < 0 or pos.y() < 0 or pos.x() > 10000 or pos.y() > 10000:
                    logging.warning(f"Invalid point coordinates: {pos.x()}, {pos.y()}")
                    return

                if self.mode in ['create', 'edit'] and self.current_slot_id is not None:
                    self.points.append(pos)
                    logging.debug(f"Added point for slot {self.current_slot_id}: {pos.x()}, {pos.y()}")
                    if len(self.points) == 4:
                        self.slot_quads[self.current_slot_id] = self.points.copy()
                        self.points.clear()
                        logging.debug(f"Slot quadrilateral for slot {self.current_slot_id} completed and points cleared")
                    self.update()
                logging.debug("mousePressEvent completed")
        except Exception as e:
            logging.error(f"Error in mousePressEvent: {str(e)}")
            raise

    def paintEvent(self, event):
        logging.debug("paintEvent triggered")
        try:
            super().paintEvent(event)
            if not self.pixmap():
                logging.debug("No pixmap to paint, exiting paintEvent")
                return

            painter = QPainter(self)
            pen = QPen(QtCore.Qt.red, 2)
            painter.setPen(pen)

            for point in self.points:
                if point and 0 <= point.x() <= 10000 and 0 <= point.y() <= 10000:
                    painter.drawEllipse(point, 5, 5)
                else:
                    logging.warning(f"Invalid point in paintEvent: {point}")

            for slot_id, quad in self.slot_quads.items():
                if len(quad) == 4:
                    valid = True
                    for point in quad:
                        if not (0 <= point.x() <= 10000 and 0 <= point.y() <= 10000):
                            valid = False
                            logging.warning(f"Invalid point in slot_quads for slot {slot_id}: {point}")
                            break
                    if valid:
                        painter.setPen(QPen(QtCore.Qt.red, 2))
                        for i in range(4):
                            painter.drawLine(quad[i], quad[(i + 1) % 4])
                        # Hiển thị slot ID gần điểm đầu tiên
                        painter.setPen(QPen(QtCore.Qt.black, 2))
                        painter.drawText(quad[0], f"Slot {slot_id}")
                        logging.debug(f"Drew slot quadrilateral for slot {slot_id}")

            painter.end()
            logging.debug("paintEvent completed")
        except Exception as e:
            logging.error(f"Error in paintEvent: {str(e)}")
            raise

    def set_mode(self, mode, slot_id=None):
        self.mode = mode
        self.current_slot_id = slot_id
        self.points.clear()
        self.update()
        logging.debug(f"Set mode to: {mode}, slot_id: {slot_id}")

    def load_media(self, path):
        logging.debug(f"load_media called with path: {path}")
        try:
            self.current_media_path = path
            pixmap = QPixmap(path)
            if not pixmap.isNull():
                self.setPixmap(pixmap)
                self.original_size = pixmap.size()
                self.setFixedSize(self.original_size)
                self.update()
                logging.debug(f"Loaded image: {path}")
            else:
                logging.error("Failed to load image: Pixmap is null")
                QMessageBox.critical(self, "Lỗi", "Không thể tải MainMap!")
        except Exception as e:
            logging.error(f"Error in load_media: {str(e)}")
            raise

    def get_slot_quads(self):
        logging.debug("get_slot_quads called")
        try:
            return {k: [(p.x(), p.y()) for p in v] for k, v in self.slot_quads.items()}
        except Exception as e:
            logging.error(f"Error in get_slot_quads: {str(e)}")
            raise

    def load_slot_points(self, slots):
        logging.debug("load_slot_points called")
        try:
            self.slot_quads = {}
            for slot in slots:
                if all(getattr(slot, attr) is not None for attr in ['d1x', 'd1y', 'd2x', 'd2y', 'd3x', 'd3y', 'd4x', 'd4y']):
                    self.slot_quads[slot.ID] = [
                        QPoint(slot.d1x, slot.d1y),
                        QPoint(slot.d2x, slot.d2y),
                        QPoint(slot.d3x, slot.d3y),
                        QPoint(slot.d4x, slot.d4y)
                    ]
                    logging.debug(f"Loaded slot points for slot {slot.ID}: {[(p.x(), p.y()) for p in self.slot_quads[slot.ID]]}")
            self.update()
        except Exception as e:
            logging.error(f"Error in load_slot_points: {str(e)}")
            raise

class PointPickerView(QtWidgets.QDialog, Ui_PointPickerView):
    def __init__(self, manager_username: str):
        super().__init__()
        self.manager_username = manager_username
        if not isinstance(manager_username, str):
            logging.warning(f"manager_username should be a string, got {type(manager_username)}: {manager_username}")
            self.manager_username = str(manager_username)
        self.db_context = DBContext()
        self.manager_repo = ManagerRepository(self.db_context)
        self.slot_repo = SlotRepository(self.db_context)
        self.setupUi(self)
        self.image_label = ImageLabel()
        self.scroll_area.setWidget(self.image_label)

        # Kết nối các tín hiệu
        self.select_image_button.clicked.connect(self.select_image)
        self.create_button.clicked.connect(self.create_slot)
        self.delete_slot_button.clicked.connect(self.delete_slot)
        self.edit_slot_button.clicked.connect(self.edit_slot)
        self.save_button.clicked.connect(self.save_slots)

        self.load_manager_data()

    def load_manager_data(self):
        logging.debug("load_manager_data called")
        logging.debug(f"Manager username: {self.manager_username}")
        try:
            manager = self.manager_repo.get_manager_by_username(self.manager_username)
            if manager and manager.MainMap:
                self.image_label.load_media(manager.MainMap)
                self.val_link_label.setText(f"MainMap: {manager.MainMap}")
            else:
                self.val_link_label.setText("MainMap: Not found")
                logging.warning(f"Manager {self.manager_username} has no MainMap")
                QMessageBox.warning(self, "Lỗi", "Manager không có MainMap!")

            # Load all slots
            slots = self.slot_repo.get_all_slots()
            self.image_label.load_slot_points(slots)
            self.slot_combo.clear()
            for slot in slots:
                self.slot_combo.addItem(f"Slot {slot.ID}", slot.ID)
                logging.debug(f"Added slot to combo box: {slot.ID}")
            logging.debug("Loaded manager data successfully")
        except Exception as e:
            logging.error(f"Error in load_manager_data: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể tải dữ liệu: {str(e)}")

    def select_image(self):
        logging.debug("select_image called")
        try:
            file_path, _ = QFileDialog.getOpenFileName(self, "Chọn hình ảnh", "", "Image Files (*.png *.jpg *.bmp)")
            if file_path:
                self.image_label.load_media(file_path)
                self.val_link_label.setText(f"MainMap: {file_path}")

                # Update MainMap của Manager
                manager = self.manager_repo.get_manager_by_username(self.manager_username)
                if manager:
                    manager.MainMap = file_path
                    self.manager_repo.update_manager(manager)
                    logging.debug(f"Updated MainMap for manager {self.manager_username}: {file_path}")
                else:
                    logging.warning(f"Manager {self.manager_username} not found")
                    QMessageBox.warning(self, "Lỗi", "Không tìm thấy Manager!")

                # Clear existing slots display
                self.image_label.slot_quads.clear()
                self.image_label.points.clear()
                self.image_label.update()
                self.slot_combo.clear()
                logging.debug(f"Selected image: {file_path}")
        except Exception as e:
            logging.error(f"Error in select_image: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể tải ảnh: {str(e)}")

    def create_slot(self):
        logging.debug("create_slot called")
        try:
            # Yêu cầu người dùng nhập tên slot
            slot_name, ok = QInputDialog.getText(self, "Tạo Slot", "Nhập tên Slot:")
            if not ok or not slot_name.strip():
                QMessageBox.warning(self, "Lỗi", "Tên Slot không được để trống!")
                return

            # Tạo slot mới
            new_slot = Slot(
                Name=slot_name.strip(),
                Manager_=self.manager_username,
                d1x=None, d1y=None, d2x=None, d2y=None,
                d3x=None, d3y=None, d4x=None, d4y=None
            )
            added_slot = self.slot_repo.add_slot(new_slot)
            if added_slot:
                QMessageBox.information(self, "Thành công", f"Đã tạo Slot với ID {added_slot.ID}!")
                self.slot_combo.addItem(f"Slot {added_slot.ID}", added_slot.ID)
                self.image_label.set_mode('create', added_slot.ID)
                logging.debug(f"Created slot {added_slot.ID}, set mode to create")
            else:
                QMessageBox.critical(self, "Lỗi", "Không thể tạo Slot!")
        except Exception as e:
            logging.error(f"Error in create_slot: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể tạo Slot: {str(e)}")

    def delete_slot(self):
        logging.debug("delete_slot called")
        try:
            slot_id = self.slot_combo.currentData()
            if slot_id is None:
                QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một slot để xóa!")
                return

            reply = QMessageBox.question(
                self, "Xác nhận", f"Bạn có chắc muốn xóa Slot {slot_id}?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                if slot_id in self.image_label.slot_quads:
                    del self.image_label.slot_quads[slot_id]
                # Sử dụng phương thức delete_slot_by_id
                success = self.slot_repo.delete_slot_by_id(slot_id)
                if success:
                    QMessageBox.information(self, "Thành công", f"Đã xóa Slot {slot_id}!")
                    self.slot_combo.removeItem(self.slot_combo.currentIndex())
                    self.image_label.update()
                    logging.debug(f"Deleted slot {slot_id}")
                else:
                    QMessageBox.warning(self, "Lỗi", f"Không tìm thấy Slot {slot_id} để xóa!")
        except Exception as e:
            logging.error(f"Error in delete_slot: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể xóa Slot: {str(e)}")

    def edit_slot(self):
        logging.debug("edit_slot called")
        try:
            slot_id = self.slot_combo.currentData()
            if slot_id is None:
                QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một slot để chỉnh sửa!")
                return
            self.image_label.set_mode('edit', slot_id)
            logging.debug(f"Editing slot {slot_id}")
        except Exception as e:
            logging.error(f"Error in edit_slot: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể chỉnh sửa slot: {str(e)}")

    def save_slots(self):
        logging.debug("save_slots called")
        try:
            slot_quads = self.image_label.get_slot_quads()
            for slot_id, quad in slot_quads.items():
                if quad == [(0, 0)] * 4:
                    continue
                # Kiểm tra tọa độ hợp lệ trước khi lưu
                for x, y in quad:
                    if x < 0 or y < 0 or x > 10000 or y > 10000:
                        raise ValueError(f"Invalid coordinate in slot {slot_id}: ({x}, {y})")
                success = self.slot_repo.update_slot_box(slot_id,
                    quad[0][0], quad[0][1],
                    quad[1][0], quad[1][1],
                    quad[2][0], quad[2][1],
                    quad[3][0], quad[3][1]
                )
                if not success:
                    logging.warning(f"Failed to update slot {slot_id}")
                    QMessageBox.warning(self, "Lỗi", f"Không thể cập nhật Slot {slot_id}!")
            QMessageBox.information(self, "Thành công", "Đã lưu tất cả slot!")
            logging.debug("Saved slots successfully")
            self.accept()
        except ValueError as e:
            logging.error(f"Validation error in save_slots: {str(e)}")
            QMessageBox.warning(self, "Lỗi", str(e))
        except Exception as e:
            logging.error(f"Error in save_slots: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể lưu slot: {str(e)}")

    def get_points(self):
        logging.debug("get_points called")
        try:
            return self.image_label.get_slot_quads()
        except Exception as e:
            logging.error(f"Error in get_points: {str(e)}")
            raise

    def closeEvent(self, event):
        logging.debug("closeEvent called")
        try:
            super().closeEvent(event)
            logging.debug("Dialog closed")
        except Exception as e:
            logging.error(f"Error in closeEvent: {str(e)}")
            raise

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = PointPickerView(manager_username="admin")
    dialog.exec_()
    sys.exit(app.exec_())