from typing import Optional, List
from BusinessObject.models import Manager

class ManagerDAO:
    def __init__(self, db_context):
        self.db_context = db_context

    def authenticate(self, username: str, password: str) -> Optional[Manager]:
        with self.db_context.get_session() as session:
            manager = session.query(Manager).filter_by(UserName=username).first()
            if manager and manager.Password == password:
                return manager
            return None

    def get_manager_by_username(self, username: str) -> Optional[Manager]:
        with self.db_context.get_session() as session:
            return session.query(Manager).filter_by(UserName=username).first()

    def get_all_managers(self) -> List[Manager]:
        with self.db_context.get_session() as session:
            return session.query(Manager).all()