from abc import ABC, abstractmethod
from typing import Optional, List
from BusinessObject.models import Manager

class IManagerRepository(ABC):
    @abstractmethod
    def authenticate(self, username, password):
        pass

    @abstractmethod
    def get_manager_by_username(self, username):
        pass

    @abstractmethod
    def get_all_managers(self) -> List[Manager]:
        pass
