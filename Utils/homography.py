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
            cap.release()
            if not ret:
                raise ValueError(f"Cannot read first frame from video {val_link}")
        else:
            src = cv.imread(val_link, -1)
            if src is None:
                raise ValueError(f"Cannot load image from {val_link}")
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
        dst_copy = dst.copy()
        print("Destination image loaded successfully")
    except Exception as e:
        print(f"Error loading destination image: {str(e)}")
        raise

    # Load existing PTS points for the camera
    try:
        print(f"Loading PTS points for camera {camera_id}")
        pts_records = pts_repo.get_pts_by_camera_id(camera_id)
        for pts in pts_records:
            if all(attr is not None for attr in [pts.srcX, pts.srcY, pts.dstX, pts.dstY]):
                src_point = [float(pts.srcX), float(pts.srcY)]
                dst_point = [float(pts.dstX), float(pts.dstY)]
                # Validate point format
                if len(src_point) == 2 and len(dst_point) == 2:
                    src_list.append(src_point)
                    dst_list.append(dst_point)
                    # Draw saved points in green
                    cv.circle(src_copy, (int(pts.srcX), int(pts.srcY)), 5, (0, 255, 0), -1)
                    cv.circle(dst_copy, (int(pts.dstX), int(pts.dstY)), 5, (0, 255, 0), -1)
                else:
                    print(f"Invalid PTS point for camera {camera_id}: src={src_point}, dst={dst_point}")
        print(f"Loaded {len(src_list)} PTS points for camera {camera_id}")
        print("src points:", src_list)
        print("dst points:", dst_list)
    except Exception as e:
        print(f"Error loading PTS points: {str(e)}")
        raise

    # Mouse callback functions
    def select_points_src(event, x, y, flags, param):
        nonlocal src_x, src_y, drawing
        print(f"Mouse event on src: event={event}, x={x}, y={y}")
        if event == cv.EVENT_LBUTTONDOWN:
            drawing = True
            src_x, src_y = x, y
            cv.circle(src_copy, (x, y), 5, (0, 0, 255), -1)
        elif event == cv.EVENT_LBUTTONUP:
            drawing = False

    def select_points_dst(event, x, y, flags, param):
        nonlocal dst_x, dst_y, drawing
        print(f"Mouse event on dst: event={event}, x={x}, y={y}")
        if event == cv.EVENT_LBUTTONDOWN:
            drawing = True
            dst_x, dst_y = x, y
            cv.circle(dst_copy, (x, y), 5, (0, 0, 255), -1)
        elif event == cv.EVENT_LBUTTONUP:
            drawing = False

    def get_plan_view(src, dst):
        print("Entering get_plan_view")
        if len(src_list) < 4 or len(dst_list) < 4:
            print("Error: At least 4 point pairs are required for homography")
            return None
        if len(src_list) != len(dst_list):
            print(f"Error: Mismatched point counts (src: {len(src_list)}, dst: {len(dst_list)})")
            return None
        try:
            # Validate each point
            for i, (src_pt, dst_pt) in enumerate(zip(src_list, dst_list)):
                if len(src_pt) != 2 or len(dst_pt) != 2:
                    print(f"Error: Invalid point pair at index {i}: src={src_pt}, dst={dst_pt}")
                    return None
            src_pts = np.array(src_list, dtype=np.float32).reshape(-1, 1, 2)
            dst_pts = np.array(dst_list, dtype=np.float32).reshape(-1, 1, 2)
            print("src_pts:", src_pts)
            print("dst_pts:", dst_pts)
            H, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)
            if H is None:
                print("Error: Homography calculation failed")
                return None
            print("H:")
            print(H)
            plan_view = cv.warpPerspective(src, H, (dst.shape[1], dst.shape[0]))
            print("Plan view generated successfully")
            return plan_view
        except Exception as e:
            print(f"Error in get_plan_view: {str(e)}")
            return None

    def merge_views(src, dst):
        print("Entering merge_views")
        plan_view = get_plan_view(src, dst)
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
                cv.circle(src_copy, (src_x, src_y), 5, (0, 255, 0), -1)
                cv.circle(dst_copy, (dst_x, dst_y), 5, (0, 255, 0), -1)
                src_point = [float(src_x), float(src_y)]
                dst_point = [float(dst_x), float(dst_y)]
                src_list.append(src_point)
                dst_list.append(dst_point)
                print("src points:", src_list)
                print("dst points:", dst_list)

                # Save to PTS table
                try:
                    pts = PTS(
                        srcX=float(src_x),
                        srcY=float(src_y),
                        dstX=float(dst_x),
                        dstY=float(dst_y),
                        Camera_=camera_id
                    )
                    print("Saving PTS to database")
                    pts_repo.add_pts(pts)
                    print(f"Saved PTS for camera {camera_id}: ({src_x}, {src_y}) -> ({dst_x}, {dst_y})")
                except Exception as e:
                    print(f"Error saving PTS: {str(e)}")
                src_x, src_y, dst_x, dst_y = -1, -1, -1, -1  # Reset points after saving
                print("Points saved and reset")

            elif k == ord('h'):
                print('Creating plan view')
                plan_view = get_plan_view(src, dst)
                if plan_view is not None:
                    cv.imshow("plan view", plan_view)
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