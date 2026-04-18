# Drug Disease AI WebApp

Kiến trúc triển khai:
- `public/`: entrypoint web PHP trên XAMPP
- `app/`: config, helpers, services
- `api/`: REST-like endpoints PHP
- `python_api/`: FastAPI service gọi hoặc giả lập model AI
- `database_schema.sql`: schema MySQL để import trước

Luồng hoạt động:
1. Người dùng đăng nhập trên PHP web.
2. Người dùng nhập thuốc hoặc bệnh.
3. PHP gọi Python API tại `http://127.0.0.1:8000`.
4. Python API trả về top-k kết quả + score + graph nodes/links.
5. PHP lưu lịch sử dự đoán vào MySQL.
6. Frontend hiển thị bảng kết quả, lịch sử, dashboard admin, biểu đồ mạng 3D.
