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
from DataAccess.Repository.CheckIn import CheckInRepository
from BusinessObject.models import Camera, Slot, CheckIn

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
checkin_quads_mainmap = {}  # Lưu tọa độ check-in từ MainMap
val_link_shape = (384, 640)  # Kích thước khung hình ValLink

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
def map_to_val_link(points, homography_matrix):
    """Ánh xạ tọa độ từ MainMap sang ValLink."""
    if homography_matrix is None or not points:
        print("Cannot map to ValLink: Homography matrix or points missing")
        return []

    transformed_points = []
    for point in points:
        src_point = np.array([[point[0], point[1]]], dtype=np.float32).reshape(-1, 1, 2)
        try:
            dst_point = cv2.perspectiveTransform(src_point, homography_matrix)
            x, y = int(dst_point[0][0][0]), int(dst_point[0][0][1])
            transformed_points.append((x, y))
            print(f"Transformed point {point} to ({x}, {y})")
        except Exception as e:
            print(f"Error transforming point {point}: {str(e)}")
            return []
    return transformed_points

# Load dữ liệu từ database
def load_camera_data(camera_id, manager_username):
    """Load thông tin camera, slot, check-in từ MainMap, và PTS từ database."""
    global main_map_img, homography_matrix, slot_quads_mainmap, checkin_quads_mainmap
    destination_zones = []
    checkin_zones = []
    slot_ids = []
    try:
        db_context = DBContext()
        camera_repo = CameraRepository(db_context)
        manager_repo = ManagerRepository(db_context)
        slot_repo = SlotRepository(db_context)
        pts_repo = PTSRepository(db_context)
        checkin_repo = CheckInRepository(db_context)

        # Load camera data
        camera = camera_repo.get_camera_by_id(camera_id)
        if not camera:
            print(f"Camera with ID {camera_id} not found.")
            return None, [], [], []

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
        slots = slot_repo.get_slots_by_manager(manager_username)
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
        slot_ids = list(slot_quads_mainmap.keys())
        print(f"Total slots loaded into slot_quads_mainmap: {len(slot_quads_mainmap)}")

        # Load check-in data từ MainMap cho manager
        checkins = checkin_repo.get_checkin_by_manager(manager_username)
        checkin_quads_mainmap = {}
        for checkin in checkins:
            if all(getattr(checkin, attr) is not None for attr in
                   ['d1x', 'd1y', 'd2x', 'd2y', 'd3x', 'd3y', 'd4x', 'd4y']):
                checkin_quads_mainmap[checkin.ID] = [
                    (checkin.d1x, checkin.d1y),
                    (checkin.d2x, checkin.d2y),
                    (checkin.d3x, checkin.d3y),
                    (checkin.d4x, checkin.d4y)
                ]
                print(f"Loaded check-in {checkin.ID} from MainMap: {checkin_quads_mainmap[checkin.ID]}")
            else:
                print(f"Check-in {checkin.ID} missing coordinates, skipping.")
        print(f"Total check-ins loaded into checkin_quads_mainmap: {len(checkin_quads_mainmap)}")

        # Load PTS points and compute homography (MainMap to ValLink)
        pts_records = pts_repo.get_pts_by_camera_id(camera_id)
        src_points = []
        dst_points = []
        for pts in pts_records:
            if all(attr is not None for attr in [pts.srcX, pts.srcY, pts.dstX, pts.dstY]):
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

        # Ánh xạ slot và check-in từ MainMap sang ValLink
        destination_zones = [map_to_val_link(quad, homography_matrix) for quad in slot_quads_mainmap.values()]
        checkin_zones = [map_to_val_link(quad, homography_matrix) for quad in checkin_quads_mainmap.values()]
        destination_zones = [zone for zone in destination_zones if zone]
        checkin_zones = [zone for zone in checkin_zones if zone]
        print(f"Final destination_zones for ValLink: {destination_zones}")
        print(f"Final checkin_zones for ValLink: {checkin_zones}")

        return camera.ValLink, destination_zones, checkin_zones, slot_ids

    except Exception as e:
        print(f"Error loading camera data: {str(e)}")
        return None, [], [], []

# Vẽ vùng đích và check-in từ destination_zones với màu sắc trên ValLink
def draw_destination_zones(frame, detected_boxes, slot_ids, destination_zones, checkin_zones):
    """Vẽ các vùng đích (slot) và check-in trên ValLink với màu xanh nếu trống, đỏ nếu có xe."""
    if not destination_zones or len(destination_zones) != len(slot_ids):
        print("No or mismatched destination zones to draw on ValLink")
        print(f"Destination zones: {destination_zones}")
        print(f"Slot IDs: {slot_ids}")
        return

    # Vẽ slot zones
    for idx, quad in enumerate(destination_zones):
        points = [(int(point[0]), int(point[1])) for point in quad if 0 <= point[0] < frame.shape[1] and 0 <= point[1] < frame.shape[0]]
        if len(points) < 3:
            print(f"Invalid quad for slot {slot_ids[idx]} on ValLink: {points}, skipping")
            continue
        has_vehicle = any(is_in_quadrilateral(box, points) for box, _ in detected_boxes)
        color = (0, 255, 0) if not has_vehicle else (0, 0, 255)
        for i in range(len(points)):
            cv2.line(frame, points[i], points[(i + 1) % len(points)], color, 2)
        avg_x = sum(p[0] for p in points) // len(points)
        avg_y = sum(p[1] for p in points) // len(points)
        cv2.putText(frame, f"Slot {slot_ids[idx]}", (avg_x - 30, avg_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Vẽ check-in zones
    for idx, quad in enumerate(checkin_zones):
        points = [(int(point[0]), int(point[1])) for point in quad if 0 <= point[0] < frame.shape[1] and 0 <= point[1] < frame.shape[0]]
        if len(points) < 3:
            print(f"Invalid quad for check-in on ValLink: {points}, skipping")
            continue
        has_vehicle = any(is_in_quadrilateral(box, points) for box, _ in detected_boxes)
        color = (0, 255, 255)  # Yellow for check-in zones
        for i in range(len(points)):
            cv2.line(frame, points[i], points[(i + 1) % len(points)], color, 2)
        avg_x = sum(p[0] for p in points) // len(points)
        avg_y = sum(p[1] for p in points) // len(points)
        cv2.putText(frame, f"CheckIn", (avg_x - 30, avg_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# Vẽ chấm đỏ tại trung tâm box và tứ giác slot/check-in trên MainMap với màu tương tự ValLink
def draw_mapped_boxes(main_map, detected_boxes, tracked_ids):
    """Vẽ tứ giác slot và check-in, chấm đỏ tại trung tâm của các bounding box đã ánh xạ lên MainMap."""
    if main_map is None or homography_matrix is None:
        print("Cannot draw mapped boxes: MainMap or homography matrix is not available")
        return main_map

    try:
        inv_homography = np.linalg.inv(homography_matrix)
    except np.linalg.LinAlgError:
        print("Cannot invert homography matrix for drawing on MainMap")
        return main_map

    main_map_copy = main_map.copy()

    # Vẽ tứ giác slot từ slot_quads_mainmap với màu dựa trên trạng thái
    for slot_id, quad in slot_quads_mainmap.items():
        points = [(int(point[0]), int(point[1])) for point in quad if
                  0 <= point[0] < main_map.shape[1] and 0 <= point[1] < main_map.shape[0]]
        if len(points) < 3:
            print(f"Invalid quad for slot {slot_id} on MainMap: {points}, skipping")
            continue

        # Kiểm tra occupancy bằng cách ánh xạ box từ ValLink về MainMap
        has_vehicle = False
        for box, _ in detected_boxes:
            x1, y1, x2, y2 = map(int, box)
            center = np.array([[(x1 + x2) / 2, (y1 + y2) / 2]], dtype=np.float32).reshape(-1, 1, 2)
            try:
                transformed_center = cv2.perspectiveTransform(center, inv_homography)
                center_x, center_y = int(transformed_center[0][0][0]), int(transformed_center[0][0][1])
                if is_in_quadrilateral((center_x, center_y, center_x, center_y), points):  # Use point check
                    has_vehicle = True
                    break
            except Exception as e:
                print(f"Error transforming center for occupancy check of slot {slot_id}: {str(e)}")

        # Chọn màu: xanh lá nếu trống, đỏ nếu có xe
        color = (0, 255, 0) if not has_vehicle else (0, 0, 255)
        for i in range(len(points)):
            cv2.line(main_map_copy, points[i], points[(i + 1) % len(points)], color, 2)
        avg_x = sum(p[0] for p in points) // len(points)
        avg_y = sum(p[1] for p in points) // len(points)
        cv2.putText(main_map_copy, f"Slot {slot_id}", (avg_x - 30, avg_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    # Vẽ tứ giác check-in từ checkin_quads_mainmap với màu vàng
    for checkin_id, quad in checkin_quads_mainmap.items():
        points = [(int(point[0]), int(point[1])) for point in quad if
                  0 <= point[0] < main_map.shape[1] and 0 <= point[1] < main_map.shape[0]]
        if len(points) < 3:
            print(f"Invalid quad for check-in {checkin_id} on MainMap: {points}, skipping")
            continue
        color = (0, 255, 255)  # Yellow for check-in zones
        for i in range(len(points)):
            cv2.line(main_map_copy, points[i], points[(i + 1) % len(points)], color, 2)
        avg_x = sum(p[0] for p in points) // len(points)
        avg_y = sum(p[1] for p in points) // len(points)
        cv2.putText(main_map_copy, f"CheckIn {checkin_id}", (avg_x - 30, avg_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Vẽ chấm đỏ tại tâm của các bounding box đã ánh xạ
    for box, obj_id in detected_boxes:
        x1, y1, x2, y2 = map(int, box)
        center = np.array([[(x1 + x2) / 2, (y1 + y2) / 2]], dtype=np.float32).reshape(-1, 1, 2)
        try:
            transformed_center = cv2.perspectiveTransform(center, inv_homography)
            center_x, center_y = int(transformed_center[0][0][0]), int(transformed_center[0][0][1])
            cv2.circle(main_map_copy, (center_x, center_y), radius=5, color=(0, 0, 255), thickness=-1)
            if obj_id in tracked_ids:
                label_text = f"ID: {obj_id}, Ticket: {tracked_ids[obj_id]}"
                cv2.putText(main_map_copy, label_text, (center_x - 30, center_y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        except Exception as e:
            print(f"Error transforming center of box {box}: {str(e)}")

    return main_map_copy

# Dictionary lưu trữ các object đã theo dõi
tracked_ids = {}

def process_video(video_path, camera_id, manager_username, destination_zones, checkin_zones, slot_ids):
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
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Đặt lại trạng thái theo dõi của YOLO
    try:
        model.predictor.trackers[0].reset()
        model.reset()
        print(f"Reset YOLO tracking state for Camera ID {camera_id}")
    except AttributeError:
        print("YOLO model does not support reset. Proceeding without reset.")

    # Khởi tạo tickets
    tickets.clear()
    add_ticket(0)  # Valid ticket
    add_ticket(1)  # Invalid ticket
    add_ticket(1)
    add_ticket(1)
    add_ticket(0)
    add_ticket(0)
    add_ticket(1)
    add_ticket(0)
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

                # Kiểm tra check-in zones để cấp ticket
                for quad in checkin_zones:
                    if is_in_quadrilateral(box, quad) and obj_id not in tracked_ids and tickets:
                        tracked_ids[obj_id] = tickets.popleft()
                        print(f"Vehicle ID {obj_id} passed check-in, assigned ticket: {tracked_ids[obj_id]}")

                # Kiểm tra slot zones để xác nhận ticket
                for quad in destination_zones:
                    if is_in_quadrilateral(box, quad):
                        if obj_id in tracked_ids and tracked_ids[obj_id] == 1:
                            cv2.putText(annotated_frame, "Invalid Ticket", (x1, y1 - 30),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
                if obj_id in tracked_ids:
                    label_text = f"ID: {obj_id}, Ticket: {tracked_ids[obj_id]}"
                    cv2.putText(annotated_frame, label_text, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # Vẽ các slot và check-in từ MainMap lên ValLink
        draw_destination_zones(annotated_frame, detected_boxes, slot_ids, destination_zones, checkin_zones)

        total_slots = len(destination_zones)
        occupied_slots = sum(1 for quad in destination_zones for box, _ in detected_boxes if is_in_quadrilateral(box, quad))
        available_slots = total_slots - occupied_slots
        cv2.putText(annotated_frame, f"Available Slots: {available_slots}/{total_slots}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        # Vẽ MainMap với các tứ giác slot và check-in, chấm đỏ đã ánh xạ
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
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    print("Video processing completed.")
    return True

if __name__ == "__main__":
    camera_id = int(input("Enter Camera ID: "))
    manager_username = input("Enter Manager Username: ")
    video_path, destination_zones, checkin_zones, slot_ids = load_camera_data(camera_id, manager_username)
    if video_path:
        process_video(video_path, camera_id, manager_username, destination_zones, checkin_zones, slot_ids)
    else:
        print("No video path available to process.")