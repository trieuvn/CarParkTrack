from sqlalchemy import text
import logging
from typing import Optional, List
from sqlalchemy.orm import Session
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

    def get_manager_by_username(self, username: str) -> Manager:
        try:
            with self.db_context.get_session() as session:
                query = text("SELECT * FROM [Manager] WHERE [UserName] = :username")
                result = session.execute(query, {"username": username}).fetchone()
                if result:
                    return Manager(
                        UserName=result[0],
                        Password=result[1],
                        Email=result[2],
                        PhoneNumber=result[3],
                        MainMap=result[4]
                    )
                return None
        except Exception as e:
            logging.error(f"Error in get_manager_by_username DAO: {str(e)}")
            raise

    def get_all_managers(self) -> List[Manager]:
        with self.db_context.get_session() as session:
            return session.query(Manager).all()

    def add_manager(self, manager: Manager) -> None:
        with self.db_context.get_session() as session:
            session.add(manager)
            session.commit()

    def update_manager(self, manager: Manager) -> None:
        with self.db_context.get_session() as session:
            session.merge(manager)
            session.commit()

    def delete_manager(self, manager: Manager) -> None:
        with self.db_context.get_session() as session:
            session.delete(manager)
            session.commit()