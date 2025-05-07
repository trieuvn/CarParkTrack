# checkinDAO.py
from typing import List, Optional
import logging
from sqlalchemy.orm import Session
from DataAccess.dbcontext import DBContext
from BusinessObject.models import CheckIn

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class CheckInDAO:
    def __init__(self, db_context: DBContext):
        self._db_context = db_context
        logging.debug("CheckInDAO initialized with db_context")

    def get_checkin_by_manager(self, manager_username: str) -> List[CheckIn]:
        """Retrieve all check-ins associated with a specific manager."""
        logging.debug(f"Getting check-ins for manager: {manager_username}")
        with self._db_context.get_session() as session:
            try:
                checkins = session.query(CheckIn).filter(CheckIn.Manager_ == manager_username).all()
                logging.debug(f"Found {len(checkins)} check-ins for manager {manager_username}")
                return checkins
            except Exception as e:
                logging.error(f"Database error in get_checkin_by_manager: {str(e)}")
                raise Exception(f"Database error: {str(e)}")

    def add_checkin(self, checkin: CheckIn) -> bool:
        """Add a new check-in to the database."""
        logging.debug(f"Adding check-in: {checkin.Name}, Manager_: {checkin.Manager_}")
        with self._db_context.get_session() as session:
            try:
                session.add(checkin)
                session.commit()
                session.refresh(checkin)  # Refresh to get the ID
                logging.debug(f"Successfully added check-in with ID: {checkin.ID}")
                return True
            except Exception as e:
                session.rollback()
                logging.error(f"Failed to add check-in: {str(e)}")
                raise Exception(f"Failed to add check-in: {str(e)}")

    def remove_checkin(self, checkin_id: int) -> bool:
        """Remove a check-in by its ID."""
        logging.debug(f"Removing check-in with ID: {checkin_id}")
        with self._db_context.get_session() as session:
            try:
                checkin = session.query(CheckIn).filter(CheckIn.ID == checkin_id).first()
                if checkin:
                    session.delete(checkin)
                    session.commit()
                    logging.debug(f"Successfully removed check-in with ID: {checkin_id}")
                    return True
                logging.warning(f"Check-in with ID {checkin_id} not found")
                return False
            except Exception as e:
                session.rollback()
                logging.error(f"Failed to remove check-in: {str(e)}")
                raise Exception(f"Failed to remove check-in: {str(e)}")

    def update_checkin(self, checkin: CheckIn) -> bool:
        """Update an existing check-in."""
        logging.debug(f"Updating check-in with ID: {checkin.ID}")
        with self._db_context.get_session() as session:
            try:
                existing_checkin = session.query(CheckIn).filter(CheckIn.ID == checkin.ID).first()
                if existing_checkin:
                    existing_checkin.Name = checkin.Name
                    existing_checkin.d1x = checkin.d1x
                    existing_checkin.d1y = checkin.d1y
                    existing_checkin.d2x = checkin.d2x
                    existing_checkin.d2y = checkin.d2y
                    existing_checkin.d3x = checkin.d3x
                    existing_checkin.d3y = checkin.d3y
                    existing_checkin.d4x = checkin.d4x
                    existing_checkin.d4y = checkin.d4y
                    existing_checkin.Manager_ = checkin.Manager_
                    session.commit()
                    logging.debug(f"Successfully updated check-in with ID: {checkin.ID}")
                    return True
                logging.warning(f"Check-in with ID {checkin.ID} not found for update")
                return False
            except Exception as e:
                session.rollback()
                logging.error(f"Failed to update check-in: {str(e)}")
                raise Exception(f"Failed to update check-in: {str(e)}")

    def get_checkin_by_id(self, checkin_id: int) -> Optional[CheckIn]:
        """Retrieve a check-in by its ID."""
        logging.debug(f"Getting check-in by ID: {checkin_id}")
        with self._db_context.get_session() as session:
            try:
                checkin = session.query(CheckIn).filter(CheckIn.ID == checkin_id).first()
                if checkin:
                    logging.debug(f"Found check-in with ID: {checkin_id}")
                else:
                    logging.warning(f"Check-in with ID {checkin_id} not found")
                return checkin
            except Exception as e:
                logging.error(f"Database error in get_checkin_by_id: {str(e)}")
                raise Exception(f"Database error: {str(e)}")