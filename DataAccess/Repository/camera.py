from typing import List, Optional
from DataAccess.Repository.Interface.Icamera import ICameraRepository
from DataAccess.cameraDAO import CameraDAO
from BusinessObject.models import Camera

class CameraRepository(ICameraRepository):
    def __init__(self, db_context):
        self.camera_dao = CameraDAO(db_context)

    def add_camera(self, camera: Camera) -> Camera:
        if not camera.Name or not camera.Name.strip():
            raise ValueError("Camera name cannot be empty!")
        return self.camera_dao.add_camera(camera)

    def update_camera(self, camera: Camera) -> None:
        if not camera.Name or not camera.Name.strip():
            raise ValueError("Camera name cannot be empty!")
        self.camera_dao.update_camera(camera)

    def delete_camera(self, camera_id: int) -> bool:
        return self.camera_dao.delete_camera(camera_id)

    def get_camera_by_id(self, camera_id: int) -> Optional[Camera]:
        return self.camera_dao.get_camera_by_id(camera_id)

    def get_all_cameras(self) -> List[Camera]:
        return self.camera_dao.get_all_cameras()

    def get_cameras_by_manager(self, manager: str) -> List[Camera]:
        if not manager or not manager.strip():
            raise ValueError("Manager name cannot be empty!")
        return self.camera_dao.get_cameras_by_manager(manager)