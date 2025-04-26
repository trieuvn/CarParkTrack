from typing import List
from BusinessObject.models import PTS

class IPTS:
    def add_pts(self, pts: PTS) -> None:
        pass

    def get_pts_by_camera_id(self, camera_id: int) -> List[PTS]:
        pass

    def delete_pts_by_id(self, pts_id: int) -> bool:
        pass

    def delete_pts_by_camera_id(self, camera_id: int) -> bool:
        pass