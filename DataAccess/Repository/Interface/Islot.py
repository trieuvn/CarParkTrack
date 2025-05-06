from abc import ABC, abstractmethod

class ISlotRepository(ABC):
    @abstractmethod
    def add_slot(self, slot):
        pass

    @abstractmethod
    def get_all_slots(self):
        pass

    @abstractmethod
    def setBoxByID(self, slot_id: int, box: tuple):
        pass

    @abstractmethod
    def getBox(self, slot_id: int) -> tuple:
        pass

    @abstractmethod
    def deleteSlotByPoint(self, x: int, y: int) -> int:
        pass