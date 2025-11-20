
# 👟 Huy Sneakers - Cloud Computing Project (AWS)

Dự án bài tập lớn môn Điện toán đám mây: Hệ thống E-commerce bán giày chịu tải cao (High Availability).

## 🚀 Giới thiệu
Dự án được xây dựng trên nền tảng **Django (Python)**, mô phỏng một website bán giày với các tính năng:
* Xem danh sách sản phẩm, chi tiết giày.
* Thêm vào giỏ hàng, đặt hàng (Checkout).
* Hệ thống quản trị (Admin) để đăng sản phẩm.
* **Mục tiêu:** Triển khai trên AWS với kiến trúc Auto Scaling & Load Balancer.

 

### 🛠️ Hướng dẫn cài đặt (Cho thành viên nhóm)

Mọi người pull code về và làm theo đúng thứ tự các bước sau để chạy local nhé.

### Bước 1: Tải code về máy
git clone [https://github.com/NguyenThanhHuy-dev/Cloud_sneaker.git](https://github.com/NguyenThanhHuy-dev/Cloud_sneaker.git)
cd Cloud_sneaker


### Bước 2: Tạo môi trường ảo (Bắt buộc)

Để không bị lỗi thư viện, hãy tạo môi trường riêng:

Bash


# Tạo venv
python -m venv venv

# Kích hoạt (Windows)
.\venv\Scripts\activate

# Kích hoạt (Mac/Linux)
source venv/bin/activate


_(Sau khi kích hoạt, đầu dòng terminal phải hiện chữ `(venv)`)_

### Bước 3: Cài đặt thư viện

Bash


pip install -r requirements.txt



### Bước 4: Cấu hình file môi trường (.env)

**Quan trọng:** Tạo một file tên là `.env` (có dấu chấm ở đầu) nằm cùng cấp với file `manage.py`. Copy toàn bộ nội dung dưới đây dán vào file `.env` đó:

Ini, TOML


# Cấu hình cơ bản
DEBUG=True
SECRET_KEY=django-insecure-team-cloud-project-2025-huy-sneaker

# Cấu hình Database (Mặc định chạy SQLite ở local cho nhanh)
DATABASE_URL=sqlite:///db.sqlite3

# Cấu hình Email giả (Để không bị lỗi khi đăng ký)
EMAIL_HOST_USER=dummy_email@gmail.com
EMAIL_HOST_PASSWORD=dummy_pass

# Key giả cho tính năng Login Facebook/Google (Không cần sửa)
SOCIAL_AUTH_FACEBOOK_KEY=dummy_key
SOCIAL_AUTH_FACEBOOK_SECRET=dummy_secret
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=dummy_key
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=dummy_secret

# Key giả cho cổng thanh toán Razorpay
RAZORPAY_KEY_ID=dummy_razorpay_id
RAZORPAY_SECRET_KEY=dummy_razorpay_secret_fix



### Bước 5: Khởi tạo Database & Chạy Web

Bash


# Tạo bảng dữ liệu (Chỉ cần chạy lần đầu)
python manage.py migrate

# Tạo tài khoản admin (Để vào trang quản trị)
python manage.py createsuperuser

# Bật Web
python manage.py runserver



Truy cập: `http://127.0.0.1:8000/` Trang Admin: `http://127.0.0.1:8000/admin/`

----------

## ⚠️ Lưu ý quan trọng khi làm việc nhóm

1.  **KHÔNG ĐƯỢC** đẩy file `.env` lên git (mỗi người tự tạo file này ở máy mình).
    
2.  **KHÔNG ĐƯỢC** đẩy file `db.sqlite3` lên git (tránh xung đột dữ liệu).
    
3.  Khi code xong tính năng mới:
    
    -   `git checkout -b ten-nhanh-moi` (Tạo nhánh riêng).
        
    -   Code xong thì `git push` và tạo Pull Request để Leader review.