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

    def get_slots_by_manager(self, manager: str):
        with self.db_context.get_session() as session:
            slots = session.query(Slot).filter(Slot.Manager_ == manager).all()
            print(f"Cameras found for manager '{manager}': {[slot.ID for slot in slots]}")
            return slots

    def setBoxByID(self, slot_id: int, box: tuple):
        """Cập nhật tọa độ box cho slot dựa trên ID
        Args:
            slot_id (int): ID của slot
            box (tuple): Tuple chứa (d1x, d1y, d2x, d2y, d3x, d3y, d4x, d4y)
        Returns:
            bool: True nếu thành công, False nếu không tìm thấy slot
        """
        with self.db_context.get_session() as session:
            slot = session.query(Slot).filter(Slot.ID == slot_id).first()
            if slot:
                d1x, d1y, d2x, d2y, d3x, d3y, d4x, d4y = box
                slot.setBox(box)
                session.commit()
                return True
            return False

    def getBox(self, slot_id: int) -> tuple:
        """Lấy tọa độ box cho slot dựa trên ID
        Returns:
            tuple: (d1x, d1y, d2x, d2y, d3x, d3y, d4x, d4y) hoặc (None, None, None, None, None, None, None, None) nếu không tìm thấy
        """
        with self.db_context.get_session() as session:
            slot = session.query(Slot).filter(Slot.ID == slot_id).first()
            if slot:
                return slot.getBox()
            return (None, None, None, None, None, None, None, None)

    def deleteSlotByPoint(self, x: int, y: int) -> int:
        """Xóa tất cả các slot có box chứa điểm (x, y)
        Args:
            x (int): Tọa độ x của điểm
            y (int): Tọa độ y của điểm
        Returns:
            int: Số lượng slot đã xóa
        """
        with self.db_context.get_session() as session:
            slots = session.query(Slot).all()
            deleted_count = 0
            for slot in slots:
                box = slot.getBox()
                if all(coord is not None for coord in box):
                    quad = [(box[i], box[i + 1]) for i in range(0, len(box), 2)]
                    if self.is_point_inside_quad(x, y, quad):
                        session.delete(slot)
                        deleted_count += 1
            session.commit()
            return deleted_count

    def is_point_inside_quad(self, x: int, y: int, quad: list) -> bool:
        """Kiểm tra xem điểm (x, y) có nằm trong hình tứ giác hay không (Ray Casting algorithm)
        Args:
            x (int): Tọa độ x của điểm
            y (int): Tọa độ y của điểm
            quad (list): List chứa 4 điểm [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        Returns:
            bool: True nếu điểm nằm trong hình tứ giác, False nếu không
        """
        if len(quad) != 4:
            return False

        intersections = 0
        for i in range(4):
            p1 = quad[i]
            p2 = quad[(i + 1) % 4]
            if self.ray_intersects_segment(x, y, p1, p2):
                intersections += 1
        return intersections % 2 == 1

    def ray_intersects_segment(self, x: int, y: int, p1: tuple, p2: tuple) -> bool:
        """Kiểm tra xem tia ngang từ điểm (x, y) có giao với đoạn thẳng p1-p2 không
        Args:
            x (int): Tọa độ x của điểm
            y (int): Tọa độ y của điểm
            p1 (tuple): Điểm đầu (x1, y1)
            p2 (tuple): Điểm cuối (x2, y2)
        Returns:
            bool: True nếu tia giao với đoạn thẳng, False nếu không
        """
        x1, y1 = p1
        x2, y2 = p2

        if y1 > y2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

        if y == y1 or y == y2:
            y += 1  # Điều chỉnh nhỏ để tránh trường hợp điểm nằm trên cạnh

        if y < y1 or y > y2 or x > max(x1, x2):
            return False
        if x < min(x1, x2):
            return True
        if y2 == y1:  # Đoạn thẳng nằm ngang
            return False

        slope = (x2 - x1) / (y2 - y1)
        intersect_x = x1 + (y - y1) * slope
        return x < intersect_x

    def update_slot_box(self, slot_id: int, d1x: int, d1y: int, d2x: int, d2y: int, d3x: int, d3y: int, d4x: int,
                        d4y: int) -> bool:
        with self.db_context.get_session() as session:
            slot = session.query(Slot).filter(Slot.ID == slot_id).first()
            if slot:
                slot.d1x = d1x
                slot.d1y = d1y
                slot.d2x = d2x
                slot.d2y = d2y
                slot.d3x = d3x
                slot.d3y = d3y
                slot.d4x = d4x
                slot.d4y = d4y
                session.commit()
                return True
            return False

    def delete_slot_by_id(self, slot_id: int) -> bool:
        with self.db_context.get_session() as session:
            slot = session.query(Slot).filter(Slot.ID == slot_id).first()
            if slot:
                session.delete(slot)
                session.commit()
                return True
            return False