from DataAccess.Repository.Interface.Imanager import IManagerRepository
from DataAccess.managerDAO import ManagerDAO
from typing import Optional, List
from BusinessObject.models import Manager

class ManagerRepository(IManagerRepository):
    def __init__(self, db_context):
        self.manager_dao = ManagerDAO(db_context)

    def authenticate(self, username, password):
        return self.manager_dao.authenticate(username, password)

    def get_manager_by_username(self, username):
        return self.manager_dao.get_manager_by_username(username)

    def get_all_managers(self) -> List[Manager]:
        return self.manager_dao.get_all_managers()