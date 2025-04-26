from typing import List
from BusinessObject.models import PTS
from DataAccess.dbcontext import DBContext
from DataAccess.ptsDAO import PTSDAO
from DataAccess.Repository.Interface.ipts import IPTS

class PTSRepository(IPTS):
    def __init__(self, db_context: DBContext):
        self.db_context = db_context
        self.pts_dao = PTSDAO(db_context)

    def add_pts(self, pts: PTS) -> None:
        self.pts_dao.add_pts(pts)

    def get_pts_by_camera_id(self, camera_id: int) -> List[PTS]:
        return self.pts_dao.get_pts_by_camera_id(camera_id)

    def delete_pts_by_id(self, pts_id: int) -> bool:
        return self.pts_dao.delete_pts_by_id(pts_id)

    def delete_pts_by_camera_id(self, camera_id: int) -> bool:
        return self.pts_dao.delete_pts_by_camera_id(camera_id)