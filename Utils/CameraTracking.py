import cv2
import torch
import numpy as np
from ultralytics import YOLO
from collections import deque
from DataAccess.dbcontext import DBContext
from DataAccess.Repository.camera import CameraRepository
from DataAccess.Repository.CameraHaveSlot import CameraHaveSlotRepository
from DataAccess.Repository.manager import ManagerRepository
from DataAccess.Repository.pts import PTSRepository
from BusinessObject.models import Camera, CameraHaveSlot

# Kiểm tra và chọn thiết bị
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {device}")
accuracy_limit = 0.7

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

# Vùng check-in và slot (sẽ được load từ database)
check_in_quad = []
destination_zones = []
slot_ids = []

# Biến toàn cục cho MainMap và homography
main_map_img = None
homography_matrix = None

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
        if isinstance(quad_points[i], tuple):
            xi, yi = quad_points[i][0], quad_points[i][1]
        elif isinstance(quad_points[i], dict) and 'x' in quad_points[i] and 'y' in quad_points[i]:
            xi, yi = quad_points[i]['x'], quad_points[i]['y']
        else:
            print(f"Invalid point format at index {i}: {quad_points[i]}")
            return False

        if isinstance(quad_points[j], tuple):
            xj, yj = quad_points[j][0], quad_points[j][1]
        elif isinstance(quad_points[j], dict) and 'x' in quad_points[j] and 'y' in quad_points[j]:
            xj, yj = quad_points[j]['x'], quad_points[j]['y']
        else:
            print(f"Invalid point format at index {j}: {quad_points[j]}")
            return False

        if ((yi > center_y) != (yj > center_y)) and \
                (center_x < (xj - xi) * (center_y - yi) / (yj - yi + 1e-10) + xi):
            inside = not inside
        j = i

    return inside

# Load dữ liệu từ database
def load_camera_data(camera_id, manager_username):
    """Load thông tin camera, slot, MainMap và PTS từ database."""
    global check_in_quad, destination_zones, slot_ids, main_map_img, homography_matrix
    try:
        db_context = DBContext()
        camera_repo = CameraRepository(db_context)
        chs_repo = CameraHaveSlotRepository(db_context)
        manager_repo = ManagerRepository(db_context)
        pts_repo = PTSRepository(db_context)

        # Load camera data
        camera = camera_repo.get_camera_by_id(camera_id)
        if not camera:
            print(f"Camera with ID {camera_id} not found.")
            return None, []

        if all(getattr(camera, attr) is not None for attr in ['d1x', 'd1y', 'd2x', 'd2y', 'd3x', 'd3y', 'd4x', 'd4y']):
            check_in_quad = [
                (camera.d1x, camera.d1y),
                (camera.d2x, camera.d2y),
                (camera.d3x, camera.d3y),
                (camera.d4x, camera.d4y)
            ]
            print(f"Loaded check-in quadrilateral: {check_in_quad}")
        else:
            print("No valid check-in quadrilateral found for this camera.")
            check_in_quad = []

        # Load slot data
        camera_have_slots = chs_repo.get_by_camera_id(camera_id)
        destination_zones = []
        slot_ids = []
        for chs in camera_have_slots:
            if all(getattr(chs, attr) is not None for attr in ['d1x', 'd1y', 'd2x', 'd2y', 'd3x', 'd3y', 'd4x', 'd4y']):
                slot_quad = [
                    {'x': chs.d1x, 'y': chs.d1y},
                    {'x': chs.d2x, 'y': chs.d2y},
                    {'x': chs.d3x, 'y': chs.d3y},
                    {'x': chs.d4x, 'y': chs.d4y}
                ]
                destination_zones.append(slot_quad)
                slot_ids.append(chs.Slot_)
                print(f"Loaded slot quadrilateral for slot {chs.Slot_}: {slot_quad}")
            else:
                print(f"No valid quadrilateral found for slot {chs.Slot_}.")

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

        # Load PTS points and compute homography
        pts_records = pts_repo.get_pts_by_camera_id(camera_id)
        src_points = []
        dst_points = []
        for pts in pts_records:
            if all(attr is not None for attr in [pts.srcX, pts.srcY, pts.dstX, pts.dstY]):
                src_points.append([float(pts.srcX), float(pts.srcY)])
                dst_points.append([float(pts.dstX), float(pts.dstY)])
        print(f"Loaded {len(src_points)} PTS points for camera {camera_id}")
        print("src points:", src_points)
        print("dst points:", dst_points)

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
                    print("Homography matrix computed successfully:")
                    print(homography_matrix)
            except Exception as e:
                print(f"Error computing homography: {str(e)}")
                homography_matrix = None

        return camera.ValLink, destination_zones

    except Exception as e:
        print(f"Error loading camera data: {str(e)}")
        return None, []

# Vẽ vùng đích từ destination_zones với màu sắc
def draw_destination_zones(frame, detected_boxes):
    """Vẽ các vùng đích lên frame với màu xanh nếu trống, đỏ nếu có xe."""
    for idx, quad in enumerate(destination_zones):
        points = [(point['x'], point['y']) for point in quad]
        has_vehicle = False
        for box in detected_boxes:
            if is_in_quadrilateral(box, quad):
                has_vehicle = True
                break
        color = (0, 255, 0) if not has_vehicle else (0, 0, 255)
        for i in range(len(points)):
            cv2.line(frame, points[i], points[(i + 1) % len(points)], color, 2)
        avg_x = sum(p[0] for p in points) // len(points)
        avg_y = sum(p[1] for p in points) // len(points)
        slot_label = f"Slot {slot_ids[idx]}"
        cv2.putText(frame, slot_label, (avg_x - 30, avg_y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

# Vẽ chấm đỏ tại trung tâm box đã ánh xạ lên MainMap
def draw_mapped_boxes(main_map, detected_boxes, tracked_ids):
    """Vẽ chấm đỏ tại trung tâm của các bounding box đã ánh xạ lên MainMap."""
    if main_map is None or homography_matrix is None:
        print("Cannot draw mapped boxes: MainMap or homography matrix is not available")
        return main_map

    main_map_copy = main_map.copy()
    for box, obj_id in detected_boxes:
        x1, y1, x2, y2 = map(int, box)
        # Tính tâm của box
        center = np.array([[(x1 + x2) / 2, (y1 + y2) / 2]], dtype=np.float32).reshape(-1, 1, 2)

        # Ánh xạ tâm sang MainMap
        try:
            transformed_center = cv2.perspectiveTransform(center, homography_matrix)
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

def process_video(video_path, camera_id, manager_username):
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
            results = model.track(frame, persist=True)
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
                if check_in_quad and is_in_quadrilateral(box, check_in_quad):
                    if obj_id not in tracked_ids and tickets:
                        tracked_ids[obj_id] = tickets.popleft()
                        print(f"Assigned ticket {tracked_ids[obj_id]} to object ID {obj_id}")
                cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (255, 255, 255), 2)
                if obj_id in tracked_ids:
                    label_text = f"ID: {obj_id}, Ticket: {tracked_ids[obj_id]}"
                    cv2.putText(annotated_frame, label_text, (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    for quad in destination_zones:
                        if is_in_quadrilateral(box, quad) and tracked_ids[obj_id] == 1:
                            cv2.putText(annotated_frame, "Invalid Ticket", (x1, y1 - 30),
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                            break

        if check_in_quad:
            for i in range(len(check_in_quad)):
                cv2.line(annotated_frame, check_in_quad[i], check_in_quad[(i + 1) % len(check_in_quad)], (0, 255, 255), 2)
            avg_x = sum(p[0] for p in check_in_quad) // len(check_in_quad)
            avg_y = sum(p[1] for p in check_in_quad) // len(check_in_quad)
            cv2.putText(annotated_frame, "Check-in", (avg_x - 30, avg_y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 2)

        draw_destination_zones(annotated_frame, [box for box, _ in detected_boxes])

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

        # Vẽ MainMap với các chấm đỏ đã ánh xạ
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
    video_path, _ = load_camera_data(camera_id, manager_username)
    if video_path:
        process_video(video_path, camera_id, manager_username)
    else:
        print("No video path available to process.")