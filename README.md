# Drug Disease AI Predictor

Ứng dụng web PHP chạy trên XAMPP, dùng MySQL để lưu dữ liệu và Python FastAPI để phục vụ AI prediction.

## 1. Tạo database
- Mở phpMyAdmin
- Import file `database_schema.sql`

## 2. Chạy Python API
Mở terminal trong thư mục dự án:

```bash
cd python_api
python -m pip install -r requirements.txt
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

## 3. Chạy web bằng XAMPP
- Đặt project trong `htdocs/DoAnBaseFix`
- Start Apache + MySQL trong XAMPP
- Truy cập: `http://localhost/DoAnBaseFix/public/login.php`

## 4. Tài khoản mặc định
- admin / password
- user1 / password

## 5. Các chức năng hiện có
- Đăng nhập
- Tra cứu thuốc -> bệnh
- Tra cứu bệnh -> thuốc
- Gọi Python API qua HTTP
- Lưu lịch sử tra cứu
- Dashboard admin thống kê
- Biểu đồ node 3D với màu khác nhau cho thuốc, bệnh, protein

## 6. Ghi chú
- Python API hiện đang là lớp tích hợp dữ liệu và trả kết quả demo thông minh từ dữ liệu có sẵn.
- Có thể nâng cấp tiếp để nối trực tiếp suy luận model thật trong `ductri_hgt_update`.
