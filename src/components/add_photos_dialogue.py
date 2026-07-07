import streamlit as st
from PIL import Image
@st.dialog("Capture or Upload Photos")
def add_photos_dialogue():

    st.write("Add Classroom Photos to scan for Attendance")
    if "photo_tab" not in st.session_state:
        st.session_state.photo_tab = "camera"
    t1,t2=st.columns(2) 
    with t1:
        type_camera="primary" if st.session_state.photo_tab=="camera" else "tertiary"
        if st.button("Capture from Camera",type=type_camera,icon=":material/camera_alt:",icon_position="left",width="stretch"):
            st.session_state.photo_tab="camera"
            st.rerun()
    with t2:
        type_upload="primary" if st.session_state.photo_tab=="upload" else "tertiary"
        if st.button("Upload from Device",type=type_upload,icon=":material/file_upload:",icon_position="left",width="stretch"):
            st.session_state.photo_tab="upload"
            st.rerun()
    if st.session_state.photo_tab=="camera":
        camera_photo=st.camera_input("Capture Photo",key="camera_photo")
        if camera_photo:
            st.session_state.attendence_image.append(Image.open(camera_photo))
            st.toast("Photo Captured Successfully!")
            st.rerun()
    if st.session_state.photo_tab=="upload":
        upload_photos=st.file_uploader("Upload Photo",type=["jpg","jpeg","png"],key="upload_photo",accept_multiple_files=True,label_visibility="collapsed")
        if upload_photos:
            for photo in upload_photos:
                st.session_state.attendence_image.append(Image.open(photo))
            st.toast("Photos Uploaded Successfully!")
            st.rerun()
    st.divider()
    if st.button("Done",type="tertiary",width="stretch"):
        st.rerun()