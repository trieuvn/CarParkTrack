import sys
import logging
import cv2
import warnings
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QPainter, QPen, QImage
from PyQt5.QtCore import Qt, QPoint, QTimer
from DataAccess.dbcontext import DBContext
from DataAccess.Repository.camera import CameraRepository
from DataAccess.Repository.CameraHaveSlot import CameraHaveSlotRepository
from BusinessObject.models import CameraHaveSlot
from Presentation.Designer.PointPicker import Ui_PointPickerView

# Bỏ qua cảnh báo DeprecationWarning liên quan đến sipPyTypeDict()
warnings.filterwarnings("ignore", category=DeprecationWarning, message="sipPyTypeDict*")

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class ImageLabel(QtWidgets.QLabel):
    def __init__(self):
        super().__init__()
        self.points = []
        self.check_in_quad = None
        self.slot_quads = {}
        self.mode = None
        self.current_slot_id = None
        self.delete_mode = False
        self.current_media_path = ""
        self.is_video = False
        self.video_capture = None
        self.current_frame = None
        self.frame_count = 0
        self.current_frame_pos = 0
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

                if self.delete_mode:
                    logging.debug("Delete mode active")
                    if self.mode == 'check_in' and self.check_in_quad and self.is_point_inside_quad(pos, self.check_in_quad):
                        self.check_in_quad = None
                        logging.debug("Removed check-in quadrilateral")
                    elif self.mode == 'slot' and self.current_slot_id in self.slot_quads:
                        if self.is_point_inside_quad(pos, self.slot_quads[self.current_slot_id]):
                            del self.slot_quads[self.current_slot_id]
                            logging.debug(f"Removed slot quadrilateral for slot {self.current_slot_id}")
                    self.update()
                else:
                    if self.mode == 'check_in':
                        self.points.append(pos)
                        logging.debug(f"Added point for check-in: {pos.x()}, {pos.y()}")
                        if len(self.points) == 4:
                            self.check_in_quad = self.points.copy()
                            self.points.clear()
                            logging.debug("Check-in quadrilateral completed and points cleared")
                    elif self.mode == 'slot' and self.current_slot_id:
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

            if self.check_in_quad and len(self.check_in_quad) == 4:
                valid = True
                for point in self.check_in_quad:
                    if not (0 <= point.x() <= 10000 and 0 <= point.y() <= 10000):
                        valid = False
                        logging.warning(f"Invalid point in check_in_quad: {point}")
                        break
                if valid:
                    painter.setPen(QPen(QtCore.Qt.yellow, 2))
                    for i in range(4):
                        painter.drawLine(self.check_in_quad[i], self.check_in_quad[(i + 1) % 4])
                    logging.debug("Drew check-in quadrilateral")

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
                        logging.debug(f"Drew slot quadrilateral for slot {slot_id}")

            painter.end()
            logging.debug("paintEvent completed")
        except Exception as e:
            logging.error(f"Error in paintEvent: {str(e)}")
            raise

    def is_point_inside_quad(self, point, quad):
        logging.debug(f"isPointInsideQuad called with point: {point}, quad: {quad}")
        try:
            if len(quad) != 4:
                logging.warning("Quad does not have 4 points")
                return False
            intersections = 0
            for i in range(4):
                p1 = quad[i]
                p2 = quad[(i + 1) % 4]
                if self.ray_intersects_segment(point, p1, p2):
                    intersections += 1
            result = intersections % 2 == 1
            logging.debug(f"isPointInsideQuad result: {result}")
            return result
        except Exception as e:
            logging.error(f"Error in isPointInsideQuad: {str(e)}")
            raise

    def ray_intersects_segment(self, point, p1, p2):
        logging.debug(f"rayIntersectsSegment called with point: {point}, p1: {p1}, p2: {p2}")
        try:
            if p1.y() > p2.y():
                p1, p2 = p2, p1
            if point.y() == p1.y() or point.y() == p2.y():
                point = QPoint(point.x(), point.y() + 1)
            if (point.y() < p1.y() or point.y() > p2.y() or
                    point.x() > max(p1.x(), p2.x())):
                return False
            if point.x() < min(p1.x(), p2.x()):
                return True
            if p2.y() == p1.y():
                return False
            slope = (p2.x() - p1.x()) / (p2.y() - p1.y())
            intersect_x = p1.x() + (point.y() - p1.y()) * slope
            result = point.x() < intersect_x
            logging.debug(f"rayIntersectsSegment result: {result}")
            return result
        except Exception as e:
            logging.error(f"Error in rayIntersectsSegment: {str(e)}")
            raise

    def set_mode(self, mode, slot_id=None):
        self.mode = mode
        self.current_slot_id = slot_id
        self.points.clear()
        self.update()
        logging.debug(f"Set mode to: {mode}, slot_id: {slot_id}")

    def set_delete_mode(self, enabled):
        self.delete_mode = enabled
        self.points.clear()
        self.update()
        logging.debug(f"Delete mode set to: {enabled}")

    def load_media(self, path, is_video=False):
        logging.debug(f"load_media called with path: {path}, is_video: {is_video}")
        try:
            self.current_media_path = path
            self.is_video = is_video
            if is_video:
                self.open_video_capture(path)
            else:
                pixmap = QPixmap(path)
                if not pixmap.isNull():
                    self.setPixmap(pixmap)
                    self.original_size = pixmap.size()
                    self.setFixedSize(self.original_size)
                    self.update()
                    logging.debug(f"Loaded image: {path}")
                else:
                    logging.error("Failed to load image: Pixmap is null")
                    QMessageBox.critical(self, "Lỗi", "Không thể tải ảnh!")
        except Exception as e:
            logging.error(f"Error in load_media: {str(e)}")
            raise

    def open_video_capture(self, video_path):
        logging.debug(f"open_video_capture called with video_path: {video_path}")
        try:
            if self.video_capture:
                self.video_capture.release()
            self.video_capture = cv2.VideoCapture(video_path)
            if not self.video_capture.isOpened():
                logging.error("Failed to open video")
                QMessageBox.critical(self, "Lỗi", "Không thể mở video!")
                self.video_capture = None
                self.is_video = False
                return
            # Kiểm tra khung hình đầu tiên
            ret, frame = self.video_capture.read()
            if not ret or frame is None:
                logging.error(f"Invalid video: Unable to read first frame from {video_path}")
                QMessageBox.critical(self, "Lỗi", "Video không hợp lệ hoặc bị hỏng!")
                self.video_capture.release()
                self.video_capture = None
                self.is_video = False
                return
            logging.debug(f"First frame shape: {frame.shape}")
            self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Đặt lại về khung đầu tiên
            self.frame_count = int(self.video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
            self.current_frame_pos = 0
            self.read_frame(0)
            logging.debug(f"Opened video: {video_path}, frame count: {self.frame_count}")
        except Exception as e:
            logging.error(f"Error in open_video_capture: {str(e)}")
            raise

    def read_frame(self, frame_position):
        logging.debug(f"read_frame called with frame_position: {frame_position}")
        try:
            if self.video_capture and self.is_video:
                self.video_capture.set(cv2.CAP_PROP_POS_FRAMES, frame_position)
                ret, frame = self.video_capture.read()
                if ret:
                    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    height, width, channels = rgb_frame.shape
                    bytes_per_line = channels * width
                    q_img = QImage(rgb_frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
                    pixmap = QPixmap.fromImage(q_img)
                    self.original_size = QtCore.QSize(width, height)
                    self.setPixmap(pixmap)
                    self.setFixedSize(self.original_size)
                    self.update()
                    logging.debug(f"Displayed frame: {frame_position}")
                    return True
                else:
                    logging.warning("Failed to read frame")
                    return False
            return False
        except Exception as e:
            logging.error(f"Error in read_frame: {str(e)}")
            raise

    def close_video(self):
        if self.video_capture:
            self.video_capture.release()
            self.video_capture = None
            self.is_video = False
            logging.debug("Closed video capture")

    def get_points(self):
        logging.debug("get_points called")
        try:
            return {
                'check_in_quad': [(p.x(), p.y()) for p in self.check_in_quad] if self.check_in_quad else [(0, 0)] * 4,
                'slot_quads': {k: [(p.x(), p.y()) for p in v] for k, v in self.slot_quads.items()}
            }
        except Exception as e:
            logging.error(f"Error in get_points: {str(e)}")
            raise

    def load_camera_points(self, camera):
        logging.debug("load_camera_points called")
        try:
            if camera and all(getattr(camera, attr) is not None for attr in ['d1x', 'd1y', 'd2x', 'd2y', 'd3x', 'd3y', 'd4x', 'd4y']):
                self.check_in_quad = [
                    QPoint(camera.d1x, camera.d1y),
                    QPoint(camera.d2x, camera.d2y),
                    QPoint(camera.d3x, camera.d3y),
                    QPoint(camera.d4x, camera.d4y)
                ]
                logging.debug(f"Loaded check-in points from camera: {[(p.x(), p.y()) for p in self.check_in_quad]}")
            else:
                self.check_in_quad = None
                logging.debug("No valid check-in points to load from camera")
            self.update()
        except Exception as e:
            logging.error(f"Error in load_camera_points: {str(e)}")
            raise

    def load_slot_points(self, camera_have_slots):
        logging.debug("load_slot_points called")
        try:
            self.slot_quads = {}
            for chs in camera_have_slots:
                if all(getattr(chs, attr) is not None for attr in ['d1x', 'd1y', 'd2x', 'd2y', 'd3x', 'd3y', 'd4x', 'd4y']):
                    self.slot_quads[chs.Slot_] = [
                        QPoint(chs.d1x, chs.d1y),
                        QPoint(chs.d2x, chs.d2y),
                        QPoint(chs.d3x, chs.d3y),
                        QPoint(chs.d4x, chs.d4y)
                    ]
                    logging.debug(f"Loaded slot points for slot {chs.Slot_}: {[(p.x(), p.y()) for p in self.slot_quads[chs.Slot_]]}")
            self.update()
        except Exception as e:
            logging.error(f"Error in load_slot_points: {str(e)}")
            raise

class PointPickerView(QtWidgets.QDialog, Ui_PointPickerView):
    def __init__(self, camera_id: int):
        super().__init__()
        self.camera_id = camera_id
        self.setupUi(self)
        self.image_label = ImageLabel()
        self.scroll_area.setWidget(self.image_label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.read_frame)

        self.slider.valueChanged.connect(self.slider_moved)
        self.select_image_button.clicked.connect(self.select_image)
        self.select_video_button.clicked.connect(self.select_video)
        self.edit_check_in_button.clicked.connect(self.edit_check_in)
        self.edit_slot_button.clicked.connect(self.edit_slot_points)
        self.delete_button.clicked.connect(self.toggle_delete_mode)
        self.save_button.clicked.connect(self.save_points)

        self.load_camera_data()

    def load_camera_data(self):
        logging.debug("load_camera_data called")
        try:
            self.db_context = DBContext()
            self.camera_repo = CameraRepository(self.db_context)
            camera = self.camera_repo.get_camera_by_id(self.camera_id)
            if camera:
                val_link = getattr(camera, 'ValLink', 'Not loaded')
                self.val_link_label.setText(f"ValLink: {val_link}")
                if val_link and val_link != 'Not loaded':
                    video_extensions = ('.mp4', '.avi', '.mov')
                    is_video = val_link.lower().endswith(video_extensions)
                    self.image_label.load_media(val_link, is_video=is_video)
                    if is_video:
                        self.slider.setMaximum(self.image_label.frame_count - 1)
                        self.slider.setValue(0)
                        self.timer.start(33)
                self.image_label.load_camera_points(camera)
                self.chs_repo = CameraHaveSlotRepository(self.db_context)
                camera_have_slots = self.chs_repo.get_by_camera_id(self.camera_id)
                for chs in camera_have_slots:
                    logging.debug(f"CameraHaveSlot object: {vars(chs)}")
                self.image_label.load_slot_points(camera_have_slots)
                self.slot_combo.clear()
                for chs in camera_have_slots:
                    slot_id = getattr(chs, 'Slot_', None)
                    if slot_id is not None:
                        self.slot_combo.addItem(f"Slot {slot_id}", slot_id)
                        logging.debug(f"Added slot to combo box: {slot_id}")
                    else:
                        logging.warning(f"CameraHaveSlot object missing 'Slot_' attribute: {vars(chs)}")
                logging.debug("Loaded camera data successfully")
            else:
                self.val_link_label.setText("ValLink: Camera not found")
                logging.warning(f"Camera with ID {self.camera_id} not found")
        except Exception as e:
            logging.error(f"Error in load_camera_data: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể tải dữ liệu camera: {str(e)}")

    def select_image(self):
        logging.debug("select_image called")
        try:
            if self.image_label.is_video:
                self.timer.stop()
                self.image_label.close_video()
                self.slider.setMaximum(0)
                self.slider.setValue(0)

            file_path, _ = QFileDialog.getOpenFileName(self, "Chọn hình ảnh", "", "Image Files (*.png *.jpg *.bmp)")
            if file_path:
                self.image_label.load_media(file_path, is_video=False)
                self.val_link_label.setText(f"ValLink: {file_path}")
                self.image_label.check_in_quad = None
                self.image_label.slot_quads.clear()
                self.image_label.points.clear()
                self.image_label.update()
                logging.debug(f"Selected image: {file_path}")
        except Exception as e:
            logging.error(f"Error in select_image: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể tải ảnh: {str(e)}")

    def select_video(self):
        logging.debug("select_video called")
        try:
            if self.image_label.is_video:
                self.timer.stop()
                self.image_label.close_video()

            file_path, _ = QFileDialog.getOpenFileName(self, "Chọn video", "", "Video Files (*.mp4 *.avi *.mov)")
            if file_path:
                self.image_label.load_media(file_path, is_video=True)
                self.val_link_label.setText(f"ValLink: {file_path}")
                self.slider.setMaximum(self.image_label.frame_count - 1)
                self.slider.setValue(0)
                self.timer.start(33)
                self.image_label.check_in_quad = None
                self.image_label.slot_quads.clear()
                self.image_label.points.clear()
                self.image_label.update()
                logging.debug(f"Selected video: {file_path}")
        except Exception as e:
            logging.error(f"Error in select_video: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể tải video: {str(e)}")

    def read_frame(self):
        try:
            if self.image_label.is_video:
                frame_pos = self.slider.value()
                self.image_label.read_frame(frame_pos)
        except Exception as e:
            logging.error(f"Error in read_frame: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể đọc frame: {str(e)}")

    def slider_moved(self, value):
        logging.debug(f"slider_moved to: {value}")
        try:
            if self.image_label.is_video:
                self.image_label.current_frame_pos = value
                self.read_frame()
        except Exception as e:
            logging.error(f"Error in slider_moved: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể di chuyển slider: {str(e)}")

    def edit_check_in(self):
        logging.debug("edit_check_in called")
        try:
            self.image_label.set_mode('check_in')
        except Exception as e:
            logging.error(f"Error in edit_check_in: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể chỉnh sửa Check-in: {str(e)}")

    def edit_slot_points(self):
        logging.debug("edit_slot_points called")
        try:
            slot_id = self.slot_combo.currentData()
            if slot_id is not None:
                self.image_label.set_mode('slot', slot_id)
                logging.debug(f"Editing slot {slot_id}")
            else:
                QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một slot!")
                logging.warning("No slot selected for editing")
        except Exception as e:
            logging.error(f"Error in edit_slot_points: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể chỉnh sửa slot: {str(e)}")

    def toggle_delete_mode(self):
        logging.debug("toggle_delete_mode called")
        try:
            delete_mode = not self.image_label.delete_mode
            self.image_label.set_delete_mode(delete_mode)
            self.delete_button.setText("Delete Mode (On)" if delete_mode else "Delete Mode")
            logging.debug(f"Delete mode toggled to: {delete_mode}")
        except Exception as e:
            logging.error(f"Error in toggle_delete_mode: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể chuyển chế độ xóa: {str(e)}")

    def save_points(self):
        logging.debug("save_points called")
        try:
            points = self.image_label.get_points()
            camera = self.camera_repo.get_camera_by_id(self.camera_id)
            if camera:
                # Save check-in quadrilateral
                if points['check_in_quad'] and points['check_in_quad'] != [(0, 0)] * 4:
                    camera.d1x, camera.d1y = points['check_in_quad'][0]
                    camera.d2x, camera.d2y = points['check_in_quad'][1]
                    camera.d3x, camera.d3y = points['check_in_quad'][2]
                    camera.d4x, camera.d4y = points['check_in_quad'][3]
                    camera.ValLink = self.val_link_label.text().replace("ValLink: ", "")
                    logging.debug(f"Saving check-in quad: {points['check_in_quad']}")
                self.camera_repo.update_camera(camera)
                logging.debug("Updated camera check-in points")

                # Save slot quadrilaterals
                for slot_id, quad in points['slot_quads'].items():
                    chs = self.chs_repo.get_by_camera_slot(self.camera_id, slot_id)
                    if chs and quad != [(0, 0)] * 4:
                        chs.d1x, chs.d1y = quad[0]
                        chs.d2x, chs.d2y = quad[1]
                        chs.d3x, chs.d3y = quad[2]
                        chs.d4x, chs.d4y = quad[3]
                        self.chs_repo.update_camera_have_slot(chs)
                        logging.debug(f"Updated slot points for slot {slot_id}: {quad}")

            QMessageBox.information(self, "Thành công", "Đã lưu tọa độ!")
            logging.debug("Saved points successfully")
            self.accept()
        except Exception as e:
            logging.error(f"Error in save_points: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể lưu tọa độ: {str(e)}")

    def get_points(self):
        logging.debug("get_points called")
        try:
            return self.image_label.get_points()
        except Exception as e:
            logging.error(f"Error in get_points: {str(e)}")
            raise

    def closeEvent(self, event):
        logging.debug("closeEvent called")
        try:
            self.timer.stop()
            self.image_label.close_video()
            super().closeEvent(event)
            logging.debug("Dialog closed")
        except Exception as e:
            logging.error(f"Error in closeEvent: {str(e)}")
            raise

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    dialog = PointPickerView(camera_id=1)
    dialog.exec_()
    sys.exit(app.exec_())