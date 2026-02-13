# Weather Trend Analysis

Phân tích xu hướng thời tiết sử dụng Python, với các tính năng phân tích thống kê, bootstrap resampling, trực quan hóa và kiểm thử tự động.

## Mục lục
- [Giới thiệu](#giới-thiệu)
- [Cài đặt](#cài-đặt)
- [Cấu trúc thư mục](#cấu-trúc-thư-mục)
- [Cách sử dụng](#cách-sử-dụng)
- [Cấu hình](#cấu-hình)
- [Kiểm thử](#kiểm-thử)
- [Yêu cầu](#yêu-cầu)

## Giới thiệu
Dự án này thực hiện phân tích xu hướng thời tiết (nhiệt độ, lượng mưa, v.v.) dựa trên dữ liệu lịch sử. Hỗ trợ phân tích tuyến tính, bootstrap để ước lượng độ bất định, so sánh các phương pháp thống kê và trực quan hóa kết quả.

## Cài đặt
1. Clone repo về máy:
	 ```bash
	 git clone <repo-url>
	 cd Weather
	 ```
2. Cài đặt các thư viện cần thiết:
	 ```bash
	 pip install -r requirements.txt
	 ```

## Cấu trúc thư mục
```
Weather/
├── main.py                  # Chạy phân tích xu hướng cơ bản
├── main_with_bootstrap.py   # Chạy phân tích có bootstrap
├── requirements.txt         # Thư viện cần thiết
├── config/
│   └── config.yaml          # File cấu hình
├── data/
│   └── weather_data.csv     # Dữ liệu thời tiết mẫu
├── outputs/
│   ├── plots/               # Lưu biểu đồ
│   └── reports/             # Lưu báo cáo
├── src/
│   ├── analysis/            # Phân tích số liệu, bootstrap
│   ├── data/                # Load và xử lý dữ liệu
│   ├── utils/               # Tiện ích cấu hình, logging
│   └── visualization/       # Vẽ biểu đồ
└── test/                    # Unit test
```

## Cách sử dụng
### 1. Phân tích cơ bản
```bash
python main.py
```
### 2. Phân tích với bootstrap
```bash
python main_with_bootstrap.py
```
Kết quả sẽ được lưu trong thư mục `outputs/plots/`.

## Cấu hình
Chỉnh sửa file `config/config.yaml` để thay đổi:
- Đường dẫn dữ liệu đầu vào
- Tham số bootstrap (số lần lặp, seed, ...)
- Mức ý nghĩa thống kê, mức tin cậy
- Năm dự đoán, các tháng mùa hè/đông

Ví dụ:
```yaml
data:
	input_file: "data/weather_data.csv"
	date_column: "date"
analysis:
	summer_months: [6, 7, 8]
	winter_months: [12, 1, 2]
	confidence_level: 0.95
	significance_level: 0.05
	prediction_year: 2030
	bootstrap:
		enabled: true
		n_iterations: 10000
		random_seed: 42
		compare_methods: true
output:
	plots_dir: "outputs/plots"
```

## Kiểm thử
Chạy toàn bộ unit test với pytest:
```bash
pytest --maxfail=1 --disable-warnings -q
```

## Yêu cầu
- Python >= 3.8
- Các thư viện: pandas, numpy, matplotlib, scipy, pyyaml, pytest, pytest-cov

## Đóng góp
Mọi đóng góp, báo lỗi hoặc ý tưởng cải tiến đều được hoan nghênh!
