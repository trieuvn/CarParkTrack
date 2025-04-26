from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QTableWidgetItem
from DataAccess.dbcontext import DBContext
from DataAccess.Repository.camera import CameraRepository
from DataAccess.Repository.manager import ManagerRepository
from DataAccess.Repository.pts import PTSRepository
from Presentation.PointPicker import PointPickerView
from Presentation.Designer.CameraManagement import Ui_CameraManagementView
from BusinessObject.models import Camera, Manager
from typing import Optional
from Utils.CameraTracking import process_video, load_camera_data
from Utils.homography import run_homography

class CameraManagementView(QtWidgets.QMainWindow, Ui_CameraManagementView):
    def __init__(self, manager_username: str):
        super().__init__()
        self.manager_username = manager_username
        self.db_context = DBContext()
        self.camera_repo = CameraRepository(self.db_context)
        self.manager_repo = ManagerRepository(self.db_context)
        self.pts_repo = PTSRepository(self.db_context)
        self.current_camera_id: Optional[int] = None
        self.points = {}
        print(f"Initializing CameraManagementView with manager: {self.manager_username}")
        self.setupUi(self)
        print("UI setup completed")
        self.load_main_map()
        self.connect_signals()
        print("Signals connected")

    def load_main_map(self):
        try:
            manager = self.manager_repo.get_manager_by_username(self.manager_username)
            if manager and manager.MainMap:
                self.main_map_edit.setText(manager.MainMap)
            else:
                self.main_map_edit.setText("")
            print(f"Loaded MainMap: {self.main_map_edit.text()}")
        except Exception as e:
            print(f"Error loading MainMap: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể tải MainMap: {str(e)}")

    def connect_signals(self):
        try:
            self.picker_button.clicked.connect(self.open_point_picker)
            print("Connected picker_button signal")
            self.add_button.clicked.connect(self.add_camera)
            print("Connected add_button signal")
            self.edit_button.clicked.connect(self.edit_camera)
            print("Connected edit_button signal")
            self.delete_button.clicked.connect(self.delete_camera)
            print("Connected delete_button signal")
            self.clear_button.clicked.connect(self.clear_form)
            print("Connected clear_button signal")
            self.operate_button.clicked.connect(self.operate_camera)
            print("Connected operate_button signal")
            self.mapping_button.clicked.connect(self.run_mapping)
            print("Connected mapping_button signal")
            self.delete_pts_button.clicked.connect(self.delete_pts)
            print("Connected delete_pts_button signal")
            self.clear_pts_points_button.clicked.connect(self.clear_pts_points)
            print("Connected clear_pts_points_button signal")
            self.table.selectionModel().selectionChanged.connect(self.on_table_selection_changed)
            print("Connected table selection signal")
            print(f"Add button enabled: {self.add_button.isEnabled()}")
            print(f"Add button visible: {self.add_button.isVisible()}")
            self.refresh_table()
        except AttributeError as e:
            print(f"Error connecting signals: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể kết nối sự kiện: {str(e)}")
            raise

    def run_mapping(self):
        try:
            print("Starting run_mapping")
            if self.current_camera_id is None:
                print("No camera selected")
                QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một camera để ánh xạ!")
                return
            camera = self.camera_repo.get_camera_by_id(self.current_camera_id)
            if not camera or not camera.ValLink:
                print("Invalid camera or ValLink")
                QMessageBox.critical(self, "Lỗi", "Camera không có đường dẫn ValLink hợp lệ!")
                return
            manager = self.manager_repo.get_manager_by_username(self.manager_username)
            if not manager or not manager.MainMap:
                print("Invalid manager or MainMap")
                QMessageBox.critical(self, "Lỗi", "Manager không có đường dẫn MainMap hợp lệ!")
                return
            print(
                f"Calling run_homography with camera_id={self.current_camera_id}, val_link={camera.ValLink}, main_map={manager.MainMap}")
            run_homography(self.current_camera_id, camera.ValLink, manager.MainMap, self.db_context)
            print("run_homography completed successfully")
            QMessageBox.information(self, "Thành công", "Đã hoàn thành ánh xạ!")
        except Exception as e:
            print(f"Error in run_mapping: {str(e)}")
            import traceback
            print("Stack trace:")
            print(traceback.format_exc())
            QMessageBox.critical(self, "Lỗi", f"Không thể thực hiện ánh xạ: {str(e)}")

    def delete_pts(self):
        try:
            pts_id_text = self.pts_id_edit.text().strip()
            if not pts_id_text:
                QMessageBox.warning(self, "Lỗi", "Vui lòng nhập ID của PTS để xóa!")
                return
            try:
                pts_id = int(pts_id_text)
            except ValueError:
                QMessageBox.warning(self, "Lỗi", "ID PTS phải là một số nguyên!")
                return
            if self.pts_repo.delete_pts_by_id(pts_id):
                QMessageBox.information(self, "Thành công", f"Đã xóa PTS với ID {pts_id}!")
                self.pts_id_edit.clear()
            else:
                QMessageBox.warning(self, "Lỗi", f"Không tìm thấy PTS với ID {pts_id}!")
        except Exception as e:
            print(f"Error in delete_pts: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể xóa PTS: {str(e)}")

    def clear_pts_points(self):
        try:
            if self.current_camera_id is None:
                QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một camera để xóa điểm PTS!")
                return
            reply = QMessageBox.question(
                self, "Xác nhận", "Bạn có chắc muốn xóa tất cả điểm PTS của camera này?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                if self.pts_repo.delete_pts_by_camera_id(self.current_camera_id):
                    QMessageBox.information(self, "Thành công", "Đã xóa tất cả điểm PTS của camera!")
                else:
                    QMessageBox.warning(self, "Thông báo", "Không có điểm PTS nào để xóa!")
        except Exception as e:
            print(f"Error in clear_pts_points: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể xóa điểm PTS: {str(e)}")

    def open_point_picker(self):
        try:
            if self.current_camera_id is None:
                QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một camera để chỉnh sửa điểm!")
                return
            picker = PointPickerView(self.current_camera_id)
            if picker.exec_():
                self.points = picker.get_points()
                self.edit_camera()
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể mở Point Picker: {str(e)}")

    def operate_camera(self):
        try:
            if self.current_camera_id is None:
                QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một camera để vận hành!")
                return
            video_path, _ = load_camera_data(self.current_camera_id)
            if video_path:
                process_video(video_path, self.current_camera_id)
            else:
                QMessageBox.critical(self, "Lỗi", "Không có đường dẫn video hợp lệ để xử lý!")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể vận hành camera: {str(e)}")

    def refresh_table(self):
        try:
            print("Refreshing table...")
            self.table.setRowCount(0)
            cameras = self.camera_repo.get_cameras_by_manager(self.manager_username)
            if not cameras:
                print(f"No cameras found for manager: {self.manager_username}")
                return
            for camera in cameras:
                row = self.table.rowCount()
                self.table.insertRow(row)
                print(f"Adding camera ID {camera.ID} to row {row}")
                self.table.setItem(row, 0, QTableWidgetItem(str(camera.ID)))
                self.table.setItem(row, 1, QTableWidgetItem(camera.Name or ""))
                self.table.setItem(row, 2, QTableWidgetItem(camera.ValLink or ""))
                self.table.setItem(row, 3, QTableWidgetItem(str(camera.CheckInLoc or "")))
                self.table.setItem(row, 4, QTableWidgetItem(str(camera.d1x or "")))
                self.table.setItem(row, 5, QTableWidgetItem(str(camera.d1y or "")))
                self.table.setItem(row, 6, QTableWidgetItem(str(camera.d2x or "")))
                self.table.setItem(row, 7, QTableWidgetItem(str(camera.d2y or "")))
                self.table.setItem(row, 8, QTableWidgetItem(str(camera.d3x or "")))
                self.table.setItem(row, 9, QTableWidgetItem(str(camera.d3y or "")))
                self.table.setItem(row, 10, QTableWidgetItem(str(camera.d4x or "")))
            self.table.repaint()
            print("Table refreshed")
        except Exception as e:
            print(f"Error in refresh_table: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể tải danh sách camera: {str(e)}")

    def add_camera(self):
        try:
            print("Add camera button clicked")
            if not self.name_edit.text().strip():
                raise ValueError("Camera name cannot be empty!")
            camera = Camera(
                Name=self.name_edit.text().strip(),
                ValLink=self.val_link_edit.text().strip() or None,
                Manager_=self.manager_username
            )
            print(f"Adding camera: {camera.Name}, Manager: {camera.Manager_}")
            added_camera = self.camera_repo.add_camera(camera)
            print(f"Camera added with ID: {added_camera.ID}")

            manager = self.manager_repo.get_manager_by_username(self.manager_username)
            if manager:
                manager.MainMap = self.main_map_edit.text().strip() or None
                self.manager_repo.update_manager(manager)
                print(f"Updated MainMap for manager {self.manager_username}: {manager.MainMap}")

            QMessageBox.information(self, "Thành công", "Đã thêm camera và cập nhật MainMap!")
            self.clear_form()
            self.refresh_table()
        except ValueError as e:
            print(f"Validation error in add_camera: {str(e)}")
            QMessageBox.warning(self, "Lỗi", str(e))
        except Exception as e:
            print(f"Error in add_camera: {str(e)}")
            QMessageBox.critical(self, "Lỗi", f"Không thể thêm camera: {str(e)}")

    def edit_camera(self):
        if self.current_camera_id is None:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một camera để sửa!")
            return
        try:
            camera = self.camera_repo.get_camera_by_id(self.current_camera_id)
            if camera:
                camera.Name = self.name_edit.text().strip() or None
                camera.ValLink = self.val_link_edit.text().strip() or None
                if self.points and 'check_in_quad' in self.points:
                    check_in_quad = self.points['check_in_quad']
                    if len(check_in_quad) == 4:
                        camera.d1x = check_in_quad[0][0]
                        camera.d1y = check_in_quad[0][1]
                        camera.d2x = check_in_quad[1][0]
                        camera.d2y = check_in_quad[1][1]
                        camera.d3x = check_in_quad[2][0]
                        camera.d3y = check_in_quad[2][1]
                        camera.d4x = check_in_quad[3][0]
                        camera.d4y = check_in_quad[3][1]
                camera.Manager_ = self.manager_username
                self.camera_repo.update_camera(camera)

                manager = self.manager_repo.get_manager_by_username(self.manager_username)
                if manager:
                    manager.MainMap = self.main_map_edit.text().strip() or None
                    self.manager_repo.update_manager(manager)
                    print(f"Updated MainMap for manager {self.manager_username}: {manager.MainMap}")

                QMessageBox.information(self, "Thành công", "Đã cập nhật camera và MainMap!")
                self.clear_form()
                self.refresh_table()
            else:
                QMessageBox.warning(self, "Lỗi", "Camera không tồn tại!")
        except ValueError as e:
            QMessageBox.warning(self, "Lỗi", str(e))
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể sửa camera: {str(e)}")

    def delete_camera(self):
        if self.current_camera_id is None:
            QMessageBox.warning(self, "Lỗi", "Vui lòng chọn một camera để xóa!")
            return
        reply = QMessageBox.question(
            self, "Xác nhận", "Bạn có chắc muốn xóa camera này?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                if self.camera_repo.delete_camera(self.current_camera_id):
                    QMessageBox.information(self, "Thành công", "Đã xóa camera!")
                    self.clear_form()
                    self.refresh_table()
                else:
                    QMessageBox.warning(self, "Lỗi", "Camera không tồn tại!")
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể xóa camera: {str(e)}")

    def clear_form(self):
        self.name_edit.clear()
        self.val_link_edit.clear()
        self.main_map_edit.clear()
        self.pts_id_edit.clear()
        self.points = {}
        self.current_camera_id = None
        self.load_main_map()

    def on_table_selection_changed(self):
        selected = self.table.selectedItems()
        if selected:
            row = selected[0].row()
            self.current_camera_id = int(self.table.item(row, 0).text())
            camera = self.camera_repo.get_camera_by_id(self.current_camera_id)
            if camera:
                self.name_edit.setText(camera.Name or "")
                self.val_link_edit.setText(camera.ValLink or "")
                self.points = {}
                if all(getattr(camera, attr) is not None for attr in ['d1x', 'd1y', 'd2x', 'd2y', 'd3x', 'd3y', 'd4x', 'd4y']):
                    self.points = {
                        'check_in_quad': [
                            (camera.d1x, camera.d1y),
                            (camera.d2x, camera.d2y),
                            (camera.d3x, camera.d3y),
                            (camera.d4x, camera.d4y)
                        ],
                        'slot_quads': {}
                    }
                self.load_main_map()