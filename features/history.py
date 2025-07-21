import streamlit as st
from services.history_service import get_detection_history

def show_history_page():
    st.write("## 📝 Riwayat Deteksi")
    history = get_detection_history(st.session_state.username)
    
    if history:
        for record in history:
            with st.expander(f"Deteksi pada {record['waktu']}"):
                st.write(f"Reptil: {record['nama_reptil']}")
                st.write(f"Confidence: {record['confidence']:.2f}")
    else:
        st.info("Belum ada riwayat deteksi")