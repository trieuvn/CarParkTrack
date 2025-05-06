from DataAccess.Repository.Interface.Islot import ISlotRepository
from DataAccess.slotDAO import SlotDAO

class SlotRepository(ISlotRepository):
    def __init__(self, db_context):
        self.slot_dao = SlotDAO(db_context)

    def add_slot(self, slot):
        if not slot.Name.strip():
            raise ValueError("Slot name cannot be empty!")
        return self.slot_dao.add_slot(slot)

    def get_all_slots(self):
        return self.slot_dao.get_all_slots()

    def get_slots_by_manager(self, username):
        return self.slot_dao.get_slots_by_manager(username)

    def setBoxByID(self, slot_id: int, box: tuple):
        """Cập nhật tọa độ box cho slot dựa trên ID
        Args:
            slot_id (int): ID của slot
            box (tuple): Tuple chứa (d1x, d1y, d2x, d2y, d3x, d3y, d4x, d4y)
        Returns:
            bool: True nếu thành công, False nếu không tìm thấy slot
        """
        return self.slot_dao.setBoxByID(slot_id, box)

    def getBox(self, slot_id: int) -> tuple:
        """Lấy tọa độ box cho slot dựa trên ID
        Returns:
            tuple: (d1x, d1y, d2x, d2y, d3x, d3y, d4x, d4y) hoặc (None, None, None, None, None, None, None, None) nếu không tìm thấy
        """
        return self.slot_dao.getBox(slot_id)

    def deleteSlotByPoint(self, x: int, y: int) -> int:
        """Xóa tất cả các slot có box chứa điểm (x, y)
        Args:
            x (int): Tọa độ x của điểm
            y (int): Tọa độ y của điểm
        Returns:
            int: Số lượng slot đã xóa
        """
        return self.slot_dao.deleteSlotByPoint(x, y)

    def update_slot_box(self, slot_id: int, d1x: int, d1y: int, d2x: int, d2y: int, d3x: int, d3y: int, d4x: int,
                        d4y: int) -> bool:
        return self.slot_dao.update_slot_box(slot_id, d1x, d1y, d2x, d2y, d3x, d3y, d4x, d4y)

    def delete_slot_by_id(self, slot_id: int) -> bool:
        return self.slot_dao.delete_slot_by_id(slot_id)