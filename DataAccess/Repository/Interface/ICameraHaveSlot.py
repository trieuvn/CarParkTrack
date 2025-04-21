# data_access/repository/interfaces/icamera_have_slot_repository.py
from abc import ABC, abstractmethod
from typing import List, Optional
from BusinessObject.models import CameraHaveSlot, Slot

class ICameraHaveSlotRepository(ABC):
    @abstractmethod
    def add_camera_have_slot(self, chs: CameraHaveSlot) -> CameraHaveSlot:
        pass

    @abstractmethod
    def update_camera_have_slot(self, chs: CameraHaveSlot) -> None:
        pass

    @abstractmethod
    def get_by_camera_id(self, camera_id: int) -> List[CameraHaveSlot]:
        pass

    @abstractmethod
    def get_by_camera_slot(self, camera_id: int, slot_id: int) -> Optional[CameraHaveSlot]:
        pass

    @abstractmethod
    def get_slots_by_manager(self, manager_username: str) -> List[Slot]:
        pass