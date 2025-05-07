# PointPicker.py
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
from DataAccess.Repository.CheckIn import CheckInRepository
from BusinessObject.models import Slot, CheckIn
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
        self.checkin_quads = {}  # {checkin_id: [QPoint, QPoint, QPoint, QPoint]}
        self.mode = None  # 'create', 'edit', 'add_checkin', 'edit_checkin'
        self.current_slot_id = None
        self.current_checkin_id = None
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
                        logging.debug(
                            f"Slot quadrilateral for slot {self.current_slot_id} completed and points cleared")
                elif self.mode in ['add_checkin', 'edit_checkin'] and self.current_checkin_id is not None:
                    self.points.append(pos)
                    logging.debug(f"Added point for checkin {self.current_checkin_id}: {pos.x()}, {pos.y()}")
                    if len(self.points) == 4:
                        self.checkin_quads[self.current_checkin_id] = self.points.copy()
                        self.points.clear()
                        logging.debug(
                            f"Check-in quadrilateral for checkin {self.current_checkin_id} completed and points cleared")
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

            # Draw slot quadrilaterals (red)
            pen = QPen(QtCore.Qt.red, 2)
            painter.setPen(pen)
            for slot_id, quad in self.slot_quads.items():
                if len(quad) == 4:
                    valid = True
                    for point in quad:
                        if not (0 <= point.x() <= 10000 and 0 <= point.y() <= 10000):
                            valid = False
                            logging.warning(f"Invalid point in slot_quads for slot {slot_id}: {point}")
                            break
                    if valid:
                        for i in range(4):
                            painter.drawLine(quad[i], quad[(i + 1) % 4])
                        painter.setPen(QPen(QtCore.Qt.black, 2))
                        painter.drawText(quad[0], f"Slot {slot_id}")
                        logging.debug(f"Drew slot quadrilateral for slot {slot_id}")

            # Draw check-in quadrilaterals (yellow)
            pen = QPen(QtCore.Qt.yellow, 2)
            painter.setPen(pen)
            for checkin_id, quad in self.checkin_quads.items():
                if len(quad) == 4:
                    valid = True
                    for point in quad:
                        if not (0 <= point.x() <= 10000 and 0 <= point.y() <= 10000):
                            valid = False
                            logging.warning(f"Invalid point in checkin_quads for checkin {checkin_id}: {point}")
                            break
                    if valid:
                        for i in range(4):
                            painter.drawLine(quad[i], quad[(i + 1) % 4])
                        painter.setPen(QPen(QtCore.Qt.black, 2))
                        painter.drawText(quad[0], f"CheckIn {checkin_id}")
                        logging.debug(f"Drew check-in quadrilateral for checkin {checkin_id}")

            # Draw current points (red for slots, yellow for check-ins)
            pen = QPen(QtCore.Qt.red if self.mode in ['create', 'edit'] else QtCore.Qt.yellow, 2)
            painter.setPen(pen)
            for point in self.points:
                if point and 0 <= point.x() <= 10000 and 0 <= point.y() <= 10000:
                    painter.drawEllipse(point, 5, 5)
                else:
                    logging.warning(f"Invalid point in paintEvent: {point}")

            painter.end()
            logging.debug("paintEvent completed")
        except Exception as e:
            logging.error(f"Error in paintEvent: {str(e)}")
            raise

    def set_mode(self, mode, slot_id=None, checkin_id=None):
        self.mode = mode
        self.current_slot_id = slot_id
        self.current_checkin_id = checkin_id
        self.points.clear()
        self.update()
        logging.debug(f"Set mode to: {mode}, slot_id: {slot_id}, checkin_id: {checkin_id}")

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

    def get_checkin_quads(self):
        logging.debug("get_checkin_quads called")
        try:
            return {k: [(p.x(), p.y()) for p in v] for k, v in self.checkin_quads.items()}
        except Exception as e:
            logging.error(f"Error in get_checkin_quads: {str(e)}")
            raise

    def load_slot_points(self, slots):
        logging.debug("load_slot_points called")
        try:
            self.slot_quads = {}
            for slot in slots:
                if all(getattr(slot, attr) is not None for attr in
                       ['d1x', 'd1y', 'd2x', 'd2y', 'd3x', 'd3y', 'd4x', 'd4y']):
                    self.slot_quads[slot.ID] = [
                        QPoint(slot.d1x, slot.d1y),
                        QPoint(slot.d2x, slot.d2y),
                        QPoint(slot.d3x, slot.d3y),
                        QPoint(slot.d4x, slot.d4y)
                    ]
                    logging.debug(
                        f"Loaded slot points for slot {slot.ID}: {[(p.x(), p.y()) for p in self.slot_quads[slot.ID]]}")
            self.update()
        except Exception as e:
            logging.error(f"Error in load_slot_points: {str(e)}")
            raise

    def load_checkin_points(self, checkins):
        logging.debug("load_checkin_points called")
        try:
            self.checkin_quads = {}
            for checkin in checkins:
                if all(getattr(checkin, attr) is not None for attr in
                       ['d1x', 'd1y', 'd2x', 'd2y', 'd3x', 'd3y', 'd4x', 'd4y']):
                    self.checkin_quads[checkin.ID] = [
                        QPoint(checkin.d1x, checkin.d1y),
                        QPoint(checkin.d2x, checkin.d2y),
                        QPoint(checkin.d3x, checkin.d3y),
                        QPoint(checkin.d4x, checkin.d4y)
                    ]
                    logging.debug(
                        f"Loaded check-in points for checkin {checkin.ID}: {[(p.x(), p.y()) for p in self.checkin_quads[checkin.ID]]}")
            self.update()
        except Exception as e:
            logging.error(f"Error in load_checkin_points: {str(e)}")
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
        self.checkin_repo = CheckInRepository(self.db_context)
        self.setupUi(self)
        self.image_label = ImageLabel()
        self.scroll_area.setWidget(self.image_label)

        # Kết nối các tín hiệu
        self.select_image_button.clicked.connect(self.select_image)
        self.create_button.clicked.connect(self.create_slot)
        self.delete_slot_button.clicked.connect(self.delete_slot)
        self.edit_slot_button.clicked.connect(self.edit_slot)
        self.save_button.clicked.connect(self.save_slots)
        self.add_checkin_button.clicked.connect(self.add_checkin)
        self.remove_checkin_button.clicked.connect(self.remove_checkin)
        self.edit_checkin_button.clicked.connect(self.edit_checkin)

        self.load_manager_data()

    def load_manager_data(self):
        logging.debug("load_manager_data called")
        logging.debug(f"Manager username: {self.manager_username}")
        try:
            manager = self.manager_repo.get_manager_by_username(self.manager_username)
            if manager:
                logging.debug(f"Found manager: {manager.UserName}")
                if manager.MainMap:
                    self.image_label.load_media(manager.MainMap)
                    self.val_link_label.setText(f"MainMap: {manager.MainMap}")
                else:
                    self.val_link_label.setText("MainMap: Not found")
                    logging.warning(f"Manager {self.manager_username} has no MainMap")
                    QMessageBox.warning(self, "Lỗi", "Manager không có MainMap!")
            else:
                logging.error(f"Manager {self.manager_username} not found in database")
                QMessageBox.critical(self, "Lỗi",
                                     f"Không tìm thấy Manager {self.manager_username} trong cơ sở dữ liệu!")

            # Load all slots
            slots = self.slot_repo.get_all_slots()
            self.image_label.load_slot_points(slots)
            self.slot_combo.clear()
            for slot in slots:
                self.slot_combo.addItem(f"Slot {slot.ID}", slot.ID)
                logging.debug(f"Added slot to combo box: {slot.ID}")

            # Load all check-ins
            checkins = self.checkin_repo.get_checkin_by_manager(self.manager_username)
            logging.debug(f"Retrieved check-ins: {len(checkins)} items")
            self.image_label.load_checkin_points(checkins)
            self.checkin_combo.clear()
            for checkin in checkins:
                self.checkin_combo.addItem(f"CheckIn {checkin.ID}", checkin.ID)
                logging.debug(f"Added check-in to combo box: {checkin.ID}")
            if not checkins:
                logging.warning(f"No check-ins found for manager {self.manager_username}")
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

                # Clear existing slots and check-ins display
                self.image_label.slot_quads.clear()
                self.image_label.checkin_quads.clear()
                self.image_label.points.clear()
                self.image_label.update()
                self.slot_combo.clear()
                self.checkin_combo.clear()
                logging.debug(f"Selected image: {file_path}")
        except Exception as e:
            logging.error(f"Error in select_image: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể tải ảnh: {str(e)}")

    def create_slot(self):
        logging.debug("create_slot called")
        try:
            slot_name, ok = QInputDialog.getText(self, "Tạo Slot", "Nhập tên Slot:")
            if not ok or not slot_name.strip():
                QMessageBox.warning(self, "Lỗi", "Tên Slot không được để trống!")
                return

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

    def add_checkin(self):
        logging.debug("add_checkin called")
        try:
            # Verify manager exists
            manager = self.manager_repo.get_manager_by_username(self.manager_username)
            if not manager:
                logging.error(f"Manager {self.manager_username} does not exist in the database")
                QMessageBox.critical(self, "Lỗi", f"Manager {self.manager_username} không tồn tại trong cơ sở dữ liệu!")
                return

            checkin_name, ok = QInputDialog.getText(self, "Tạo CheckIn", "Nhập tên CheckIn:")
            if not ok or not checkin_name.strip():
                QMessageBox.warning(self, "Lỗi", "Tên CheckIn không được để trống!")
                return

            new_checkin = CheckIn(
                Name=checkin_name.strip(),
                Manager_=self.manager_username,
                d1x=None, d1y=None, d2x=None, d2y=None,
                d3x=None, d3y=None, d4x=None, d4y=None
            )
            logging.debug(f"Created new CheckIn object: {new_checkin.Name}, Manager_: {new_checkin.Manager_}")
            added_checkin = self.checkin_repo.add_checkin(new_checkin)
            if added_checkin:
                QMessageBox.information(self, "Thành công", f"Đã tạo CheckIn với ID {added_checkin.ID}!")
                self.checkin_combo.addItem(f"CheckIn {added_checkin.ID}", added_checkin.ID)
                self.image_label.set_mode('add_checkin', checkin_id=added_checkin.ID)
                logging.debug(f"Created check-in {added_checkin.ID}, set mode to add_checkin")
            else:
                QMessageBox.critical(self, "Lỗi", "Không thể tạo CheckIn! Kiểm tra log để biết chi tiết.")
                logging.error("add_checkin failed, check database constraints or connection")
        except Exception as e:
            logging.error(f"Error in add_checkin: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể tạo CheckIn: {str(e)}")

    def remove_checkin(self):
        logging.debug("remove_checkin called")
        try:
            checkin_id = self.checkin_combo.currentData()
            if checkin_id is None:
                QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một CheckIn để xóa!")
                return

            reply = QMessageBox.question(
                self, "Xác nhận", f"Bạn có chắc muốn xóa CheckIn {checkin_id}?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                if checkin_id in self.image_label.checkin_quads:
                    del self.image_label.checkin_quads[checkin_id]
                success = self.checkin_repo.remove_checkin(checkin_id)
                if success:
                    QMessageBox.information(self, "Thành công", f"Đã xóa CheckIn {checkin_id}!")
                    self.checkin_combo.removeItem(self.checkin_combo.currentIndex())
                    self.image_label.update()
                    logging.debug(f"Deleted check-in {checkin_id}")
                else:
                    QMessageBox.warning(self, "Lỗi", f"Không tìm thấy CheckIn {checkin_id} để xóa!")
                    logging.warning(f"remove_checkin returned False for checkin_id {checkin_id}")
        except Exception as e:
            logging.error(f"Error in remove_checkin: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể xóa CheckIn: {str(e)}")

    def edit_checkin(self):
        logging.debug("edit_checkin called")
        try:
            checkin_id = self.checkin_combo.currentData()
            if checkin_id is None:
                QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một CheckIn để chỉnh sửa!")
                return
            self.image_label.set_mode('edit_checkin', checkin_id=checkin_id)
            logging.debug(f"Editing check-in {checkin_id}")
        except Exception as e:
            logging.error(f"Error in edit_checkin: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể chỉnh sửa check-in: {str(e)}")

    def save_slots(self):
        logging.debug("save_slots called")
        try:
            slot_quads = self.image_label.get_slot_quads()
            for slot_id, quad in slot_quads.items():
                if quad == [(0, 0)] * 4:
                    continue
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

            checkin_quads = self.image_label.get_checkin_quads()
            for checkin_id, quad in checkin_quads.items():
                if quad == [(0, 0)] * 4:
                    continue
                for x, y in quad:
                    if x < 0 or y < 0 or x > 10000 or y > 10000:
                        raise ValueError(f"Invalid coordinate in checkin {checkin_id}: ({x}, {y})")
                checkin = self.checkin_repo.get_checkin_by_id(checkin_id)
                if checkin:
                    checkin.d1x, checkin.d1y = quad[0]
                    checkin.d2x, checkin.d2y = quad[1]
                    checkin.d3x, checkin.d3y = quad[2]
                    checkin.d4x, checkin.d4y = quad[3]
                    success = self.checkin_repo.update_checkin(checkin)
                    if not success:
                        logging.warning(f"Failed to update checkin {checkin_id}")
                        QMessageBox.warning(self, "Lỗi", f"Không thể cập nhật CheckIn {checkin_id}!")
            QMessageBox.information(self, "Thành công", "Đã lưu tất cả slot và check-in!")
            logging.debug("Saved slots and check-ins successfully")
            self.accept()
        except ValueError as e:
            logging.error(f"Validation error in save_slots: {str(e)}")
            QMessageBox.warning(self, "Lỗi", str(e))
        except Exception as e:
            logging.error(f"Error in save_slots: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể lưu slot hoặc check-in: {str(e)}")

    def get_points(self):
        logging.debug("get_points called")
        try:
            return {
                'slots': self.image_label.get_slot_quads(),
                'checkins': self.image_label.get_checkin_quads()
            }
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