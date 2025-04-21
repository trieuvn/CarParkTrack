# data_access/repository/interfaces/icamera_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from BusinessObject.models import Camera

class ICameraRepository(ABC):
    @abstractmethod
    def add_camera(self, camera: Camera) -> Camera:
        pass

    @abstractmethod
    def update_camera(self, camera: Camera) -> None:
        pass

    @abstractmethod
    def delete_camera(self, camera_id: int) -> bool:
        pass

    @abstractmethod
    def get_camera_by_id(self, camera_id: int) -> Optional[Camera]:
        pass

    @abstractmethod
    def get_all_cameras(self) -> List[Camera]:
        pass

    @abstractmethod
    def get_cameras_by_manager(self, manager: str) -> List[Camera]:
        pass