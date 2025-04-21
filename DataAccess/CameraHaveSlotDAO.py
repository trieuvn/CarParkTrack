# data_access/dao/camera_have_slot_dao.py
from typing import List, Optional
from BusinessObject.models import CameraHaveSlot, Slot
from sqlalchemy.orm import Session

class CameraHaveSlotDAO:
    def __init__(self, db_context):
        self.db_context = db_context

    def add_camera_have_slot(self, chs: CameraHaveSlot) -> CameraHaveSlot:
        with self.db_context.get_session() as session:
            session.add(chs)
            session.commit()
            session.refresh(chs)
            return chs

    def update_camera_have_slot(self, chs: CameraHaveSlot) -> None:
        with self.db_context.get_session() as session:
            session.merge(chs)
            session.commit()

    def get_by_camera_id(self, camera_id: int) -> List[CameraHaveSlot]:
        with self.db_context.get_session() as session:
            return session.query(CameraHaveSlot).filter_by(Camera_=camera_id).all()

    def get_by_camera_slot(self, camera_id: int, slot_id: int) -> Optional[CameraHaveSlot]:
        with self.db_context.get_session() as session:
            return session.query(CameraHaveSlot).filter_by(Camera_=camera_id, Slot_=slot_id).first()

    def get_slots_by_manager(self, manager_username: str) -> List[Slot]:
        with self.db_context.get_session() as session:
            return session.query(Slot).filter_by(Manager=manager_username).all()