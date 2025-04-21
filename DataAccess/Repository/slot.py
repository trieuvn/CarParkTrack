from DataAccess.Repository.Interface.Islot import ISlotRepository
from DataAccess.slotDAO import SlotDAO


class SlotRepository(ISlotRepository):
    def __init__(self, db_context):
        self.slot_dao = SlotDAO(db_context)

    def add_slot(self, slot):
        if not slot.name.strip():
            raise ValueError("Slot name cannot be empty!")
        return self.slot_dao.add_slot(slot)

    def get_all_slots(self):
        return self.slot_dao.get_all_slots()