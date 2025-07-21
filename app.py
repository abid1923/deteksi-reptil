import streamlit as st
st.set_page_config(initial_sidebar_state="collapsed")
from features.auth import show_login_page
from features.home import show_home_page
from features.detection import show_detection_page
from features.history import show_history_page
from features.map import show_map_page

def init_session_state():
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
    if 'username' not in st.session_state:
        st.session_state.username = None
    if 'detected_classes' not in st.session_state:
        st.session_state.detected_classes = []
    if 'quiz_state' not in st.session_state:
        st.session_state.quiz_state = {}
    if 'current_detection' not in st.session_state:
        st.session_state.current_detection = None
    if 'result_image' not in st.session_state:
        st.session_state.result_image = None
    if 'detection_saved' not in st.session_state:
        st.session_state.detection_saved = False

def logout():
    st.session_state.logged_in = False
    st.session_state.username = None
    st.session_state.detected_classes = []
    st.session_state.quiz_state = {}
    st.session_state.current_detection = None
    st.session_state.detection_saved = False

def main():
    st.set_page_config(page_title="Deteksi Reptil", page_icon="🐊", layout="wide")
    init_session_state()

    if not st.session_state.logged_in:
        show_login_page()
    else:
        # HAPUS st.title() dari sini jika ingin tampilan lebih minimalis
        st.title("🐊 Deteksi Reptil Kebun Binatang Ragunan")
        
        col1, col2 = st.columns([4, 1])
        with col1:
            # MODIFIKASI SELECTBOX INI:
            menu = st.selectbox(
                "Navigasi",  # Teks yang muncul di atas dropdown
                ["Beranda", "Deteksi Gambar", "Riwayat Deteksi", "Peta Ragunan"],
                key="menu",
                label_visibility="collapsed"  # Sembunyikan label
            )
            
            # TAMBAHKAN INI UNTUK MEMBUAT PEMISAH VISUAL
            st.markdown("---") 

        with col2:
            st.write(f"👤 Login sebagai: {st.session_state.username}")
            if st.button("Logout"):
                logout()
                st.rerun()
        
        # TAMBAHKAN SPASI ANTAR KOMPONEN
        st.write("")  
        
        if menu == "Beranda":
            show_home_page()
        elif menu == "Deteksi Gambar":
            show_detection_page()
        elif menu == "Riwayat Deteksi":
            show_history_page()
        elif menu == "Peta Ragunan":
            show_map_page()

if __name__ == "__main__":
    main()