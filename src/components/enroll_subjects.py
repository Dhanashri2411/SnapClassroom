import streamlit as st
import supabase
from src.database.config import supabase
from src.database.db import enroll_student_to_subject, unenroll_student_to_subject
@st.dialog("Enroll Subjects")
def enroll_dialog():
    st.write("Enter the Subject code Given by your Teacher to Enroll in the Subject")
    join_code=st.text_input("Subject Code",placeholder="E.g. CS101",key="enroll_subject_code")

    if st.button("Enroll Now",type="primary",width="stretch"):
        if join_code:
            res=supabase.table("subjects").select("subject_id,name,subject_code").eq("subject_code",join_code).execute()
            if res.data:
                subject=res.data[0]
                student_id=st.session_state.student_data["student_id"]
                check=supabase.table("subject_students").select("*").eq("subject_id",subject["subject_id"]).eq("student_id",student_id).execute()
                if check.data:
                    st.warning("You are already enrolled in this subject")
                else:
                    enroll_student_to_subject(student_id,subject["subject_id"])
                    st.success(f"You have been enrolled in {subject['name']} successfully!")
                    import time
                    time.sleep(1)
                    st.rerun()
                    
            else:
                st.warning("Invalid Subject Code")
                return
            st.session_state.enroll_subject_code=join_code
            st.toast("Enrolled Succesfully!")
            st.rerun()
        else:
            st.warning("Please Enter the Subject Code")