import streamlit as st

def show_map_page():
    st.markdown("## 🗺️ **Peta Interaktif Kebun Binatang Ragunan**")
    st.markdown("""
    Jelajahi lokasi Kebun Binatang Ragunan secara langsung melalui peta interaktif di bawah ini.  
    Peta ini dapat membantu Anda mengetahui letak area-area penting serta memperkaya pengalaman edukatif dan wisata Anda.
    """)
    
    st.markdown(
        '<iframe src="https://www.google.com/maps/d/embed?mid=1WxhE_KdpD1pO36C0ow-q9HCQHuDMuGJL&ehbc=2E312F" width="100%" height="600"></iframe>',
        unsafe_allow_html=True
    )