import streamlit as st
from services.history_service import get_detection_history

def show_history_page():
    st.write("## 📝 Riwayat Deteksi")
    history = get_detection_history(st.session_state.username)

    if history:
        for record in history:
            with st.expander(f"Deteksi pada {record['waktu']}"):
                reptil = record['nama_reptil']
                confidence = record['confidence']

                if reptil.lower() == "tidak terdeteksi":
                    st.warning("⚠️ Tidak ada reptil terdeteksi dalam gambar ini.")
                else:
                    st.write(f"Reptil: {reptil}")
                    st.write(f"Confidence: {confidence:.2f}")
    else:
        st.info("Belum ada riwayat deteksi")