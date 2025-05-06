import cv2
import torch
import numpy as np
from ultralytics import YOLO
from collections import deque
from DataAccess.dbcontext import DBContext
from DataAccess.Repository.camera import CameraRepository
from DataAccess.Repository.manager import ManagerRepository
from DataAccess.Repository.slot import SlotRepository
from DataAccess.Repository.pts import PTSRepository
from BusinessObject.models import Camera, Slot

# Kiểm tra và chọn thiết bị
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")
accuracy_limit = 0.3

# Load mô hình YOLO
try:
    model = YOLO('car-100_v3.pt')
except Exception as e:
    print(f"Error loading model: {e}")

# Hàng đợi ticket
tickets = deque()


def add_ticket(number):
    """Thêm ticket vào hàng đợi."""
    tickets.append(number)


# Biến toàn cục
main_map_img = None
homography_matrix = None
slot_quads_mainmap = {}  # Lưu tọa độ slot từ MainMap
val_link_shape = (384, 640)  # Kích thước khung hình ValLink (dựa trên log: 384x640)


# Hàm kiểm tra xem box có nằm trong vùng tứ giác không
def is_in_quadrilateral(box, quad_points):
    """Kiểm tra xem trung tâm của box có nằm trong tứ giác không."""
    if not quad_points or len(quad_points) < 3:
        return False

    x1, y1, x2, y2 = map(int, box)
    center_x = (x1 + x2) // 2
    center_y = (y1 + y2) // 2
    inside = False
    j = len(quad_points) - 1

    for i in range(len(quad_points)):
        xi, yi = quad_points[i][0], quad_points[i][1]
        xj, yj = quad_points[j][0], quad_points[j][1]
        if ((yi > center_y) != (yj > center_y)) and \
                (center_x < (xj - xi) * (center_y - yi) / (yj - yi + 1e-10) + xi):
            inside = not inside
        j = i

    return inside


# Hàm ánh xạ tọa độ từ MainMap sang ValLink
def map_slot_to_val_link(slot_id, slot_quads):
    """Ánh xạ trực tiếp tọa độ slot từ MainMap sang ValLink nếu hợp lệ."""
    global homography_matrix
    if homography_matrix is None or slot_id not in slot_quads:
        print(f"Cannot map slot {slot_id} to ValLink: Homography matrix or slot data missing")
        return []

    quad_points = slot_quads[slot_id]
    print(f"Original slot {slot_id} coordinates on MainMap: {quad_points}")

    transformed_points = []
    for point in quad_points:
        src_point = np.array([[point[0], point[1]]], dtype=np.float32).reshape(-1, 1, 2)
        try:
            dst_point = cv2.perspectiveTransform(src_point, homography_matrix)
            x, y = int(dst_point[0][0][0]), int(dst_point[0][0][1])
            transformed_points.append((x, y))
            print(f"Transformed point {point} to ({x}, {y}) for slot {slot_id}")
        except Exception as e:
            print(f"Error transforming point {point} for slot {slot_id}: {str(e)}")
            return []

    if len(transformed_points) < 3:
        print(f"Insufficient valid points for slot {slot_id} after transformation: {transformed_points}")
        return []
    return transformed_points


# Load dữ liệu từ database
def load_camera_data(camera_id, manager_username):
    """Load thông tin camera, slot từ MainMap, và PTS từ database."""
    global main_map_img, homography_matrix, slot_quads_mainmap
    destination_zones = []
    slot_ids = []
    try:
        db_context = DBContext()
        camera_repo = CameraRepository(db_context)
        manager_repo = ManagerRepository(db_context)
        slot_repo = SlotRepository(db_context)
        pts_repo = PTSRepository(db_context)

        # Load camera data
        camera = camera_repo.get_camera_by_id(camera_id)
        if not camera:
            print(f"Camera with ID {camera_id} not found.")
            return None, [], []

        # Load MainMap
        manager = manager_repo.get_manager_by_username(manager_username)
        if not manager or not manager.MainMap:
            print("No valid MainMap found for manager.")
            main_map_img = None
        else:
            main_map_img = cv2.imread(manager.MainMap, -1)
            if main_map_img is None:
                print(f"Failed to load MainMap from {manager.MainMap}")
            else:
                print(f"Loaded MainMap from {manager.MainMap}")

        # Load slot data từ MainMap cho manager
        slots = slot_repo.get_slots_by_manager(manager_username)  # Lấy tất cả slot của manager
        slot_quads_mainmap = {}
        for slot in slots:
            if all(getattr(slot, attr) is not None for attr in
                   ['d1x', 'd1y', 'd2x', 'd2y', 'd3x', 'd3y', 'd4x', 'd4y']):
                slot_quads_mainmap[slot.ID] = [
                    (slot.d1x, slot.d1y),
                    (slot.d2x, slot.d2y),
                    (slot.d3x, slot.d3y),
                    (slot.d4x, slot.d4y)
                ]
                print(f"Loaded slot {slot.ID} from MainMap: {slot_quads_mainmap[slot.ID]}")
            else:
                print(f"Slot {slot.ID} missing coordinates, skipping.")
        print(f"Total slots loaded into slot_quads_mainmap: {len(slot_quads_mainmap)}")

        # Tạo danh sách slot IDs từ tất cả slots của manager
        slot_ids = list(slot_quads_mainmap.keys())
        print(f"All slot IDs for manager {manager_username}: {slot_ids}")
        print(f"Total slot IDs: {len(slot_ids)}")

        # Load PTS points and compute homography (MainMap to ValLink)
        pts_records = pts_repo.get_pts_by_camera_id(camera_id)
        src_points = []
        dst_points = []
        for pts in pts_records:
            if all(attr is not None for attr in [pts.srcX, pts.srcY, pts.dstX, pts.dstY]):
                # MainMap (src) -> ValLink (dst)
                src_points.append([float(pts.dstX), float(pts.dstY)])
                dst_points.append([float(pts.srcX), float(pts.srcY)])
        print(f"Loaded {len(src_points)} PTS points for camera {camera_id}")
        print("MainMap points (src):", src_points)
        print("ValLink points (dst):", dst_points)

        if len(src_points) < 4 or len(dst_points) < 4:
            print("Warning: At least 4 point pairs are required for homography. Mapping disabled.")
            homography_matrix = None
        elif len(src_points) != len(dst_points):
            print(f"Error: Mismatched point counts (src: {len(src_points)}, dst: {len(dst_points)})")
            homography_matrix = None
        else:
            try:
                src_pts = np.array(src_points, dtype=np.float32).reshape(-1, 1, 2)
                dst_pts = np.array(dst_points, dtype=np.float32).reshape(-1, 1, 2)
                homography_matrix, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
                if homography_matrix is None:
                    print("Error: Homography calculation failed")
                else:
                    print("Homography matrix (MainMap to ValLink) computed successfully:")
                    print(homography_matrix)
            except Exception as e:
                print(f"Error computing homography: {str(e)}")
                homography_matrix = None

        # Ánh xạ trực tiếp từ MainMap sang ValLink
        destination_zones = []
        for slot_id in slot_ids:
            if slot_id not in slot_quads_mainmap:
                print(f"Slot {slot_id} not found in slot_quads_mainmap, skipping mapping to ValLink")
                continue
            transformed_quad = map_slot_to_val_link(slot_id, slot_quads_mainmap)
            if transformed_quad:
                destination_zones.append(transformed_quad)
                print(f"Mapped slot {slot_id} to ValLink: {transformed_quad}")
            else:
                print(f"Failed to map slot {slot_id} to ValLink")

        print(f"Final destination_zones for ValLink: {destination_zones}")
        print(f"Number of destination zones: {len(destination_zones)}, Number of slot IDs: {len(slot_ids)}")
        return camera.ValLink, destination_zones, slot_ids

    except Exception as e:
        print(f"Error loading camera data: {str(e)}")
        return None, [], []


# Vẽ vùng đích từ destination_zones với màu sắc trên ValLink
def draw_destination_zones(frame, detected_boxes, slot_ids, destination_zones):
    """Vẽ các vùng đích (slot) từ MainMap lên ValLink với màu xanh nếu trống, đỏ nếu có xe."""
    if not destination_zones or len(destination_zones) != len(slot_ids):
        print("No or mismatched destination zones to draw on ValLink")
        print(f"Destination zones: {destination_zones}")
        print(f"Slot IDs: {slot_ids}")
        return

    for idx, quad in enumerate(destination_zones):
        # Kiểm tra và lọc tọa độ hợp lệ
        points = [(int(point[0]), int(point[1])) for point in quad]
        if len(points) < 3:
            print(f"Invalid quad for slot {slot_ids[idx]} on ValLink: {points}, skipping")
            continue

        # Kiểm tra xem slot có xe hay không
        has_vehicle = False
        for box in detected_boxes:
            if is_in_quadrilateral(box, points):
                has_vehicle = True
                break

        # Chọn màu: xanh lá nếu trống, đỏ nếu có xe
        color = (0, 255, 0) if not has_vehicle else (0, 0, 255)

        # Vẽ tứ giác slot trên ValLink
        for i in range(len(points)):
            cv2.line(frame, points[i], points[(i + 1) % len(points)], color, 2)

        # Gắn nhãn slot
        avg_x = sum(p[0] for p in points) // len(points)
        avg_y = sum(p[1] for p in points) // len(points)
        slot_label = f"Slot {slot_ids[idx]}"
        cv2.putText(frame, slot_label, (avg_x - 30, avg_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


# Vẽ chấm đỏ tại trung tâm box và tứ giác slot trên MainMap
def draw_mapped_boxes(main_map, detected_boxes, tracked_ids):
    """Vẽ tứ giác slot và chấm đỏ tại trung tâm của các bounding box đã ánh xạ lên MainMap."""
    if main_map is None or homography_matrix is None:
        print("Cannot draw mapped boxes: MainMap or homography matrix is not available")
        return main_map

    # Tính homography ngược (ValLink -> MainMap)
    try:
        inv_homography = np.linalg.inv(homography_matrix)
    except np.linalg.LinAlgError:
        print("Cannot invert homography matrix for drawing on MainMap")
        return main_map

    main_map_copy = main_map.copy()

    # Vẽ tứ giác slot từ slot_quads_mainmap
    if not slot_quads_mainmap:
        print("No slots available to draw on MainMap")
    else:
        for slot_id, quad in slot_quads_mainmap.items():
            points = [(int(point[0]), int(point[1])) for point in quad if
                      0 <= point[0] < main_map.shape[1] and 0 <= point[1] < main_map.shape[0]]
            if len(points) < 3:
                print(f"Invalid quad for slot {slot_id} on MainMap: {points}, skipping")
                continue
            for i in range(len(points)):
                cv2.line(main_map_copy, points[i], points[(i + 1) % len(points)], (255, 0, 0), 2)
            avg_x = sum(p[0] for p in points) // len(points)
            avg_y = sum(p[1] for p in points) // len(points)
            slot_label = f"Slot {slot_id}"
            cv2.putText(main_map_copy, slot_label, (avg_x - 30, avg_y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Vẽ chấm đỏ tại tâm của các bounding box đã ánh xạ
    for box, obj_id in detected_boxes:
        x1, y1, x2, y2 = map(int, box)
        # Tính tâm của box
        center = np.array([[(x1 + x2) / 2, (y1 + y2) / 2]], dtype=np.float32).reshape(-1, 1, 2)

        # Ánh xạ tâm sang MainMap
        try:
            transformed_center = cv2.perspectiveTransform(center, inv_homography)
            center_x, center_y = int(transformed_center[0][0][0]), int(transformed_center[0][0][1])
            # Vẽ chấm đỏ tại tâm
            cv2.circle(main_map_copy, (center_x, center_y), radius=5, color=(0, 0, 255), thickness=-1)
            # Thêm nhãn với ID và ticket
            if obj_id in tracked_ids:
                label_text = f"ID: {obj_id}, Ticket: {tracked_ids[obj_id]}"
                cv2.putText(main_map_copy, label_text, (center_x - 30, center_y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        except Exception as e:
            print(f"Error transforming center of box {box}: {str(e)}")

    return main_map_copy


# Dictionary lưu trữ các object đã theo dõi
tracked_ids = {}


def process_video(video_path, camera_id, manager_username, destination_zones, slot_ids):
    """Xử lý video với YOLO tracking và ánh xạ lên MainMap."""
    global model, main_map_img, homography_matrix
    torch.cuda.empty_cache()

    # Kiểm tra video trước khi mở
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file: {video_path}")
        return False

    # Đọc khung hình đầu tiên để kiểm tra kích thước
    ret, first_frame = cap.read()
    if not ret or first_frame is None:
        print(f"Error reading first frame from video: {video_path}")
        cap.release()
        return False
    print(f"Video resolution for Camera ID {camera_id}: {first_frame.shape}")
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Đặt lại về khung đầu tiên

    # Đặt lại trạng thái theo dõi của YOLO
    try:
        model.predictor.trackers[0].reset()
        model.reset()
        print(f"Reset YOLO tracking state for Camera ID {camera_id}")
    except AttributeError:
        print("YOLO model does not support reset. Proceeding without reset.")

    # Khởi tạo tickets
    tickets.clear()
    add_ticket(0)
    add_ticket(1)
    add_ticket(1)
    add_ticket(1)
    add_ticket(1)
    add_ticket(0)
    add_ticket(0)
    add_ticket(0)
    add_ticket(0)
    add_ticket(1)
    add_ticket(0)
    add_ticket(1)
    add_ticket(1)
    add_ticket(0)
    tracked_ids.clear()

    # Thiết lập cửa sổ OpenCV
    cv2.namedWindow(f"YOLO Tracking - Camera ID {camera_id}")
    cv2.moveWindow(f"YOLO Tracking - Camera ID {camera_id}", 80, 80)
    if main_map_img is not None:
        cv2.namedWindow("MainMap")
        cv2.moveWindow("MainMap", 780, 80)

    frame_count = 0
    while cap.isOpened():
        success, frame = cap.read()
        if not success or frame is None:
            print(f"End of video reached or invalid frame at frame {frame_count}.")
            break

        frame_count += 1
        # Kiểm tra kích thước khung hình
        if frame.shape[0] <= 0 or frame.shape[1] <= 0:
            print(f"Invalid frame size at frame {frame_count}: {frame.shape}")
            continue

        try:
            results = model.track(frame, tracker="botsort.yaml", persist=True, conf=0.75, iou=0.45)
        except Exception as e:
            print(f"Error during tracking (frame {frame_count}): {e}")
            continue

        annotated_frame = frame.copy()
        detected_boxes = []
        if results[0].boxes is not None and results[0].boxes.id is not None:
            for box, conf, obj_id in zip(results[0].boxes.xyxy, results[0].boxes.conf, results[0].boxes.id):
                if conf <= accuracy_limit:
                    continue
                obj_id = int(obj_id)
                detected_boxes.append((box, obj_id))
                x1, y1, x2, y2 = map(int, box)
                for quad in destination_zones:
                    if is_in_quadrilateral(box, quad):
                        if obj_id not in tracked_ids and tickets:
                            tracked_ids[obj_id] = tickets.popleft()
                            print(f"Assigned ticket {tracked_ids[obj_id]} to object ID {obj_id}")
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
                if obj_id in tracked_ids:
                    label_text = f"ID: {obj_id}, Ticket: {tracked_ids[obj_id]}"
                    cv2.putText(annotated_frame, label_text, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    if tracked_ids[obj_id] == 1:
                        cv2.putText(annotated_frame, "Invalid Ticket", (x1, y1 - 30),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Vẽ các slot từ MainMap lên ValLink
        draw_destination_zones(annotated_frame, [box for box, _ in detected_boxes], slot_ids, destination_zones)

        total_slots = len(destination_zones)
        occupied_slots = 0
        for quad in destination_zones:
            for box, _ in detected_boxes:
                if is_in_quadrilateral(box, quad):
                    occupied_slots += 1
                    break
        available_slots = total_slots - occupied_slots
        cv2.putText(annotated_frame, f"Available Slots: {available_slots}/{total_slots}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Vẽ MainMap với các tứ giác slot và chấm đỏ đã ánh xạ
        if main_map_img is not None:
            mapped_frame = draw_mapped_boxes(main_map_img, detected_boxes, tracked_ids)
            cv2.imshow("MainMap", mapped_frame)

        cv2.imshow(f"YOLO Tracking - Camera ID {camera_id}", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyWindow(f"YOLO Tracking - Camera ID {camera_id}")
    if main_map_img is not None:
        cv2.destroyWindow("MainMap")
    # Giải phóng bộ nhớ GPU
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    print("Video processing completed.")
    return True


if __name__ == "__main__":
    camera_id = int(input("Enter Camera ID: "))
    manager_username = input("Enter Manager Username: ")
    video_path, destination_zones, slot_ids = load_camera_data(camera_id, manager_username)
    if video_path:
        process_video(video_path, camera_id, manager_username, destination_zones, slot_ids)
    else:
        print("No video path available to process.")