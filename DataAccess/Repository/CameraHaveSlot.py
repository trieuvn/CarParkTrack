# data_access/repository/camera_have_slot_repository.py
from typing import List, Optional
from DataAccess.Repository.Interface.ICameraHaveSlot import ICameraHaveSlotRepository
from DataAccess.CameraHaveSlotDAO import CameraHaveSlotDAO
from BusinessObject.models import CameraHaveSlot, Slot

class CameraHaveSlotRepository(ICameraHaveSlotRepository):
    def __init__(self, db_context):
        self.dao = CameraHaveSlotDAO(db_context)

    def add_camera_have_slot(self, chs: CameraHaveSlot) -> CameraHaveSlot:
        return self.dao.add_camera_have_slot(chs)

    def update_camera_have_slot(self, chs: CameraHaveSlot) -> None:
        self.dao.update_camera_have_slot(chs)

    def get_by_camera_id(self, camera_id: int) -> List[CameraHaveSlot]:
        return self.dao.get_by_camera_id(camera_id)

    def get_by_camera_slot(self, camera_id: int, slot_id: int) -> Optional[CameraHaveSlot]:
        return self.dao.get_by_camera_slot(camera_id, slot_id)

    def get_slots_by_manager(self, manager_username: str) -> List[Slot]:
        return self.dao.get_slots_by_manager(manager_username)