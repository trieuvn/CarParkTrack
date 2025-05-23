# CheckIn.py
from typing import List, Optional
import logging
from BusinessObject.models import CheckIn
from DataAccess.checkinDAO import CheckInDAO
from DataAccess.Repository.Interface.ICheckIn import ICheckIn

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class CheckInRepository(ICheckIn):
    def __init__(self, db_context):
        self.checkin_dao = CheckInDAO(db_context)
        logging.debug("CheckInRepository initialized")

    def get_checkin_by_manager(self, manager_username: str) -> List[CheckIn]:
        """Retrieve all check-ins associated with a manager."""
        logging.debug(f"CheckInRepository: Retrieving check-ins for manager {manager_username}")
        try:
            checkins = self.checkin_dao.get_checkin_by_manager(manager_username)
            logging.debug(f"CheckInRepository: Retrieved {len(checkins)} check-ins")
            return checkins
        except Exception as e:
            logging.error(f"Error retrieving check-ins for manager {manager_username}: {str(e)}")
            return []

    def add_checkin(self, checkin: CheckIn) -> Optional[CheckIn]:
        """Add a new check-in for a manager and return the added check-in."""
        logging.debug(f"CheckInRepository: Adding check-in {checkin.Name}")
        try:
            success = self.checkin_dao.add_checkin(checkin)
            if success:
                logging.debug(f"CheckInRepository: Successfully added check-in with ID {checkin.ID}")
                return checkin
            logging.error("CheckInRepository: add_checkin returned False")
            return None
        except Exception as e:
            logging.error(f"Error adding check-in: {str(e)}")
            return None

    def remove_checkin(self, checkin_id: int) -> bool:
        """Remove a check-in by its ID."""
        logging.debug(f"CheckInRepository: Removing check-in {checkin_id}")
        try:
            return self.checkin_dao.remove_checkin(checkin_id)
        except Exception as e:
            logging.error(f"Error removing check-in {checkin_id}: {str(e)}")
            return False

    def update_checkin(self, checkin: CheckIn) -> bool:
        """Update an existing check-in."""
        logging.debug(f"CheckInRepository: Updating check-in {checkin.ID}")
        try:
            return self.checkin_dao.update_checkin(checkin)
        except Exception as e:
            logging.error(f"Error updating check-in: {str(e)}")
            return False

    def get_checkin_by_id(self, checkin_id: int) -> Optional[CheckIn]:
        """Retrieve a check-in by its ID."""
        logging.debug(f"CheckInRepository: Getting check-in {checkin_id}")
        try:
            return self.checkin_dao.get_checkin_by_id(checkin_id)
        except Exception as e:
            logging.error(f"Error retrieving check-in {checkin_id}: {str(e)}")
            return None