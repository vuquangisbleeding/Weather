# Weather Trend Analysis - Báo cáo đặc điểm và ưu việt

## 1. Điểm đặc biệt của dự án
- **Phân tích xu hướng thời tiết chuyên sâu**: Hỗ trợ phân tích nhiệt độ, lượng mưa, độ ẩm theo mùa, năm, hoặc toàn bộ chuỗi thời gian.
- **Bootstrap resampling**: Áp dụng bootstrap để ước lượng độ bất định, tạo khoảng tin cậy mà không cần giả định phân phối chuẩn.
- **So sánh phương pháp thống kê**: Cho phép so sánh kết quả giữa phương pháp tham số (parametric) và phi tham số (bootstrap).
- **Cấu hình linh hoạt**: Toàn bộ tham số (đường dẫn dữ liệu, số lần bootstrap, mức ý nghĩa, năm dự đoán, ...) đều chỉnh qua file YAML.
- **Trực quan hóa mạnh mẽ**: Sinh biểu đồ xu hướng, khoảng tin cậy, so sánh bootstrap và parametric, lưu tự động vào thư mục outputs.
- **Kiểm thử tự động**: Có sẵn unit test cho các module chính, đảm bảo độ tin cậy và dễ mở rộng.

## 2. Tính năng nổi bật
- **Phân tích tuyến tính (Linear Regression)**: Tìm xu hướng nhiệt độ, lượng mưa theo thời gian, kiểm tra ý nghĩa thống kê.
- **Bootstrap cho ước lượng độ bất định**: Lặp lại phân tích hàng ngàn lần để lấy phân phối tham số, tạo khoảng tin cậy thực nghiệm.
- **Dự đoán tương lai**: Dự báo giá trị (nhiệt độ, mưa, ...) cho năm chỉ định trong cấu hình.
- **Tùy chọn phân tích theo mùa**: Phân tích riêng cho mùa hè, mùa đông hoặc toàn bộ năm.
- **Lưu trữ và xuất báo cáo, biểu đồ**: Tự động lưu kết quả vào thư mục outputs/plots và outputs/reports.

## 3. Công dụng thực tiễn
- **Nghiên cứu biến đổi khí hậu**: Phân tích xu hướng nhiệt độ, lượng mưa để đánh giá tác động biến đổi khí hậu tại địa phương.
- **Hỗ trợ ra quyết định**: Cung cấp số liệu, biểu đồ, dự báo giúp nhà quản lý, nông nghiệp, thủy lợi, ... lập kế hoạch thích ứng.
- **Giảng dạy & học tập**: Là ví dụ thực tiễn về phân tích dữ liệu, thống kê, bootstrap, trực quan hóa trong Python.

## 4. Ưu việt so với các giải pháp khác
- **Không phụ thuộc vào giả định phân phối**: Bootstrap cho phép ước lượng độ bất định mà không cần dữ liệu tuân theo phân phối chuẩn.
- **Cấu trúc module rõ ràng, dễ mở rộng**: Tách biệt các phần (load dữ liệu, phân tích, trực quan hóa, kiểm thử), dễ bảo trì và phát triển thêm.
- **Tùy biến cao**: Dễ dàng thay đổi dữ liệu, tham số, phương pháp phân tích qua file cấu hình mà không cần sửa code.
- **Tích hợp kiểm thử tự động**: Đảm bảo chất lượng, phát hiện lỗi sớm khi mở rộng hoặc chỉnh sửa.
- **Thích hợp cho cả nghiên cứu, ứng dụng thực tế và đào tạo**.

---

*Báo cáo tự động sinh ngày 13/02/2026.*
