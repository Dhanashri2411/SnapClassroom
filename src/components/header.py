import streamlit as st
def header_home():
    logo_url="https://i.ibb.co/YTYGn5qV/logo.png"
    st.markdown(
        f"""   
        <div style="display: flex; align-items: center; justify-content: center;">
                <img src="{logo_url}" alt="Logo" style="width: 100px; height: 100px; margin-right: 10px;">
                <h1 style="font-family: 'Climate Crisis', sans-serif; font-size: 3.5rem; color: #333;">Snap<br/>Class</h1>
            </div>
        """, unsafe_allow_html=True)
def header_dashboard():

    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    
    st.markdown(f"""
        <div style="display:flex; align-items:center; justify-content:center; gap:10px">
            <img src='{logo_url}' style='height:85px;' />
            <h2 style='text-align:left; color:#5865F2'>SNAP<br/>CLASS</h1>
        </div>   
                
                """, unsafe_allow_html=True)