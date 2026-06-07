# Mini Project Streamlit

Ứng dụng Streamlit đơn giản cho trang đăng ký tài khoản, có kiểm tra:

- Email phải đúng định dạng Gmail.
- Mật khẩu phải có ít nhất 8 ký tự, gồm chữ hoa, chữ thường, số và ký tự đặc biệt.

## Yêu cầu

- Python 3.12 trở lên
- `uv`

## Tạo môi trường và cài đặt

Trong thư mục dự án, chạy:

```bash
uv sync
```

Lệnh này sẽ tạo môi trường ảo `.venv` và cài các thư viện cần thiết từ `pyproject.toml`.

## Chạy ứng dụng

Khởi động app Streamlit bằng lệnh:

```bash
uv run streamlit run main.py
```

Sau khi chạy, Streamlit sẽ mở ứng dụng trong trình duyệt mặc định.

## Cấu trúc chính

- `main.py`: mã nguồn ứng dụng Streamlit
- `pyproject.toml`: cấu hình dự án và dependency
- `icons/`: chứa icon giao diện

## Ghi chú

Nếu bạn thay đổi dependency, hãy chạy lại:

```bash
uv sync
```
