import streamlit as st
import segno
import io
@st.dialog("Share Class Link")
def share_subject_dialogue(subject_name, subject_code):
    app_domain="snaplass-main.streamlit.app"
    join_url=f"{app_domain}/?join-code={subject_code}"
    st.header("Scan to Join")
    qrcode = segno.make(join_url)
    img_buffer = io.BytesIO()
    qrcode.save(img_buffer, kind="png", scale=10,border=1)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### Copy the Link")
        st.code(join_url, language="text")
        st.code(subject_code, language="text")
        st.info("Copy this link to share QR on WhatsApp and Email")
    with col2:
        st.markdown("### Scan the QR Code")
        st.image(img_buffer.getvalue(),use_container_width=True,caption="Scan this QR code to join the class")

