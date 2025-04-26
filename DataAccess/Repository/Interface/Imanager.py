from typing import Optional, List
from BusinessObject.models import Manager

class IManagerRepository:
    def authenticate(self, username: str, password: str) -> Optional[Manager]:
        pass

    def get_manager_by_username(self, username: str) -> Optional[Manager]:
        pass

    def get_all_managers(self) -> List[Manager]:
        pass

    def add_manager(self, manager: Manager) -> None:
        pass

    def update_manager(self, manager: Manager) -> None:
        pass

    def delete_manager(self, manager: Manager) -> None:
        pass