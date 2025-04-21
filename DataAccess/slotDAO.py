from BusinessObject.models import Slot

class SlotDAO:
    def __init__(self, db_context):
        self.db_context = db_context

    def add_slot(self, slot):
        with self.db_context.get_session() as session:
            session.add(slot)
            session.commit()
            session.refresh(slot)
            return slot

    def get_all_slots(self):
        with self.db_context.get_session() as session:
            return session.query(Slot).all()