import base64
import re
from pathlib import Path

import streamlit as st

EMAIL_PATTERN = re.compile(r"^[A-Za-z0-9._%+-]+@gmail\.com$", re.IGNORECASE)
PASSWORD_PATTERN = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$")


def is_valid_email(email: str) -> bool:
    return bool(EMAIL_PATTERN.fullmatch(email.strip()))


def is_valid_password(password: str) -> bool:
    return bool(PASSWORD_PATTERN.fullmatch(password))


def _render_label_with_icon(icon_path: str, label: str, margin_top: str) -> None:
    icon_file = Path(__file__).resolve().parent / icon_path
    icon_data = base64.b64encode(icon_file.read_bytes()).decode("ascii")
    st.markdown(
        f"""
        <div style="display:flex;align-items:center;gap:0.5rem;margin:{margin_top} 0 0.4rem;">
            <img
                src="data:image/png;base64,{icon_data}"
                alt="{label}"
                style="width:18px;height:18px;display:block;object-fit:contain;transform:translateY(-2px);"
            />
            <strong>{label}</strong>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_email_label() -> None:
    _render_label_with_icon("icons/e-mail.webp", "Địa chỉ Email", "0.7rem")


def render_password_label() -> None:
    _render_label_with_icon("icons/padlock.png", "Mật khẩu", "0.15rem")


def main() -> None:
    st.set_page_config(page_title="Streamlit", page_icon="📋", layout="centered")

    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(180deg, #10131a 0%, #0c0f15 100%);
        }

        .card {
            max-width: 720px;
            margin: 0 auto;
            padding: 1.15rem 1.2rem 1.25rem;
            background: rgba(15, 18, 26, 0.96);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 18px;
            box-shadow: 0 18px 50px rgba(0, 0, 0, 0.28);
        }

        .field-label {
            color: rgba(255, 255, 255, 0.92);
            font-size: 1rem;
            font-weight: 700;
            margin-bottom: 0.35rem;
        }

        .stButton button {
            background: linear-gradient(135deg, #1a2030 0%, #111827 100%);
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 14px;
            padding: 0.7rem 1.1rem;
            font-weight: 700;
            transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease;
        }

        .stButton button:hover {
            transform: translateY(-1px);
            border-color: rgba(255, 255, 255, 0.22);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.22);
        }

        .result-box {
            margin-top: 1rem;
            padding: 0.9rem 1rem;
            border-radius: 12px;
            font-weight: 600;
        }

        .success-box {
            background: rgba(34, 197, 94, 0.12);
            border: 1px solid rgba(34, 197, 94, 0.25);
            color: #7ee2a8;
        }

        .error-box {
            background: rgba(239, 68, 68, 0.12);
            border: 1px solid rgba(239, 68, 68, 0.25);
            color: #ffb4b4;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="card">', unsafe_allow_html=True)
    with st.form("registration_form", clear_on_submit=False):
        render_email_label()
        email = st.text_input(
            label="Email",
            placeholder="Nhập email theo mẫu hợp lệ...",
            label_visibility="collapsed",
        )

        render_password_label()
        password = st.text_input(
            label="Mật khẩu",
            type="password",
            placeholder="Nhập mật khẩu theo quy tắc trên",
            label_visibility="collapsed",
        )

        submitted = st.form_submit_button("Tạo Tài Khoản")

    st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        if not is_valid_email(email):
            st.markdown(
                '<div class="result-box error-box">Email của bạn không hợp lệ. Vui lòng kiểm tra định dạng (ví dụ: ten.ban@gmail.com).</div>',
                unsafe_allow_html=True,
            )
        elif not is_valid_password(password):
            st.markdown(
                '<div class="result-box error-box">Mật khẩu không đáp ứng các yêu cầu về độ mạnh (8 ký tự, hoa, thường, số, đặc biệt).</div>',
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="result-box success-box">Tạo tài khoản thành công!</div>',
                unsafe_allow_html=True,
            )
            st.balloons()


if __name__ == "__main__":
    main()
