import streamlit as st
from src.components.header import header_home
from src.ui.base_layout import base_layout_home,base_layout_overall


def home_screen():
    
    header_home()
    base_layout_home()
    base_layout_overall()
    col1, col2 = st.columns(2)

    with col1:
         if st.button("Student Portal", key="student_portal"):
            st.session_state['login_type'] = 'student'
            st.rerun()
    with col2:
        if st.button("Teacher Portal", key="teacher_portal"):
            st.session_state['login_type'] = 'teacher'
            st.rerun()
    