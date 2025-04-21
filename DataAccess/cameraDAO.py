from typing import List, Optional
from BusinessObject.models import Camera
from sqlalchemy.orm import Session

class CameraDAO:
    def __init__(self, db_context):
        self.db_context = db_context

    def add_camera(self, camera: Camera) -> Camera:
        with self.db_context.get_session() as session:
            session.add(camera)
            session.commit()
            session.refresh(camera)
            print(f"Camera added to database with ID: {camera.ID}")
            return camera

    def update_camera(self, camera: Camera) -> None:
        with self.db_context.get_session() as session:
            session.merge(camera)
            session.commit()

    def delete_camera(self, camera_id: int) -> bool:
        with self.db_context.get_session() as session:
            camera = session.get(Camera, camera_id)
            if camera:
                session.delete(camera)
                session.commit()
                return True
            return False

    def get_camera_by_id(self, camera_id: int) -> Optional[Camera]:
        with self.db_context.get_session() as session:
            return session.get(Camera, camera_id)

    def get_all_cameras(self) -> List[Camera]:
        with self.db_context.get_session() as session:
            return session.query(Camera).all()

    def get_cameras_by_manager(self, manager: str) -> List[Camera]:
        with self.db_context.get_session() as session:
            cameras = session.query(Camera).filter(Camera.Manager_ == manager).all()
            print(f"Cameras found for manager '{manager}': {[camera.ID for camera in cameras]}")
            return cameras