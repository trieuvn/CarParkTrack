from abc import ABC, abstractmethod

class ISlotRepository(ABC):
    @abstractmethod
    def add_slot(self, slot):
        pass

    @abstractmethod
    def get_all_slots(self):
        pass