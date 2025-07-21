import streamlit as st
from services.auth_service import register_user, verify_login

def show_login_page():
    st.title("🐊 Login Sistem Deteksi Reptil")
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            if verify_login(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Username atau password salah")

    with tab2:
        new_username = st.text_input("Username", key="register_username")
        new_password = st.text_input("Password", type="password", key="register_password")
        if st.button("Register"):
            if register_user(new_username, new_password):
                st.success("Registrasi berhasil! Silakan login.")
            else:
                st.error("Username sudah digunakan")