# Hệ thống quản lý bãi đỗ xe thông minh

---

## I. Giới thiệu

Hệ thống quản lý bãi đỗ xe thông minh là một ứng dụng hỗ trợ nhận diện phương tiện, theo dõi vị trí, và đề xuất các vị trí đỗ xe còn trống trong bãi đỗ xe. Dự án sử dụng các công nghệ học sâu và xử lý hình ảnh để tự động hóa quy trình quản lý bãi đỗ xe, giúp tiết kiệm thời gian và tăng hiệu quả sử dụng không gian.

**Các tính năng chính**:

- Nhận diện phương tiện trong video hoặc luồng camera trực tiếp bằng mô hình YOLOv11.
- Theo dõi chuyển động của phương tiện sử dụng thuật toán BoT-SORT.
- Ánh xạ không gian bãi đỗ xe bằng kỹ thuật Homography để xác định vị trí trống.
- Giao diện người dùng thân thiện được phát triển bằng Qt6.
- Lưu trữ thông tin phương tiện (biển số, thời gian đỗ) trong cơ sở dữ liệu MS SQL Server.

Dự án phù hợp cho các bãi đỗ xe tại trung tâm thương mại, tòa nhà văn phòng, hoặc khu dân cư.

---

## II. Công nghệ sử dụng

Dự án sử dụng các công nghệ và thư viện sau:

- **Python 3.11**: Ngôn ngữ lập trình chính.
- **YOLOv11**: Mô hình học sâu để nhận diện phương tiện.
- **BoT-SORT**: Thuật toán theo dõi đa đối tượng.
- **Qt6**: Thư viện phát triển giao diện người dùng.
- **OpenCV**: Xử lý hình ảnh và video.
- **Homography**: Kỹ thuật ánh xạ không gian để xác định vị trí đỗ xe.
- **MS SQL Server**: Cơ sở dữ liệu để lưu trữ thông tin phương tiện.
- **CUDA Toolkit 11.x**: Hỗ trợ tăng tốc xử lý trên GPU NVIDIA.

---

## III. Hướng dẫn cài đặt và sử dụng

### 1. Cài đặt môi trường

1. **Cài đặt Python**:
   - Tải Python 3.11 từ python.org.
   - Đảm bảo thêm Python vào biến PATH trong quá trình cài đặt.
2. **Cài đặt Git**:
   - Tải và cài đặt Git từ git-scm.com.
3. **Cài đặt MS SQL Server**:
   - Tải SQL Server Express từ microsoft.com.
   - Cấu hình server và tạo cơ sở dữ liệu theo file `carPark.sql`.
4. **Cài đặt CUDA Toolkit**:
   - Tải CUDA Toolkit 11.x từ developer.nvidia.com.
   - Đảm bảo GPU NVIDIA có hỗ trợ CUDA được cài đặt driver mới nhất.
5. **Cài đặt trình soạn thảo**:
   - Sử dụng Visual Studio Code, PyCharm, hoặc Notepad++ để chỉnh sửa mã nguồn.

### 2. Tải và chạy mã nguồn

#### 2.1. Clone repository

1. Mở Git Bash (Windows).

2. Clone repository từ GitHub:

   ```sh
   git clone https://github.com/trieuvn/CarParkTrack.git
   ```

#### 2.2. Cài đặt thư viện

Cài đặt các thư viện Python cần thiết:

```sh
pip install -r requirements.txt
```

#### 2.3. Cấu hình môi trường

1. **Cơ sở dữ liệu**:
   - Mở MS SQL Server Management Studio (Windows) hoặc công cụ tương tự (Linux).
   - Chạy tệp `carPark.sql` để tạo bảng và cấu trúc cơ sở dữ liệu.
   - Chạy lệnh "mssql+pyodbc://@(TÊN MÁY xem ở PC -&gt; properties VD: DESKTOP-M0KCUVC)/CarPark?driver=ODBC+Driver+17+for+SQL+Server&Trusted_Connection=yes" --outfile BusinessObject/models.py" để thực hiện scaffold lên model.
   - Cấu hình lại file database.py để hệ thống dẫn tới cơ sở dữ liệu.
2. **Camera/Video**:
   - Kết nối camera hoặc chuẩn bị file video (định dạng `.mp4`) để thử nghiệm.
   - Cập nhật đường dẫn video/camera trong `main.py` (ví dụ: `0` cho webcam, hoặc `"path/to/video.mp4"`).

#### 2.4. Chạy ứng dụng

1. Mở terminal trong thư mục dự án.

2. Chạy ứng dụng:

   ```sh
   python main.py
   ```

3. **Kết quả mong đợi**:

   - Giao diện Qt6 hiển thị luồng video từ camera hoặc file video.
   - Các phương tiện được nhận diện và theo dõi, với khung bao (bounding box) và ID.
   - Vị trí đỗ xe trống được đánh dấu trên giao diện.
   - Thông tin phương tiện (biển số, thời gian đỗ) được lưu vào cơ sở dữ liệu.

---

## V. Yêu cầu hệ thống

| Thành phần | Yêu cầu tối thiểu | Yêu cầu khuyến nghị |
| --- | --- | --- |
| **Hệ điều hành** | Windows 10, Ubuntu 20.04 | Windows 11, Ubuntu 22.04 |
| **CPU** | Intel Core i3-9100F | Intel Core i7-12700 |
| **GPU** | NVIDIA GTX 1650 (CUDA hỗ trợ) | NVIDIA RTX 4060 |
| **RAM** | 8GB | 16GB |
| **Dung lượng ổ cứng** | 10GB trống | 20GB trống |
| **Phần mềm** | Python 3.8+, MS SQL Server, CUDA Toolkit 11.x | Python 3.10, MS SQL Server 2022, CUDA Toolkit 11.8 |
| **Camera/Video** | Webcam hoặc video 720p | Camera IP hoặc video 1080p |

---

## VII. Liên hệ và đóng góp

Nếu bạn có thắc mắc, đề xuất cải tiến, hoặc muốn đóng góp vào dự án, vui lòng:

- **Liên hệ**:
  - Email: trieunn22@uef.edu.vn.
  - GitHub: trieuvn.

---

**Cảm ơn bạn đã quan tâm đến dự án!**
