from typing import List, Optional
from sqlalchemy.orm import Session
from BusinessObject.models import PTS
from DataAccess.dbcontext import DBContext

class PTSDAO:
    def __init__(self, db_context: DBContext):
        self.db_context = db_context

    def add_pts(self, pts: PTS) -> None:
        with self.db_context.get_session() as session:
            session.add(pts)
            session.commit()

    def get_pts_by_camera_id(self, camera_id: int) -> List[PTS]:
        with self.db_context.get_session() as session:
            return session.query(PTS).filter_by(Camera_=camera_id).all()

    def delete_pts_by_id(self, pts_id: int) -> bool:
        with self.db_context.get_session() as session:
            pts = session.query(PTS).filter_by(ID=pts_id).first()
            if pts:
                session.delete(pts)
                session.commit()
                return True
            return False

    def delete_pts_by_camera_id(self, camera_id: int) -> bool:
        with self.db_context.get_session() as session:
            pts_records = session.query(PTS).filter_by(Camera_=camera_id).all()
            if pts_records:
                for pts in pts_records:
                    session.delete(pts)
                session.commit()
                return True
            return False