from typing import List, Optional
from BusinessObject.models import CheckIn

class ICheckIn:
    def get_checkin_by_manager(self, manager_username: str) -> List[CheckIn]:
        pass

    def add_checkin(self, checkin: CheckIn) -> bool:
        pass

    def remove_checkin(self, checkin_id: int) -> bool:
        pass

    def update_checkin(self, checkin: CheckIn) -> bool:
        pass

    def get_checkin_by_id(self, checkin_id: int) -> Optional[CheckIn]:
        pass