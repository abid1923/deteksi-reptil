import streamlit as st

def show_home_page():
    st.write("""
    ## Selamat datang di Sistem Deteksi Reptil Kebun Binatang Ragunan! 🦎

    Sistem ini menggunakan teknologi AI untuk mendeteksi berbagai jenis reptil yang ada di Kebun Binatang Ragunan.
    Anda dapat mengupload gambar reptil dan sistem akan mendeteksi jenis reptil tersebut.

    ### Fitur-fitur:
    1. 📸 **Deteksi Gambar**: Upload gambar reptil untuk diidentifikasi  
    2. 📝 **Riwayat Deteksi**: Lihat history deteksi yang pernah dilakukan  
    3. 🗺️ **Peta Ragunan**: Lihat peta lokasi reptil di Ragunan
    """)

    st.markdown("""
    <h4>🦕 Daftar Reptil yang Bisa Dideteksi:</h4>
    <ul style="font-size: 18px;">
        <li>🦎 Biawak Salvator</li>
        <li>🐊 Buaya</li>
        <li>🐢 Bulus Moncong Babi</li>
        <li>🦎 Iguana</li>
        <li>🦖 Komodo</li>
        <li>🐢 Kura-kura Sulcata</li>
        <li>🐍 Ular Koros</li>
        <li>🐍 Ular Sanca</li>
        <li>🐍 Ular Sendok Raja</li>
    </ul>
    """, unsafe_allow_html=True)