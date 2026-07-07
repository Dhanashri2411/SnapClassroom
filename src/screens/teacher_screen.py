from requests import get
import streamlit as st
from src.components.subject_card import subject_card
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.footer import footer_dashboard
from src.components.header import header_dashboard
from src.database.db import check_teacher_exists,create_teacher_login,teacher_login,get_teacher_subjects
from src.components.dialogue_create_subject import create_subject_dialogue
from src.components.dialogue_share_subject import share_subject_dialogue
from src.components.add_photos_dialogue import add_photos_dialogue
from src.pipelines.face_pipeline import predict_attendance
from src.database.config import supabase
from datetime import datetime
import numpy as np
import pandas as pd
from src.components.dialogue_voice_attendence import voice_attendance_dialogue
from src.components.attendence_results_dialogue import attendence_result_dialogue
from src.database.db import get_attendance_for_teacher
def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()
    elif "teacher_login_type" not in st.session_state or st.session_state.teacher_login_type=="login":
         teacher_screen_login()
    elif st.session_state.teacher_login_type=="register":
        teacher_screen_register()
def  teacher_dashboard():
    teacher_data=st.session_state.teacher_data
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        st.subheader(f""" WelCome  {teacher_data['name']}""")
        if st.button("Logout",type="secondary",key="loginbakbtn",shortcut="control+backspace"):
            st.session_state['is_logged_in']=False
            del st.session_state['teacher_data']
            st.rerun()
    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = 'take_attendance'
    tab1, tab2, tab3 = st.columns(3)


    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendance' else "tertiary"
        if st.button('Take Attendance',type=type1, width='stretch', icon=':material/ar_on_you:'):
            st.session_state.current_teacher_tab = 'take_attendance'
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == 'manage_subjects' else "tertiary"
        if st.button('Manage Subjects', type=type2, width='stretch', icon=':material/book_ribbon:'):
            st.session_state.current_teacher_tab = 'manage_subjects'
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == 'attendance_records' else "tertiary"
        if st.button('Attendance Records',type=type3, width='stretch', icon=':material/cards_stack:'):
            st.session_state.current_teacher_tab = 'attendance_records'
            st.rerun()

    st.divider()
    if st.session_state.current_teacher_tab == 'take_attendance':
        tab_take_attendance()
    if st.session_state.current_teacher_tab == 'manage_subjects':
        tab_manage_subjects()
    if st.session_state.current_teacher_tab == 'attendance_records':
        tab_attendance_records()

    footer_dashboard()
def tab_take_attendance():
    teacher_id=st.session_state.teacher_data['teacher_id']
    st.header("Take AI Attendence")
    if "attendence_image" not in st.session_state:
        st.session_state.attendence_image=[]
    subjects=get_teacher_subjects(teacher_id)
    if not subjects:
        st.warning("No Subject Found Please Enter a Subject First")
        return
    subjects_options={f"{sub['name']}-{sub['subject_code']}":sub['subject_id'] for sub in subjects}

    col1,col2=st.columns([3,1],vertical_alignment="bottom") 
    with col1:
        select_subjects_label=st.selectbox("Select Subject",options=list(subjects_options.keys()),key="select_subjects_label")
    with col2:
        if st.button("Add Photos",type="primary",key="addphotos",icon=":material/add_a_photo:",icon_position="left",width="stretch"):
            add_photos_dialogue()
    selected_subject_id=subjects_options[select_subjects_label]
    st.divider()

    if st.session_state.attendence_image:
        st.subheader("Added Photos")
        galary_cols=st.columns(4)
        for i,photo in enumerate(st.session_state.attendence_image):
            with galary_cols[i%4]:
                st.image(photo,  caption=f"Photo {i+1}")
    has_photos=bool(st.session_state.attendence_image)
    c1,c2,c3=st.columns(3)
    with c1:
        if st.button("Clear All Photos",width="stretch",key="clr_photo",type="tertiary",icon=":material/delete:",disabled=not has_photos):
            st.session_state.attendence_image=[]
            st.rerun()
    with c2:
        if st.button("Run Face Analysis",type="secondary",key="analyse",width="stretch",icon=":material/analytics:",disabled=not has_photos):
            st.spinner("Analyzing the Faces......")
            all_detected_ids={}

            for i,img in enumerate(st.session_state.attendence_image):
                img_np=np.array(img.convert("RGB"))
                detected,_,_=predict_attendance(img_np)

                if detected:
                    for sid in detected.keys():
                        student_id=int(sid)

                        all_detected_ids.setdefault(student_id,[]).append(f"Photo {i+1}")

            enroll_response=supabase.table("subject_students").select("*,students(*)").eq("subject_id",selected_subject_id).execute()
            enroll_students=enroll_response.data
            if not enroll_students:
                st.warning('No students enrolled in this course')
            else:
                results, attendence_to_logs  = [], []

                current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


                for node in enroll_students:
                    student = node['students']
                    sources = all_detected_ids.get(int(student['student_id']), [])
                    is_present= len(sources) > 0

                    results.append({
                        "Name": student['name'],
                        "ID": student['student_id'],
                        "Source": ", ".join(sources) if is_present else "-",
                        "Status": "✅ Present" if is_present else "❌ Absent"
                    })

                    attendence_to_logs.append({
                        "timestamp": current_timestamp,
                        'student_id': student['student_id'],
                        "subject_id":selected_subject_id,
                        'is_present': bool(is_present)
                    })
            attendence_result_dialogue(pd.DataFrame(results),attendence_to_logs)
    with c3:
        if st.button("Use Voice Attendance",type="primary",key="voice",width="stretch",icon=":material/mic:"):
            voice_attendance_dialogue(selected_subject_id)
def tab_manage_subjects():
    teacher_id=st.session_state.teacher_data['teacher_id']
    col1,col2=st.columns(2)
    with col1:
        st.header("Manage Subjects")
    with col2:
        if st.button("Add New Subject",type="primary",key="addnewsubject",shortcut="control+enter"):
            create_subject_dialogue(teacher_id)
    subjects=get_teacher_subjects(teacher_id)
    if subjects:
        for sub in subjects:
            stats =  stats = [
                ( "Students", sub['total_students']),
                ( "Classes", sub['total_classes']),
            ]
                
            
        def share_btn():
            if st.button(f"Share Code: {sub['subject_code']}",type="secondary",key=f"sharecode_{sub['subject_code']}",width="stretch",icon=":material/share:",icon_position="left"):
               share_subject_dialogue(sub['name'],sub['subject_code'])
            st.space()
        subject_card (
            name=sub['name'],
            section=sub['section'],
            code=sub['subject_code'],
            stats=stats,
            footer_callback=share_btn
        )
    else:
        st.info("No Subjects Found! Please Add New Subject")
def tab_attendance_records():
    st.header("Attendance Records")
    teacher_id=st.session_state.teacher_data["teacher_id"]
    records=get_attendance_for_teacher(teacher_id)
    if not records:
        return
    data=[]
    for r in records:
        ts=r.get("timestamp")
        data.append({
            "ts_group":ts.split(".")[0] if ts else None,
            "Time":datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "NA",
            "Subject":r["subjects"]["name"],
            "Subject Code":r["subjects"]["subject_code"],
            "is_present":bool(r.get("is_present",False))
        })
    df=pd.DataFrame(data)
    summary=(
        df.groupby(["ts_group","Time","Subject","Subject Code"])
        .agg(
            Present_Count=("is_present","sum"),
            Total_Count=("is_present","count")
        ).reset_index()
    )
    summary['Attendance Stats'] = (
        "✅ " + summary['Present_Count'].astype(str) + " /"
        + summary['Total_Count'].astype(str) + ' Students'
    )

    display_df = ( summary.sort_values(by='ts_group' ,ascending=False)
                  [['Time', 'Subject', 'Subject Code', 'Attendance Stats']]
                  )
    
    st.dataframe(display_df, width='stretch', hide_index=True)
def login_teacher(username,password):
    if not username or not password:
        return False
    teacher=teacher_login(username,password)
    if teacher:
        st.session_state.user_role="teacher"
        st.session_state.teacher_data=teacher
        st.session_state.is_logged_in=True
        return True
    return False

def teacher_screen_login():
    style_background_dashboard()
    style_base_layout()
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Back To Home",type="secondary",key="backtohome",shortcut="control+backspace"):
            st.session_state['login_type']=None
            st.rerun()
    st.header("Login with Password")
    st.space()
    text_username=st.text_input("Enetr Username",placeholder="Dhanam")
    text_password=st.text_input("Enter Your Password",placeholder="Password",type="password")
    st.divider()
    bt1,bt2=st.columns(2)
    with bt1:
       if st.button('Login', icon=':material/passkey:', shortcut='control+enter', width='stretch'):
           if login_teacher(text_username,text_password):
               st.toast("Welcome Back!!")
               import time
               time.sleep(1)
               st.rerun()
           else:
               st.error("Inavlid Crendentials")

    with bt2:
       if st.button("Register Instead",type="primary",icon=":material/passkey:",icon_position="left",width="stretch"):
           st.session_state.teacher_login_type ="register"
            
    footer_dashboard()


def register_teacher(teacher_username,teacher_name,teacher_password,confirm_password):
    if not teacher_name or not teacher_username or not teacher_password:
        return False,"All Fields are Required"
    if check_teacher_exists(teacher_username):
        return False,"Username Already Taken"
    if teacher_password !=confirm_password:
        return False ,"Please Enter Valid Password"
    try:
        create_teacher_login(teacher_username,teacher_password,teacher_name)
        return True ,"Successfully Register!Login Now"
    except Exception as e:
        return False,"Unexpected Error"
    
def teacher_screen_register():
    style_background_dashboard()
    style_base_layout()
    c1, c2 = st.columns(2, vertical_alignment='center', gap='xxlarge')
    with c1:
        header_dashboard()
    with c2:
        if st.button("Back To Home",type="secondary",key="backtohome",shortcut="control+backspace"):
            st.session_state["login_type"]=None
            st.rerun()
    st.header("Register Yourself Here")
    st.space()
    teacher_username=st.text_input("Enetr Username",placeholder="Dhanam")
    teacher_name=st.text_input("Enetr Your Name",placeholder="Dhanashri")
    teacher_password=st.text_input("Enter Your Password",placeholder="Password",type="password")
    confirm_password=st.text_input("Confirm Your Password",placeholder="Password",type="password")
    
    st.divider()
    bt1,bt2=st.columns(2)
    with bt1:
        if st.button('Register Now', icon=':material/passkey:', shortcut='control+enter', width='stretch'):
            success,message=register_teacher(teacher_username,teacher_name,teacher_password,confirm_password)
            if success:
                st.success(message)
                import time
                time.sleep(2)
                st.session_state.teacher_login_type="login"
                st.rerun()
            else:
                st.error(message)

    with bt2:
       if st.button("Login Instead",type="primary",icon=":material/passkey:",icon_position="left",width="stretch"):
            st.session_state.teacher_login_type ="login"
            st.rerun()  

            
    footer_dashboard()


    