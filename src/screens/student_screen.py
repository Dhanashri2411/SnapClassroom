import streamlit as st
from src.ui.base_layout import base_layout_dashboard,base_layout_overall

def student_screen():
    base_layout_dashboard()
    base_layout_overall()
    st.header("Student Screen")
    