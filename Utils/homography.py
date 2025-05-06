import numpy as np
import cv2 as cv
from BusinessObject.models import PTS
from DataAccess.dbcontext import DBContext
from DataAccess.Repository.pts import PTSRepository
import os

def run_homography(camera_id: int, val_link: str, main_map: str, db_context: DBContext):
    drawing = False
    src_x, src_y = -1, -1
    dst_x, dst_y = -1, -1
    src_list = []
    dst_list = []
    selected_idx = -1  # Chỉ số của điểm đang chọn để chỉnh sửa/xóa
    pts_repo = PTSRepository(db_context)

    # Helper function to check if a file is a video
    def is_video_file(filepath: str) -> bool:
        video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.wmv'}
        return os.path.splitext(filepath)[1].lower() in video_extensions

    # Load source (ValLink: image or video)
    try:
        print(f"Loading source from {val_link}")
        if is_video_file(val_link):
            cap = cv.VideoCapture(val_link)
            if not cap.isOpened():
                raise ValueError(f"Cannot open video file from {val_link}")
            ret, src = cap.read()
            if not ret:
                raise ValueError(f"Cannot read first frame from video {val_link}")
            cap.release()
        else:
            src = cv.imread(val_link, -1)
            if src is None:
                raise ValueError(f"Cannot load image from {val_link}")
        if src.shape[0] <= 0 or src.shape[1] <= 0:
            raise ValueError(f"Invalid source image dimensions: {src.shape}")
        src_copy = src.copy()
        print("Source image/video loaded successfully")
    except Exception as e:
        print(f"Error loading source image/video: {str(e)}")
        raise

    # Load destination (MainMap: image)
    try:
        print(f"Loading destination from {main_map}")
        dst = cv.imread(main_map, -1)
        if dst is None:
            raise ValueError(f"Cannot load destination image from {main_map}")
        if dst.shape[0] <= 0 or dst.shape[1] <= 0:
            raise ValueError(f"Invalid destination image dimensions: {dst.shape}")
        dst_copy = dst.copy()
        print("Destination image loaded successfully")
    except Exception as e:
        print(f"Error loading destination image: {str(e)}")
        raise

    # Kiểm tra kích thước tương thích
    if src.shape[1] != dst.shape[1] or src.shape[0] != dst.shape[0]:
        print(f"Warning: Source ({src.shape}) and destination ({dst.shape}) dimensions differ. Homography may fail.")

    # Load existing PTS points for the camera
    try:
        print(f"Loading PTS points for camera {camera_id}")
        pts_records = pts_repo.get_pts_by_camera_id(camera_id)
        for pts in pts_records:
            if all(attr is not None for attr in [pts.srcX, pts.srcY, pts.dstX, pts.dstY]):
                src_point = [float(pts.srcX), float(pts.srcY)]
                dst_point = [float(pts.dstX), float(pts.dstY)]
                if len(src_point) == 2 and len(dst_point) == 2 and 0 <= src_point[0] < src.shape[1] and 0 <= src_point[1] < src.shape[0] and 0 <= dst_point[0] < dst.shape[1] and 0 <= dst_point[1] < dst.shape[0]:
                    src_list.append(src_point)
                    dst_list.append(dst_point)
                    cv.circle(src_copy, (int(pts.srcX), int(pts.srcY)), 5, (0, 255, 0), -1)
                    cv.circle(dst_copy, (int(pts.dstX), int(pts.dstY)), 5, (0, 255, 0), -1)
                else:
                    print(f"Invalid or out-of-bounds PTS point for camera {camera_id}: src={src_point}, dst={dst_point}")
        print(f"Loaded {len(src_list)} PTS points for camera {camera_id}")
        print("src points:", src_list)
        print("dst points:", dst_list)
    except Exception as e:
        print(f"Error loading PTS points: {str(e)}")
        raise

    # Mouse callback functions
    def select_points_src(event, x, y, flags, param):
        nonlocal src_x, src_y, drawing, selected_idx
        print(f"Mouse event on src: event={event}, x={x}, y={y}")
        if event == cv.EVENT_LBUTTONDOWN:
            drawing = True
            src_x, src_y = x, y
            # Kiểm tra xem có chọn lại điểm cũ không
            for i, (sx, sy) in enumerate(src_list):
                if abs(sx - x) < 10 and abs(sy - y) < 10:
                    selected_idx = i
                    print(f"Selected existing point at index {i}")
                    break
            else:
                selected_idx = -1
                cv.circle(src_copy, (x, y), 5, (0, 0, 255), -1)
        elif event == cv.EVENT_LBUTTONUP:
            drawing = False

    def select_points_dst(event, x, y, flags, param):
        nonlocal dst_x, dst_y, drawing, selected_idx
        print(f"Mouse event on dst: event={event}, x={x}, y={y}")
        if event == cv.EVENT_LBUTTONDOWN:
            drawing = True
            dst_x, dst_y = x, y
            # Kiểm tra xem có chọn lại điểm cũ không
            for i, (dx, dy) in enumerate(dst_list):
                if abs(dx - x) < 10 and abs(dy - y) < 10:
                    selected_idx = i
                    print(f"Selected existing point at index {i}")
                    break
            else:
                selected_idx = -1
                cv.circle(dst_copy, (x, y), 5, (0, 0, 255), -1)
        elif event == cv.EVENT_LBUTTONUP:
            drawing = False

    def get_plan_view(src, dst):
        print("Entering get_plan_view")
        if len(src_list) < 4 or len(dst_list) < 4:
            print("Error: At least 4 point pairs are required for homography")
            return None, None
        if len(src_list) != len(dst_list):
            print(f"Error: Mismatched point counts (src: {len(src_list)}, dst: {len(dst_list)})")
            return None, None
        try:
            src_pts = np.array(src_list, dtype=np.float32).reshape(-1, 1, 2)
            dst_pts = np.array(dst_list, dtype=np.float32).reshape(-1, 1, 2)
            print("src_pts:", src_pts)
            print("dst_pts:", dst_pts)
            H, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)
            if H is None:
                print("Error: Homography calculation failed")
                return None, None
            print("Homography matrix:")
            print(H)
            plan_view = cv.warpPerspective(src, H, (dst.shape[1], dst.shape[0]))
            print("Plan view generated successfully")
            return plan_view, H
        except Exception as e:
            print(f"Error in get_plan_view: {str(e)}")
            return None, None

    def merge_views(src, dst):
        print("Entering merge_views")
        plan_view, _ = get_plan_view(src, dst)  # Sửa ở đây để unpack đúng 2 giá trị
        if plan_view is None:
            print("Cannot merge views: Plan view generation failed")
            return None
        try:
            mask = np.all(plan_view == 0, axis=2)
            plan_view[mask] = dst[mask]
            print("Views merged successfully")
            return plan_view
        except Exception as e:
            print(f"Error in merge_views: {str(e)}")
            return None

    try:
        print("Setting up OpenCV windows")
        cv.namedWindow('src')
        cv.moveWindow("src", 80, 80)
        cv.setMouseCallback('src', select_points_src)

        cv.namedWindow('dst')
        cv.moveWindow("dst", 780, 80)
        cv.setMouseCallback('dst', select_points_dst)

        print("Entering main loop")
        while True:
            cv.imshow('src', src_copy)
            cv.imshow('dst', dst_copy)
            k = cv.waitKey(1) & 0xFF
            print(f"Key pressed: {k}")
            if k == ord('s'):
                print('Saving points')
                if src_x == -1 or src_y == -1 or dst_x == -1 or dst_y == -1:
                    print("Please select both src and dst points before saving")
                    continue
                print(f"Selected points: src=({src_x}, {src_y}), dst=({dst_x}, {dst_y})")
                if selected_idx >= 0:
                    # Cập nhật điểm hiện có
                    src_list[selected_idx] = [float(src_x), float(src_y)]
                    dst_list[selected_idx] = [float(dst_x), float(dst_y)]
                    # Cập nhật trong database
                    pts = pts_repo.get_pts_by_camera_id(camera_id)[selected_idx]
                    pts.srcX = float(src_x)
                    pts.srcY = float(src_y)
                    pts.dstX = float(dst_x)
                    pts.dstY = float(dst_y)
                    pts_repo.update_pts(pts)
                    print(f"Updated PTS at index {selected_idx}")
                else:
                    # Thêm điểm mới
                    src_list.append([float(src_x), float(src_y)])
                    dst_list.append([float(dst_x), float(dst_y)])
                    pts = PTS(
                        srcX=float(src_x),
                        srcY=float(src_y),
                        dstX=float(dst_x),
                        dstY=float(dst_y),
                        Camera_=camera_id
                    )
                    pts_repo.add_pts(pts)
                    print(f"Saved new PTS for camera {camera_id}")
                # Vẽ lại điểm đã lưu
                cv.circle(src_copy, (src_x, src_y), 5, (0, 255, 0), -1)
                cv.circle(dst_copy, (dst_x, dst_y), 5, (0, 255, 0), -1)
                src_x, src_y, dst_x, dst_y = -1, -1, -1, -1
                selected_idx = -1
                print("Points saved and reset")

            elif k == ord('d'):
                print('Deleting selected point')
                if selected_idx >= 0 and selected_idx < len(src_list):
                    pts = pts_repo.get_pts_by_camera_id(camera_id)[selected_idx]
                    pts_repo.delete_pts(pts.ID)
                    del src_list[selected_idx]
                    del dst_list[selected_idx]
                    src_copy = src.copy()
                    dst_copy = dst.copy()
                    for sx, sy in src_list:
                        cv.circle(src_copy, (int(sx), int(sy)), 5, (0, 255, 0), -1)
                    for dx, dy in dst_list:
                        cv.circle(dst_copy, (int(dx), int(dy)), 5, (0, 255, 0), -1)
                    selected_idx = -1
                    print(f"Deleted point at index {selected_idx}")
                else:
                    print("No point selected to delete")

            elif k == ord('h'):
                print('Creating plan view')
                plan_view, H = get_plan_view(src, dst)
                if plan_view is not None:
                    cv.imshow("plan view", plan_view)
                    print("Homography matrix saved in memory for use")

            elif k == ord('m'):
                print('Merging views')
                merge = merge_views(src, dst)
                if merge is not None:
                    cv.imshow("merge", merge)
            elif k == ord('q') or k == 27:  # 'q' or Esc to exit
                print("Exiting homography tool")
                break

    except Exception as e:
        print(f"Error in homography main loop: {str(e)}")
        import traceback
        print("Stack trace:")
        print(traceback.format_exc())
        raise
    finally:
        print("Cleaning up OpenCV windows")
        cv.destroyAllWindows()